from setuptools import setup, find_packages

config = {
    'description': ' Bot that organizes Github Issues',
    'author': 'Athena Yao',
    'author_email': 'fu@dreamwidth.org.',
    'url': 'https://github.com/afuna/ghi-assist',
    'version': '0.1',
    'packages': find_packages(),
    'scripts': ['bin/server.py'],
    'name': 'GHI Assist'
}

setup(**config)