from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.views.generic import TemplateView
from tastypie.api import Api

from task.api import TaskResource, ProjectResource, TokenResource, TaskUserDetailResource

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(TaskResource())
v1_api.register(ProjectResource())
v1_api.register(TokenResource())
v1_api.register(TaskUserDetailResource())

urlpatterns = patterns('',
    (r'^grappelli/', include('grappelli.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    # api
    (r'^api/', include(v1_api.urls)),

    # Homepage
    (r'^$', TemplateView.as_view(template_name='index.html')),
)

#used to show static assets out of the collected-static
if getattr(settings, 'SERVE_STATIC', False) and settings.SERVE_STATIC:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': False,}),
        url(r'^uploads/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': False,}),
    )
