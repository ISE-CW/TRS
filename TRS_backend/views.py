from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import View
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse


# Create your views here.

def test(request):
    # 检测请求方法，如果是GET则直接返回原页面，是POST则执行接下来的添加操作
    if request.method == 'POST':
        parm = request.POST.get('parm')
        print(parm)
        res = '后端返回参数示例'
        result = {'status': 1, 'msg': '前端传入参数:'+parm+'后端返回参数:'+res}
        return JsonResponse(result)
    else:
        print('你妈死了')
        print(request)
        return HttpResponseRedirect('/请求地址')
