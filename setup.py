"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['arte.py']
DATA_FILES = []
OPTIONS = {'iconfile': './icon/icon.icns'}

setup(
    app=APP,
    name='Arte+7',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
