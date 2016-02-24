from setuptools import setup, find_packages

import tigerhost


tests_require = [
    'flake8>=2.4.0',
    'pytest>=2.5.0',
    'mock>=1.0.0',
]

install_requires = [
    'Click>=6.0',
    'subprocess32>=3.2.6',
]

setup(
    name='tigerhost',
    version=tigerhost.__version__,
    author='Naphat Sanguansin',
    author_email='naphat.krit@gmail.com',
    description='TigerHost Command-Line Client',
    packages=find_packages(),
    install_requires=install_requires,
    extras_require={'tests': tests_require},
    tests_require=tests_require,
    entry_points='''
        [console_scripts]
        tigerhost=tigerhost.entry:entry
    ''',
)
