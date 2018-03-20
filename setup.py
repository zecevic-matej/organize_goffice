from setuptools import setup

setup(
    name='goffice',
    version='0.1',
    py_modules=['quickstart'],
    install_requires=[
        'Click',
        'httplib2',
        'google_api_python_client',
        'setuptools'
    ],
    entry_points='''
        [console_scripts]
        goffice=quickstart:cli
    ''',
)