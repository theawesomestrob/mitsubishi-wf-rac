"""Local configuration"""
import os
import socket
import getpass

MY_DEVICE_ID = socket.gethostname()
MY_OPERATOR_ID = getpass.getuser()

TIMEZONE='UTC'
if os.path.exists('/etc/timezone'):
    with open('/etc/timezone', 'r', encoding='utf-8') as f:
        TIMEZONE=f.read().strip()
