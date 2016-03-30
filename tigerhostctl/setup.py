from setuptools import setup, find_packages

import tigerhostctl

from tigerhostctl import settings


tests_require = [
    'flake8>=2.4.0',
    'pytest>=2.5.0',
    'mock>=1.0.0',
]

install_requires = [
    'Click>=6.0',
    'tigerhost==0.3.2',
    'subprocess32>=3.2.6',
]

setup(
    name=settings.APP_NAME,
    version=tigerhostctl.__version__,
    author='Naphat Sanguansin',
    author_email='naphat.krit@gmail.com',
    description='A tool for provisioning TigerHost.',
    packages=find_packages(),
    install_requires=install_requires,
    extras_require={'tests': tests_require},
    tests_require=tests_require,
    url='https://github.com/naphatkrit/TigerHost',
    entry_points='''
        [console_scripts]
        {app_name}=tigerhostctl.entry:entry
    '''.format(app_name=settings.APP_NAME),
)
