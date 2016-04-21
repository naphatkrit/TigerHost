import os


APP_NAME = 'tigerhost-deploy'

PROJECT_REMOTE = 'git@github.com:naphatkrit/TigerHost.git'

DOMAIN_NAME = 'tigerhostapp.com'

DEBUG = bool(os.environ.get('DEBUG', False))

DEISCTL_INSTALL_URL = 'http://deis.io/deisctl/install.sh'

DEIS_INSTALL_URL = 'http://deis.io/deis-cli/install.sh'

ADDONS_COMPOSE_PROJECT_NAME = 'addons'

MAIN_COMPOSE_PROJECT_NAME = 'tigerhost'
