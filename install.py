import os
import sys
import shutil
import subprocess

# Default Backend Configuration
_BACKEND_PATH = "/home/django"
_VENV_PYTHON_PATH = "/home/django/venv/bin/python"
_VENV_PIP_PATH = "/home/django/venv/bin/pip"
_VENV_DAPHNE_PATH = "/home/django/venv/bin/daphne"

_BASE_PATH = ""
_DAEMON_PATH = "/etc/systemd/system/daphne_daemon.service"
_NGIX_PATH = "/etc/nginx"
_LOG_PATH = "/var/log/website"

def system_arguments(arg):
    global _BASE_PATH

    if _BASE_PATH == "":
        _BASE_PATH = os.getcwd()

    if arg == '-s':
        print("Prepath definition is captured!")
        specific_backend_path()
    elif arg == '-i':
        print("Installation has begun!")
        installation()
    elif arg == '-n':
        print("NGINX Configuration has begun!")
        set_nginx_conf()
    elif arg == '-d':
        print("Daemon Configuration has begun!")
        set_daphne_daemon()
    else:
        print("Unaccepted Arguments")
        print("Setup is determined!")
        raise KeyError(f"Installation process is not failed due to unexpected argument {arg}")

def specific_backend_path():
    global _BACKEND_PATH
    global _VENV_PYTHON_PATH
    global _VENV_PIP_PATH

    _BACKEND_PATH = input("Please enter desired backend path")
    _BACKEND_PATH.replace("\n", "")
    print("Backend Path is updated!")
    _VENV_PIP_PATH = f"{_BACKEND_PATH}/venv/bin/pip"
    _VENV_PYTHON_PATH = f"{_BACKEND_PATH}/venv/bin/python"

def installation():
    global _LOG_PATH
    global _BACKEND_PATH
    global _BASE_PATH

    print("Creating Log Folder")
    if not os.path.exists(_LOG_PATH):
        os.mkdir(_LOG_PATH)
    set_website()

def set_website():
    global _BACKEND_PATH
    global _BASE_PATH

    items = os.listdir(_BASE_PATH)

    print("Relocation of website items")
    for item in items:
        shutil.move(f"{_BASE_PATH}/{item}", _BACKEND_PATH)

    create_venv()
    set_database_application()

def set_nginx_conf():
    global _BACKEND_PATH
    global _BASE_PATH
    global _NGIX_PATH

    os.chdir(_BACKEND_PATH)
    if os.path.exists(f"{_BACKEND_PATH}/nginx.conf"):
        print("Configuration Relocation")
        execute_os_command(f"mv {_BACKEND_PATH}/nginx.conf {_NGIX_PATH}/sites-available/")
        print("Creating Symbolink")
        execute_os_command(f"ln -s {_NGIX_PATH}/sites-available/nginx.conf {_NGIX_PATH}/sites-enabled/")
        print("Restarting NGINX Service")
        execute_os_command("systemctl restart nginx")
    else:
        raise KeyError("There is no NGINX configuration file is found\nPlease start installation without -n parameter!")

def set_daphne_daemon():
    global _DAEMON_PATH
    if os.path.exists(_DAEMON_PATH):
        raise KeyError("Daemon is already set!\nPlease remove -d argument in your installation")
    else:
        print("Writing Daemon Into Place")
        info = f"""[Unit]
Description=Django Daphne Service
After=network.target

[Service]
WorkingDirectory={_BACKEND_PATH}
ExecStart={_VENV_DAPHNE_PATH} -b 127.0.0.1 -p 8000 kanban_backend.asgi:application
Restart=always
StandardOutput=append:/var/log/website/daphne_output.log;
StandardError=append:/var/log/website/daphne_error.log;

[Install]
WantedBy=multi-user.target
"""
        print("Running Daemon")
        with open(_DAEMON_PATH, 'a') as file_op:
            file_op.write(info)
        execute_os_command("systemctl start daphne_daemon")
        execute_os_command("systemctl enable daphne_daemon")
        print("Enabling Daemon")

def set_database_application():
    global _BACKEND_PATH
    global _BASE_PATH
    global _VENV_PYTHON_PATH
    
    os.chdir(_BACKEND_PATH)
    print("Database migration is started!")
    execute_os_command(f"{_VENV_PYTHON_PATH} manage.py makemigrations")
    execute_os_command(f"{_VENV_PYTHON_PATH} manage.py migrate")
    print("Database migration is over!")
    os.chdir(_BASE_PATH)

def create_venv():
    global _BACKEND_PATH
    global _BASE_PATH

    os.chdir(_BACKEND_PATH)
    execute_os_command("python3 -m venv venv")
    execute_os_command(f"{_VENV_PIP_PATH} install -r {_BACKEND_PATH}/requirements.txt")
    os.chdir(_BASE_PATH)

def execute_os_command(commands):
    command_list = commands.split(" ")
    process = subprocess.Popen(command_list, shell=True, stdout=subprocess.PIPE)
    process.wait()

if __name__ == "__main__":
    args = sys.argv[1:]
    print("Setup is started")

    for arg in args:
        accepted_args = ['-i', '-n', '-d', '-s']
        if not arg in accepted_args:
            print("Unaccepted Arguments")
            print("Setup is determined!")
            raise KeyError(f"Installation process is not failed due to unexpected argument {arg}")
        else:
            pass

    print("Accepted Arguments")
    for arg in args:
        system_arguments(arg)
    print("Setup is completed!")
