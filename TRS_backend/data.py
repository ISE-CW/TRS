import os, django
import re
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TRS_manager.settings")
django.setup()

from TRS_backend.models import User, ReportSet, Report, SelectResult, FeatureResult, OtherWidget


# 定义所有数据库操作

# ----------User表相关操作--------------#

# 插入用户数据
def insert_user(name, password):
    user = User()
    user.name = name
    user.password = password
    user.save()
    return user.uid


# 查询用户数据
def find_user(name):
    res = User.objects.filter(name=name)
    for user in res:
        result = {'uid': user.uid, 'name': user.name, 'password': user.password}
        return result


# 查询用户名是否重复
def is_user_exist(name):
    res = User.objects.filter(name=name)
    return len(res) > 0


# 清空用户数据
def clean_user():
    User.objects.all().delete()


# ----------ReportSet表相关操作----------#

# 插入ReportSet数据
def insert_report_set(uid, report_num):
    report_set = ReportSet()
    report_set.uid = uid
    report_set.report_num = report_num
    report_set.save()
    return report_set.sid


# 查询ReportSet数据
def find_report_set(uid):
    res = ReportSet.objects.filter(uid=uid).order_by('-upload_time')
    r_set = []
    for report_set in res:
        result = {'sid': report_set.sid, 'uid': report_set.uid, 'report_num': report_set.report_num,
                  'upload_time': '{}.{}.{} {}:{}:{}'.format(report_set.upload_time.year, report_set.upload_time.month,
                                                            report_set.upload_time.day, report_set.upload_time.hour+8,
                                                            report_set.upload_time.minute, report_set.upload_time.second)}
        r_set.append(result)
    return r_set


# 获取指定id的ReportSet数据
def get_report_set(sid):
    res = ReportSet.objects.get(sid=sid)
    result = {'sid': res.sid, 'uid': res.uid, 'report_num': res.report_num,
              'upload_time': '{}.{}.{} {}:{}:{}'.format(res.upload_time.year, res.upload_time.month,
                                                        res.upload_time.day, res.upload_time.hour+8,
                                                        res.upload_time.minute, res.upload_time.second)}
    return result


# 清空ReportSet数据
def clean_report_set():
    ReportSet.objects.all().delete()


# ----------Report表相关操作-------------#

# 插入report数据
def insert_report(sid, bug_id, bug_category, severity, recurrent, bug_create_time, bug_page, description, img_url,
                  app_name, device):
    report = Report()
    report.sid = sid
    report.bug_id = bug_id
    report.bug_category = bug_category
    report.severity = severity
    report.recurrent = recurrent
    report.bug_create_time = bug_create_time
    report.bug_page = bug_page
    report.description = description
    report.img_url = img_url
    report.app_name = app_name
    report.device = device
    report.save()
    return report.rid


# 查询report数据
def find_report(sid):
    res = Report.objects.filter(sid=sid)
    result = []
    for report in res:
        r = {'rid': report.rid, 'sid': report.sid, 'bug_id': report.bug_id, 'bug_category': report.bug_category,
             'severity': report.severity, 'recurrent': report.recurrent, 'bug_create_time': report.bug_create_time,
             'bug_page': report.bug_page, 'description': report.description, 'img_url': report.img_url,
             'app_name': report.app_name, 'device': report.device}
        result.append(r)
    return result


# 得到指定id的report
def get_report(rid):
    report = Report.objects.get(rid=rid)
    result = {'rid': report.rid, 'sid': report.sid, 'bug_id': report.bug_id, 'bug_category': report.bug_category,
             'severity': report.severity, 'recurrent': report.recurrent, 'bug_create_time': report.bug_create_time,
             'bug_page': report.bug_page, 'description': report.description, 'img_url': report.img_url,
             'app_name': report.app_name, 'device': report.device}
    return result


# 清空report数据
def clean_report():
    Report.objects.all().delete()


# --------SelectResult表相关操作---------#

# 插入SelectResult数据
def insert_select_result(sid,create_time,reduction,select_param,path,state):
    result=SelectResult()
    result.sid=sid
    result.create_time=create_time
    result.select_param=select_param
    result.path=path
    result.reduction=reduction
    result.state=state
    result.save()
    srid=result.srid
    return srid

def update_select_result(srid,sid,create_time,reduction,select_param,path,state):
    result = get_select_result(srid)
    result.sid = sid
    result.create_time = create_time
    result.select_param = select_param
    result.path = path
    result.reduction = reduction
    result.state=state
    result.save()
    return srid

