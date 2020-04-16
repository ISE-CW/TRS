from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import View
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
import TRS_backend.data as data
import json


# Create your views here.

def test(request):
    # 检测请求方法，如果是GET则直接返回原页面，是POST则执行接下来的添加操作
    if request.method == 'POST':
        parm = request.POST.get('parm')
        print(parm)
        res = '后端返回参数示例'
        result = {'status': 1, 'msg': '前端传入参数:' + parm + '后端返回参数:' + res}
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


# 获取首页预览数据
def get_report_set_simple_info(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        r_set = data.find_report_set(uid)
        result = []
        for reportSet in r_set:
            sid = reportSet['sid']
            upload_time = reportSet['upload_time']
            report_num = reportSet['report_num']
            report_list = data.find_report(sid)
            reports = []
            if len(report_list) <= 5:
                for report in report_list:
                    reports.append({'bug_id': report['bug_id'], 'bug_category': report['bug_category'],
                                    'severity': report['severity'], 'recurrent': report['recurrent'],
                                    'bug_create_time': report['bug_create_time'], 'bug_page': report['bug_page'],
                                    'description': report['description'], 'img_url': report['img_url'],
                                    'app_name': report['app_name'], 'device': report['device']})
                while len(reports) < 6:
                    reports.append({'bug_id': '', 'bug_category': '', 'description': '', 'app_name': ''})
            else:
                for i in range(5):
                    report = reports[i]
                    reports.append({'bug_id': report['bug_id'], 'bug_category': report['bug_category'],
                                    'severity': report['severity'], 'recurrent': report['recurrent'],
                                    'bug_create_time': report['bug_create_time'], 'bug_page': report['bug_page'],
                                    'description': report['description'], 'img_url': report['img_url'],
                                    'app_name': report['app_name'], 'device': report['device']})
                reports.append({'bug_id': '更多待查看', 'bug_category': '更多待查看',
                                'severity': '更多待查看', 'recurrent': '更多待查看',
                                'bug_create_time': '更多待查看', 'bug_page': '更多待查看',
                                'description': '更多待查看', 'img_url': '更多待查看',
                                'app_name': '更多待查看', 'device': '更多待查看'})
            result.append({'sid': sid, 'upload_time': upload_time, 'report_num': report_num, 'reports': reports})
        return JsonResponse({'reportSet': result})
    else:
        print(request)
        return HttpResponseRedirect('/请求地址')


# 上传报告
def upload_report(request):
    if request.method == 'POST':
        report_list_str = request.POST.get('report_list')
        uid = request.POST.get('uid')
        report_list = json.loads(report_list_str)
        sid = data.insert_report_set(uid, len(report_list))
        for report in report_list:
            data.insert_report(sid, report['bug_id'], report['bug_category'], report['severity'], report['recurrent'],
                               report['bug_create_time'], report['bug_page'], report['description'], report['img_url'],
                               report['app_name'], report['device'])
        report_set = data.get_report_set(sid)
        return JsonResponse({'sid': sid, 'upload_time': report_set['upload_time']})

    else:
        print(request)
        return HttpResponseRedirect('/请求地址')
