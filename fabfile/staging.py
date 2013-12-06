from heroku import CustomTask, deploy, deploy_source, deploy_static_media, deploy_user_media, sync_prod_db

deploy = CustomTask(deploy, 'feature_fabscripts')
deploy_source = CustomTask(deploy_source, 'feature_fabscripts')
deploy_static_media = CustomTask(deploy_static_media, 'feature_fabscripts')
deploy_user_media = CustomTask(deploy_user_media, 'feature_fabscripts')
sync_prod_db = CustomTask(sync_prod_db, 'feature_fabscripts')