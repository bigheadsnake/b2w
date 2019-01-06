#!/usr/bin/python3
# -*-coding:UTF-8-*-

from bottle import route, run, template, static_file, install, mako_view, request, get, post, response, default_app, \
    redirect
from bottle_mysql import MysqlPlugin
from bottle_auth import AuthPlugin
import priviledge
import utils

install(MysqlPlugin())
install(AuthPlugin())


def make_priviledge_vars(url):
    def make_priviledge_vars_inner(fn):
        def wrapper(*args, **kwargs):
            db = kwargs['db']

            if 'user' in kwargs:
                user = kwargs['user']
            else:
                user = None

            # 检查是否有权限访问
            if not priviledge.can_access(db, user, url):
                redirect('/entry?error=2')

            # 更新显示菜单
            r = fn(*args, **kwargs)
            update_vars = priviledge.nav_display_flags(db, user)
            r.update(update_vars)
            return r

        return wrapper

    return make_priviledge_vars_inner


def make_template_vars(fn):
    def wrapper(*args, **kwargs):
        dft_vars = {'active_user': ''
                    }
        r = fn(*args, **kwargs)
        # 使用 r 更新 dft_vars
        dft_vars.update(r)
        return dft_vars

    return wrapper


def make_login_vars(fn):
    def wrapper(*args, **kwargs):
        # 检查输入是否包含非法字符，若有，则直接返回不含参数的本页
        if request.query.dict is not None:
            for k in request.query.dict:
                for v in range(0, len(request.query.dict[k])):
                    if utils.check_html_request(request.query.dict[k][v]):
                        redirect('/entry?error=3')

        r = fn(*args, **kwargs)

        if 'user' in kwargs:
            user = kwargs['user']
            login_vars = {'logged': user.logged}
            login_vars.update(r)
            return login_vars
        else:
            return r

    return wrapper


@post('/login')
def login(db, user):
    if user.authenticate(request.forms.get('username'), request.forms.get('password')):
        redirect("/")
    redirect('/entry?error=1')


@route('/logout')
def logout(db, user):
    user.logout()
    redirect('/')


@route('/entry')
@mako_view('entry.html')
@make_priviledge_vars('/entry')
@make_template_vars
@make_login_vars
def login(db, user):
    if user.logged:
        redirect("/")
    error = request.query.error or None
    return {"page_title": u"B2W supply and marketing management system", "error": error, "posturl": '/'}


@route('/')
@mako_view('welcome.html')
@make_priviledge_vars('/welcome')
@make_template_vars
@make_login_vars
def welcome(db, user):
    if not user.logged:
        redirect("/entry")
    # f, rows = dbutils.get_table_dat(db, 'dk_WorkingProgress', 'StatDate', 'DESC', (0, 3))#
    # error = request.query.error or None

    return {"page_title": u"Beyond 2 Wheels"}


@route('/s/<filepath:path>')
def server_static(db, user, filepath):
    return static_file(filepath, root='./assets/')


@route('/<filename:re:.*\.png>')
def server_static(db, user, filename):
    return static_file(filename, root='./assets/img/', mimetype='image/png')


def run_cmd():
    # GunicornApplication 类会调用 parser.parse_args() 读取命令行参数，故此本脚本不再使用 ArgsPaser
    run(server='gunicorn', workers=4, host='0.0.0.0', port=80)


if __name__ == '__main__':
    run_cmd()
