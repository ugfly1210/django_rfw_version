from django.conf.urls import url,include
from rest_framework.versioning import QueryParameterVersioning,HostNameVersioning,URLPathVersioning

from . import views

urlpatterns = [
    url(r'query_param/', views.QueryParam.as_view(),name='query_param'),
    url(r'^(?P<v>[v1|v2]+)/url_path', views.URLPathVersion.as_view(),name='url_path'),
    url(r'^host_name',views.HostNameVersion.as_view(),name='host_name')
]