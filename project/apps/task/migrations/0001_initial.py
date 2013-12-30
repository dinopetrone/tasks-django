# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Organization'
        db.create_table(u'task_organization', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'task', ['Organization'])

        # Adding model 'TaskUser'
        db.create_table(u'task_taskuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=254)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=254, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['task.Organization'], null=True, blank=True)),
        ))
        db.send_create_signal(u'task', ['TaskUser'])

        # Adding M2M table for field groups on 'TaskUser'
        m2m_table_name = db.shorten_name(u'task_taskuser_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('taskuser', models.ForeignKey(orm[u'task.taskuser'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['taskuser_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'TaskUser'
        m2m_table_name = db.shorten_name(u'task_taskuser_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('taskuser', models.ForeignKey(orm[u'task.taskuser'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['taskuser_id', 'permission_id'])

        # Adding model 'Project'
        db.create_table(u'task_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['task.Organization'], null=True, blank=True)),
        ))
        db.send_create_signal(u'task', ['Project'])

        # Adding M2M table for field users on 'Project'
        m2m_table_name = db.shorten_name(u'task_project_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'task.project'], null=False)),
            ('taskuser', models.ForeignKey(orm[u'task.taskuser'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'taskuser_id'])

        # Adding model 'Task'
        db.create_table(u'task_task', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=2000, null=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['task.Project'])),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('loe', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('task_type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('assigned_to', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['task.TaskUser'], null=True, blank=True)),
        ))
        db.send_create_signal(u'task', ['Task'])

        # Adding model 'TaskHistory'
        db.create_table(u'task_taskhistory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['task.Task'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['task.TaskUser'])),
        ))
        db.send_create_signal(u'task', ['TaskHistory'])


    def backwards(self, orm):
        # Deleting model 'Organization'
        db.delete_table(u'task_organization')

        # Deleting model 'TaskUser'
        db.delete_table(u'task_taskuser')

        # Removing M2M table for field groups on 'TaskUser'
        db.delete_table(db.shorten_name(u'task_taskuser_groups'))

        # Removing M2M table for field user_permissions on 'TaskUser'
        db.delete_table(db.shorten_name(u'task_taskuser_user_permissions'))

        # Deleting model 'Project'
        db.delete_table(u'task_project')

        # Removing M2M table for field users on 'Project'
        db.delete_table(db.shorten_name(u'task_project_users'))

        # Deleting model 'Task'
        db.delete_table(u'task_task')

        # Deleting model 'TaskHistory'
        db.delete_table(u'task_taskhistory')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'task.organization': {
            'Meta': {'object_name': 'Organization'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'task.project': {
            'Meta': {'object_name': 'Project'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['task.Organization']", 'null': 'True', 'blank': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['task.TaskUser']", 'null': 'True', 'blank': 'True'})
        },
        u'task.task': {
            'Meta': {'object_name': 'Task'},
            'assigned_to': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['task.TaskUser']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'loe': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['task.Project']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'task_type': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'task.taskhistory': {
            'Meta': {'object_name': 'TaskHistory'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['task.Task']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['task.TaskUser']"})
        },
        u'task.taskuser': {
            'Meta': {'object_name': 'TaskUser'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['task.Organization']", 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '254', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['task']