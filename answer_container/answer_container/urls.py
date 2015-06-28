from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls',\
        namespace='accounts')),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^qanda/', include('QandA.urls', namespace='qanda')),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^api/', include('api.urls')),#, namespace='api')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
