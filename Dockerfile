FROM xxx.xxx.xxx:80/runtime/centos7/python

COPY src /build/
WORKDIR /build

RUN yum -y install python-mako tzdata gcc python-devel python-ldap
RUN pip install fluent-logger \
    && pip install gunicorn \
    && pip install requests \
    && pip install PyMySQL \
    && pip install pandas \
    && pip install sqlalchemy \
    && pip install openpyxl

EXPOSE 80
CMD ["python", "server.py", "--access-logfile", "-", "--error-logfile", "-", "--timeout", "60"]
