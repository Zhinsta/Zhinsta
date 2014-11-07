# coding: utf-8

from setuptools import setup, find_packages

install_requires = [
    'Flask-Cache',
    'MySQL-python',
    'flask',
    'flask-admin',
    'flask-restful',
    'flask-sqlalchemy',
    'flask-wtf',
    'gevent',
    'itsdangerous',
    'python-instagram',
    'redis',
    'sqlalchemy',
    'wtforms==1.0.5',
]

entry_points = {
    'console_scripts': [
        'run = zhinsta.app:run',
        'refresh = script.refresh_user:main'
    ]
}

setup(
    name="zhinsta",
    version="0.0.1",
    packages=find_packages(),
    install_requires=install_requires,
    entry_points=entry_points,
)
