from TRS_backend.data import *
from TRS_backend.ReportClustering.Bean.OrigianlReport import *

# 根据workid获取某个测试报告集所包含的所有所有测试报告原始文件
def getOrigianlReports(workid):
    result=[]
    reports=find_report(workid);
    for item in reports:
        result.append(OriginalReport(item))
    return result

# 根据workid和bugid锁定某个测试报告原始文件
def getOrigianlReport(workid,bugid):
    return OriginalReport(get_report(bugid))
