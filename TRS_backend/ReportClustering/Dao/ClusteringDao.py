from TRS_backend.data import *
from TRS_backend.ReportClustering.Util.Enumeration import *
def getSingleClusteringReport(srid):
    data=get_select_result(srid)
    if data.reduction==0:
        data.reduction=''
    else:
        data.reduction=Reduction(data.reduction)
    return data

def getAllClusteringReport(sid):
    data=get_select_results(sid)
    for item in data:
        if item.reduction==0:
            item.reduction=''
        else:
            item.reduction=Reduction(item.reduction)
    return data

def saveClusteringReport(sid,create_time,reduction,select_param,path):
    if reduction is None:
        return insert_select_result(sid,create_time,0,select_param,path)
    else:
        return insert_select_result(sid, create_time,reduction.value,select_param, path)