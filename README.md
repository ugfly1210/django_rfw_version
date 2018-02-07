# django_rfw_version 以及昨日回顾以及解析器浅析

# day3 

补充：
###### 关于实例化
```python
v1 = ['view.xxx.path.Role','view.xxx.path.']
```
> 回顾
#### 为什么用 django restframework？
关于认证、权限、节流，只需要写类，就可以实现他们的方法返回值就可。
它帮我们实现了一些功能。

#### 设计好的点？
  单独视图配置和全局配置， 它的全局配置类似django中间件(importlib + 反射)。
  动态配置可扩展（用户下单后，通过短信、邮件等提醒）。
  
#### 关于它的原理：
  基于 cbv，和 django 继承的是同一个。
  请求进来之后，先执行 dispatch （ 五大功能，都是在 dispatch 里面实现）。
  - 先执行 as_view()
  - view 函数
    obj = cls()
    。。。
    return self.dispatch()
  - dispatch
    - 封装 request
    - 版本
    - 认证 -> request.user -> 循环对象，执行_authticate
    - 权限
    - 节流

#### 新 request对象(request，认证相关)
  如果新 req 对象里面没有你要的东西，就去旧的 request 里面找。
          request.query_params
          request.POST
          request.Meta  
          
          
> 今日内容
1. 版本，
2. 解析器，
3. 序列化，
4. 分页

版本和解析器一旦配置好，基本可以不用再动。
序列化：
  - QuuerySet 类型 -> list,dict
  - 请求验证
django form 组件也可以用在 restframework。


### 1. 为什么要有版本？ 
  如果是version_1，就返回111
  如果是version_2，就返回22
  如果是version_3，就返回3
  自己可以在 url 里面写，然后 request 获取再判断就可以。
  
  但是d_rfw 已经帮你做好了。
  from rest_framework.versioning
  versioning_class = QueryParameterVersioning  # 这个就是帮你获取 version 的值。
  推荐:
  versioning_class = UrlPathVersioning
  
###### 版本源码执行流程
  ```python
  1. 进来先到 dispatch()
     def dispatch(self, request, *args, **kwargs):
  2. self.initial(request, *args, **kwargs)
  3.  # 处理版本信息
      # 这两句是处理版本信息，点击self.determine_version
        version, scheme = self.determine_version(request, *args, **kwargs)
        request.version, request.versioning_scheme = version, scheme
  4. def determine_version(self, request, *args, **kwargs):
         if self.versioning_class is None:
            return (None, None)
         scheme = self.versioning_class()
         return (scheme.determine_version(request, *args, **kwargs), scheme)
  5. URLPathVersioning.determine_version(self, request, *args, **kwargs):
     return version
  6. 封装到 request 中
     request.version, request.versioning_scheme = version, scheme
  7. 使用
     class URLPathVersion(APIView):
    # 关于 urlpath
    versioning_class = URLPathVersioning

    def get(self,request,*args,**kwargs):
        print(request.version)
        print(request.versioning_scheme)
  ```
