# encoding=utf-8
import server
import sys
import environ

if __name__ == '__main__':
    print(sys.version)
    environ.run_env()
    server.run(host='0.0.0.0', port=80, debug=True, reloader=False)
