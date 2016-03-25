from setuptools import setup, find_packages

import proxy


tests_require = [
    'pytest-twisted>=1.5',
]

install_requires = [
    'twisted>=16.0.0,<17.0.0',
]

setup(
    name='TigerHost Services Proxy',
    version=proxy.__version__,
    author='Naphat Sanguansin',
    author_email='naphat.krit@gmail.com',
    description='TigerHost Command-Line Client',
    packages=find_packages(),
    install_requires=install_requires,
    extras_require={'tests': tests_require},
    tests_require=tests_require,
    url='https://github.com/naphatkrit/TigerHost',
    entry_points='''
        [console_scripts]
        proxy=proxy.proxy
    ''',
)
