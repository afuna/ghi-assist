try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': ' Bot that organizes Github Issues',
    'author': 'Athena Yao',
    'author_email': 'fu@dreamwidth.org.',
    'url': 'https://github.com/afuna/ghi-assist',
    'version': '0.1',
    'packages': ['ghi_assist'],
    'scripts': [],
    'name': 'GHI Assist'
}

setup(**config)