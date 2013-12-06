from os import path
from subprocess import Popen
from fabric.api import local, cd, lcd, get, env, roles, execute, task, run, \
                       settings, abort, hide
from fabric.colors import yellow

from agency_vars import with_vars

import logging
logging.basicConfig()
log = logging.getLogger(__name__)


# paths
base_path   = "./project/static"
css_path    = base_path + "/css/"
config_path = css_path + "config.rb"


# sass execs
exec_sass_watch   = "compass watch --poll {} -c {}"
#exec_sass_compile = "compass compile {} --output-style compressed -c {} --force"
exec_sass_compile = "compass compile {} -c {} --trace --force"


@task
@with_vars
def env_test():
    local('env | grep AGENCY')

@task
def runall():
    local('touch nohup.out')
    local('nohup fab vagrant.celery &')
    local('nohup fab vagrant.celerybeat &')
    local('nohup fab vagrant.css_watch &')
    local('nohup fab vagrant.runserver &')
    local('tail -f nohup.out')

@task
def killall():
    log.warning(yellow('killing all processes'))
    with settings(warn_only=True):
        local("ps ax | grep '[m]anage.py runserver' | awk '{ print $1 }' | xargs sudo kill -9")
        local("ps ax | grep '[m]anage.py run_gunicorn' | awk '{ print $1 }' | xargs sudo kill -9")
        local("ps ax | grep '[m]anage.py worker' | awk '{ print $1 }' | xargs sudo kill -9")
        local("ps ax | grep '[m]anage.py celerybeat' | awk '{ print $1 }' | xargs sudo kill -9")
        local("ps ax | grep '[m]anage.py compass' | awk '{ print $1 }' | xargs sudo kill -9")
        local("ps ax | grep '[m]anage.py sass' | awk '{ print $1 }' | xargs sudo kill -9")

@task
def runserver():
    with settings(warn_only=True):
        # FOR SOME REASON IF THE PROCESS WASN'T ENDED CORRECTLY, THIS WILL KILL IT
        local("ps ax | grep '[m]anage.py runserver' | awk '{ print $1 }' | xargs kill -9")
    local('python ./manage.py runserver [::]:8000')

@task
def gunicorn():
    with settings(warn_only=True):
        # FOR SOME REASON IF THE PROCESS WASN'T ENDED CORRECTLY, THIS WILL KILL IT
        local("ps ax | grep '[m]anage.py run_gunicorn' | awk '{ print $1 }' | xargs kill -9")
        local('python ./manage.py run_gunicorn [::]:8000')

@task
def celery():
    with settings(warn_only=True):
        # FOR SOME REASON IF THE PROCESS WASN'T ENDED CORRECTLY, THIS WILL KILL IT
        local("ps ax | grep '[m]anage.py worker' | awk '{ print $1 }' | xargs kill -9")
        local('python manage.py celery worker --loglevel=INFO')


@task
def celerybeat():
    with settings(warn_only=True):
        # FOR SOME REASON IF THE PROCESS WASN'T ENDED CORRECTLY, THIS WILL KILL IT
        local("ps ax | grep '[m]anage.py celerybeat' | awk '{ print $1 }' | xargs kill -9")
        local('python manage.py celerybeat --loglevel=INFO')

@task
def initdb(load_images=False):
    local('yes no | python manage.py syncdb')
    local('python manage.py migrate')
    local('python manage.py createsuperuser')

    if load_images:
        load_fixture_images()
    load_fixtures()


@task
def syncdb():
    local('python manage.py syncdb')
    local('python manage.py migrate')

@task
def resetall():
    """Stop all services, destroy the database, restore it from fixtures, remove all files in uploads directory and download assets."""
    killall()
    local('vagrant provision')
    resetdb(delete_images=True, load_images=True)

@task
def resetdb(load_images=False, delete_images=False):
    killall()



    # mysql
    # local("mysql -u vagrant -pvagrant -e 'drop database if exists django'")
    # local('mysql -u vagrant -pvagrant -e "create database django"')

    # postgres
    local('dropdb django')
    local('createdb django')
    if delete_images:
        local("mkdir -p ./uploads")
        with lcd("./uploads"):
            local('rm -rf ./*')

    initdb(load_images)

@task
def load_fixtures():
    local("python manage.py loaddata  project/fixtures/local_data.json")


@task
def load_fixture_images():
    # basic media fixture stub
    uploads_dir = path.abspath(path.join(path.dirname(__file__), '../uploads'))
    with lcd(uploads_dir):
        with settings(warn_only=True):
            local('rm -rf ./*')
        #local('curl -sLO https://domain/assets.tar.bz2')
        #local('tar xjvf assets.tar.bz2')
        #local('rm assets.tar.bz2')

@task
def collectstatic(no_input=False, skip_admin=False):
    local('python manage.py collectstatic {} {}'.format('--noinput' if no_input else '', '-i "admin*" -i "grappelli*"' if skip_admin else ''))

@task
def css_watch(new_config=None):
    with settings(warn_only=True):
        # Killing all sass processes before executing a new one
        local("ps ax | grep [c]ompass | awk '{ print $1 }' | xargs sudo kill -9")
    local(exec_sass_watch.format(base_path, config_path))

@task
def pipinstall():
    local('/home/vagrant/.venv/bin/pip install --use-mirrors -r ./requirements/local.txt')

@task
def css_compile():
    local(exec_sass_compile.format(base_path, config_path))

@task
def test():
    local('python manage.py test')