from TRS_backend.ReportClustering.BusinessLogic import ClusterBL
from TRS_backend.data import *
from TRS_backend.ReportClustering.Util.Enumeration import *
from TRS_backend.ReportClustering.Dao import ClusteringDao
from TRS_backend.ReportClustering.FunctionClass.FileProduction import FormatTransformation
from TRS_backend.ReportClustering.Util.Transformation import *
import time
from django.core import serializers
from TRS_backend.models import *
import json

def createCluster(sid,choices):
    current = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    reduction=changeChineseToEnum(choices[0]['reduction'])
    srid=insert_select_result(sid,current,reduction.value,'','',State.RUNNING.value)
    good_features, bad_features = ClusterBL.featureTransformation(sid, reduction)
    tree = ClusterBL.algorithmExecution(good_features, choices)
    ClusterBL.fileProduction(srid,sid, tree, choices, reduction, good_features, bad_features, current)
    return

def readFile(srid,format):
    cluster=ClusteringDao.getSingleClusteringReport(srid)
    path=cluster.path
    file=open(path,'r',encoding='UTF-8').read()
    return file

def downloadFile(srid,format):
    cluster = ClusteringDao.getSingleClusteringReport(srid)
    path = cluster.path
    if format == 'doc':
        new_path = FormatTransformation.markdownToWord(path)
    elif format == 'pdf':
        new_path = FormatTransformation.markdownToPDF(path)
    else:
        new_path = path
    file = open(new_path, 'r', encoding='UTF-8')
    return file

def getSetInfo(sid):
    set=get_report_set(sid)
    return set

def getClustersInfo(sid):
    clusters=ClusteringDao.getAllClusteringReport(sid)
    json_format=serializers.serialize("json", clusters)
    result_data=[]
    temp=json.loads(json_format)
    for i in range(0,len(temp)):
        cluster=temp[i]['fields']
        cluster['srid']=temp[i]['pk']
        cluster['state']=changeEnumToChinese(State(cluster['state']))
        choice=getChoice(cluster['select_param'])
        cluster['select_param']=json.loads(choice)
        result_data.append(cluster)
    return json.dumps(result_data)

def getChoice(path):
    choice=open(path,'r')
    content=choice.read()
    return content


