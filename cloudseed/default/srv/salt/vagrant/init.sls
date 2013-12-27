{% from "python/map.jinja" import python with context %}
{% set user = 'vagrant' %}
{% set home = '/home/%s'|format(user) %}
{% set envpath = '%s/project-env'|format(home)  %}

include:
  - vim
  - build-tools
  - python.virtualenv
  - ruby.compass
  - node
  - node.requirejs
  - redis
  - heroku
  - git
  - rabbitmq
  - memcached
  - postgresql
  - postgresql.dev

app.user:
  user.present:
    - name: app
    - home: /home/app
    - shell: /bin/false
    - system: true
    - password: $1$tRNpmY/o$4ssNcGsrm9Spv2TfzKSb51
    - order: 1

app.sudoer:
    file.append:
        - name: /etc/sudoers
        - text:
          - 'app    ALL=(ALL)  NOPASSWD: ALL'

app.virtualenv:
  virtualenv.managed:
    - name: {{ envpath }}
    - require:
      - pip: python.virtualenv

app.gevent.libevent:
  pkg:
    - installed
    - name: {{ python.libevent_dev }}

app.heroku.path:
  cmd.wait_script:
    - source: salt://heroku/files/add_to_path.py
    - user: vagrant
    - args: {{ home }}
    - require:
      - pkg: python.core
    - watch:
      - cmd: heroku.core

app.virtualenv.source:
  file.append:
    - name: "/home/{{ user }}/.bashrc"
    - text: "source {{ envpath }}/bin/activate"
    - require:
      - virtualenv: app.virtualenv

app.ps1:
  file.append:
    - name: "/home/{{ user }}/.bashrc"
    - text: |
            purple='\[\e[0;35m\]'
            yellow='\[\e[0;33m\]'
            Bwhite='\[\e[0;37m\]'
            reset='\[\e[0m\]'
            export  PS1="\[[${purple}\u@\h ${Bwhite}\w${reset}\$(__git_ps1 \" (${yellow}%s${reset})\")]\n\$(date +%H:%M) \$ "
    - require:
      - file: app.virtualenv.source

app.cdwww:
  file.append:
    - name: "/home/{{ user }}/.bashrc"
    - text: 'cd /var/www'
    - require:
      - file: app.virtualenv.source

app.pip.install:
  pip:
    - installed
    - name: requirements
    - requirements: /var/www/requirements/local.txt
    - bin_env: {{ envpath }}
    - require:
      - pkg: build-tools.core
      - pkg: postgresql.dev
      - virtualenv: app.virtualenv
      - pkg: app.gevent.libevent
      - file: app.ps1

