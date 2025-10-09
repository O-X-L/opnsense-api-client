from sys import path as sys_path
from os import path as os_path

sys_path.append(os_path.dirname(os_path.abspath(__file__)))

# pylint: disable=C0413
from basic.client import Client
