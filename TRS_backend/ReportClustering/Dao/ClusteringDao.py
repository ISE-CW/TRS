from TRS_backend.data import *
from TRS_backend.ReportClustering.Util.Enumeration import *
from TRS_backend.ReportClustering.Util.Transformation import *


def getSingleClusteringReport(srid):
    data = get_select_result(srid)
    if data.reduction == 0:
        data.reduction = ''
    else:
        data.reduction = changeEnumToChinese(Reduction(data.reduction))
    return data


def getAllClusteringReport(sid):
    data = get_select_results(sid)
    for item in data:
        if item.reduction == 0:
            item.reduction = ''
        else:
            item.reduction = changeEnumToChinese(Reduction(item.reduction))
    return data


def saveClusteringReport(srid, sid, create_time, reduction, select_param, path,state):
    if reduction is None:
        return update_select_result(srid, sid, create_time, 0, select_param, path,state)
    else:
        return update_select_result(srid, sid, create_time, reduction.value, select_param, path,state)


def getSetInfo(sid):
    return getSetInfo(sid)
