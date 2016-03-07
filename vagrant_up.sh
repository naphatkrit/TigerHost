#!/usr/bin/env bash

sudo aptitude -y update
sudo aptitude -y upgrade

# for batch install (i.e., no intervention)
sudo aptitude -y install debconf-utils

# to run the Django local server process in the background
sudo aptitude -y install screen

sudo aptitude -y install python-pip
sudo aptitude -y install python-requests


# all of this required for the PostgreSQL extension
sudo aptitude -y install python-dev
sudo aptitude -y install postgresql
sudo aptitude -y install libpq-dev
sudo aptitude -y install python-psycopg2



# install mysql server
## echo "mysql-server-5.5 mysql-server/root_password_again password $MYSQL_ROOT_PASSWORD" | debconf-set-selections
## echo "mysql-server-5.5 mysql-server/root_password password $MYSQL_ROOT_PASSWORD" | debconf-set-selections
## sudo aptitude -y install mysql-server
##

## should be in requirements
##sudo pip install django
export DATABASE_URL=postgres://vagrant@10.0.2.2:5432/vagrant
export BROKER_URL=amqp://guest:guest@10.0.2.2:5672//
sudo pip install -r /vagrant/requirements.txt
python /vagrant/manage.py migrate
python /vagrant/manage.py loaddata /vagrant/api_server/fixtures/test_user.json


export DJANGO_DEBUG=True
export DJANGO_EXTERNAL_PORT=8000
export DJANGO_DEBUG_NETID=$1

# start the server
screen -dmS djangoproc bash -c 'python /vagrant/manage.py runserver 0.0.0.0:8000'
screen -dmS celeryproc bash -c '(cd /vagrant && celery -A api_server worker -l info)'
# quit with
# screen -S djangoproc -X quit
