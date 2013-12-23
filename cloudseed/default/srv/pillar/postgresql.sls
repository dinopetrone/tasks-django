postgresql:
  users:
    app:
      password: app
      createdb: true

  databases:
    django:
      owner: app

  hba:
   - type: local
     database: django
     user: app
     method: ident

   - type: local
     database: postgres
     user: app
     method: ident

   - type: host
     database: django
     user: app
     address: 0.0.0.0/0
     method: md5
