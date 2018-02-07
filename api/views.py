from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.versioning import QueryParameterVersioning,URLPathVersioning,HostNameVersioning
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from django.urls import reverse
from urllib.parse import urlencode


class QueryParam(APIView):
    # self.dispatch
    # 基于 url 传参
    self.dispatch
    versioning_class = QueryParameterVersioning  # 基于 url 的 get 传参方式。
    # renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    # http://127.0.0.1:8000/api/query_param/
    # http://127.0.0.1:8000/api/query_param/?version=v2       # version 对应 settings 。

    def get(self,request,*args,**kwargs):
        print(request.version)           # 接收到的版本号
        print(request.versioning_scheme) # 版本类的实例
        """
        v2
        <rest_framework.versioning.QueryParameterVersioning object at 0x104beae10>
        """
        # 版本类的 reverse 方法，只能反向生成当前版本的 url
        reverse_url = request.versioning_scheme.reverse('query_param',request=request)
        print(reverse_url)

        # 如果想要生成任意版本的 url ，可以使用 django 的 reverse 方法
        base_url = reverse('query_param')
        reverse_url = '%s?%s'%(base_url,urlencode({'v':'v3'}))
        print(reverse_url)

        return Response('hao')


class URLPathVersion(APIView):
    # 关于正则
    # http://127.0.0.1:8000/api/v1/url_path/
    versioning_class = URLPathVersioning

    def get(self,request,*args,**kwargs):
        print(request.version)             # v1
        print(request.versioning_scheme)   # <rest_framework.versioning.URLPathVersioning object at 0x104c4be48>

        # 版本类的 reverse 方法，只能生成当前版本的 url
        reverse_url = request.versioning_scheme.reverse('url_path',request=request)
        print(reverse_url)                 # http://127.0.0.1:8000/api/v1/url_path

        # 使用 django 的 reverse 方法，可以生成任意 url
        base_url = reverse('url_path', kwargs={'v':'v2'})
        print(base_url)                    # /api/v2/url_path
        return Response('URLPathVersion_ok')


class HostNameVersion(APIView):
    # 基于主机名  http://v1.example.com:8000/api/host_name/
    versioning_class = HostNameVersioning

    def get(self,request,*args,**kwargs):
        print(request.version)           # v1
        print(request.versioning_scheme) # <rest_framework.versioning.HostNameVersioning object at 0x104babd68>

        # 版本类的reverse方法只能反向生成当前版本的url
        reverse_url = request.versioning_scheme.reverse('host_name', request=request)
        print(reverse_url)

        # django的reverse方法可以反向生成任意版本的url
        from django.urls import reverse
        base_url = reverse('hostname')
        reverse_url = "http://%s.example.com:8000/api/host_name/" % 'v2'
        print(reverse_url)

        return Response('Host_ok')