def get_select_result(srid):
    result = SelectResult.objects.get(srid=srid)
    return result

def get_select_results(sid):
    result=SelectResult.objects.filter(sid=sid)
    return result

# --------FeatureResult表相关操作--------#

# 插入FeatureResult数据
def insert_feature_result(rid, recurrent_procedure, bug_description, problem_widget, is_match, widget_path,
                          other_widget, pic_path, pic_url):
    report = get_report(rid)
    feature_result = FeatureResult()
    feature_result.rid = rid
    feature_result.sid = report['sid']
    feature_result.recurrent_procedure = ' '.join(recurrent_procedure)
    feature_result.bug_description = ' '.join(bug_description)
    feature_result.problem_widget = problem_widget
    feature_result.is_match = is_match
    feature_result.widget_path = widget_path
    feature_result.pic_path = pic_path
    feature_result.pic_url = pic_url
    feature_result.save()
    frid = feature_result.frid
    insert_other_widget(frid, other_widget)
    return frid


# 查询FeatureResult数据
def find_feature_result(sid):
    res = FeatureResult.objects.filter(sid=sid)
    feature_list = []
    for r in res:
        other_widget = find_other_widget(r.frid)
        procedures = re.split(' ', r.recurrent_procedure)
        procedures = [item for item in filter(lambda x: x != '', procedures)]
        descriptions = re.split(' ', r.bug_description)
        descriptions = [item for item in filter(lambda x: x != '', descriptions)]
        feature = {'frid': r.frid, 'rid': r.rid, 'sid': r.sid, 'procedure': procedures, 'problem': descriptions,
                   'widget': r.problem_widget, 'is_widget_available': r.is_match, 'widget_path': r.widget_path,
                   'other_widget': other_widget, 'andrimg_path': r.pic_path, 'pic_url': r.pic_url}
        feature_list.append(feature)
    return feature_list


# 查询特定报告对应的特征提取结果
def get_feature_result(rid):
    feature_result = FeatureResult.objects.get(rid=rid)
    other_widget = find_other_widget(feature_result.frid)
    procedures = re.split(' ', feature_result.recurrent_procedure)
    procedures = [item for item in filter(lambda x: x != '', procedures)]
    descriptions = re.split(' ', feature_result.bug_description)
    descriptions = [item for item in filter(lambda x: x != '', descriptions)]
    feature = {'frid': feature_result.frid, 'rid': feature_result.rid, 'sid': feature_result.sid,
               'procedure': procedures, 'problem': descriptions, 'widget': feature_result.problem_widget,
               'is_widget_available': feature_result.is_match, 'widget_path': feature_result.widget_path,
               'other_widget': other_widget, 'andrimg_path': feature_result.pic_path,
               'pic_url': feature_result.pic_url}
    return feature


# 查询是否已有FeatureResult数据
def is_feature_result_exist(sid):
    res = FeatureResult.objects.filter(sid=sid)
    return len(res) > 0


# 清空feature_report
def clean_feature_report():
    FeatureResult.objects.all().delete()


# --------OtherWidget表相关操作----------#

# 插入OtherWidget
def insert_other_widget(frid, path_list):
    for path in path_list:
        other_widget = OtherWidget()
        other_widget.frid = frid
        other_widget.path = path
        other_widget.save()


# 查询OtherWidget
def find_other_widget(frid):
    res = OtherWidget.objects.filter(frid=frid)
    widgets = []
    for r in res:
        widgets.append(r.path)
    return widgets


# 清空OtherWidget
def clean_other_widget():
    OtherWidget.objects.all().delete()


# uid = insert_user('test', '12345')
# sid = insert_report_set(1, 257)
# reports = pd.read_csv('F:\\360MoveData\\Users\\lenovo\\Desktop\\experiment\\result_file.csv')
# ids = reports['bug_id']
# categories = reports['bug_category']
# severities = reports['severity']
# recurrents = reports['recurrent']
# times = reports['bug_create_time']
# bug_page = reports['bug_page']
# descriptions = reports['description']
# images = reports['img_url']
# app_names = reports['app_name']
# devices = reports['device']
# for i in range(len(ids)):
#     insert_report(4, ids[i], categories[i], severities[i], recurrents[i], times[i], bug_page[i],
#                   descriptions[i], images[i], app_names[i], devices[i])
#
# res = find_report(4)
# for report in res:
#     print(report)
