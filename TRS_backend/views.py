from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import View
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
import TRS_backend.data as data


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
        print(request)
        return HttpResponseRedirect('/请求地址')


# 登录
def login(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        if data.is_user_exist(name):
            res = data.find_user(name)
            if res['password'] == password:
                result = {'status': 1, 'msg': res['uid']}
                return JsonResponse(result)
            else:
                result = {'status': -1, 'msg': '密码错误'}
                return JsonResponse(result)
        else:
            result = {'status': -1, 'msg': '用户名不存在'}
            return JsonResponse(result)
    else:
        print(request)
        return HttpResponseRedirect('/请求地址')


# 注册
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        if data.is_user_exist(name):
            result = {'status': -1, 'msg': '用户名已存在'}
            return JsonResponse(result)
        else:
            data.insert_user(name, password)
            result = {'status': 1, 'msg': '注册成功'}
            return JsonResponse(result)
    else:
        print(request)
        return HttpResponseRedirect('/请求地址')
