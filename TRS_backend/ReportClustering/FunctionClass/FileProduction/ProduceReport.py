from TRS_backend.ReportClustering.Dao.ReportDao import *
from TRS_backend.ReportClustering.Dao.FeatureDao import *
from TRS_backend.ReportClustering.Util.Enumeration import *
from TRS_backend.ReportClustering.Util.Transformation import *

# 根据用户的个性化聚类选择将聚类结果保存到文档中
# cluster_id指该次聚类操作的编号
# choices指用户的个性化聚类选择，是个数组，其中每个数组项choice 包括：choice['relevant_data'], choice['algorithm_chosen'], choice['parameters']
# report_tree指通过聚类算法生成的报告树的根节点
# good_reports指符合要求的特征数据
# bad_reports指不符合要求的特征数据
# level指暂时打印的内容属于第几层，level>=1
# num指level中的第几个，num>=1
# cluster_index指这是文档中的第几个cluster
# 通过先根遍历生成测试选择报告
def produceReport(workid, choices, reduction, report_tree, good_reports, bad_reports,first):
    result = ''
    if report_tree.isLeave():
        center_desc = getDescription(workid, good_reports[report_tree.center].report_id)
        result+='<html>\n' \
                '<table>\n' \
                '<tr>\n' \
                '<th colspan=3 style="text-align:center;font-size:30px">Cluster Group</th>\n' \
                '</tr>\n' \
                '<tr>\n' \
                '<td><b>Center Report</b></td>\n' \
                '<td style="width:300px">Value: '+str(report_tree.center)+'<br><br>BUG ID: '+center_desc['bug_id']+'<br><br>'+center_desc['description']+'</td>\n' \
                '<td><img src="'+center_desc['image_url']+'" style="width:350px"></td>\n' \
                '</tr>\n'
        for item in report_tree.values:
            if item!=report_tree.center:
                desc=getDescription(workid,good_reports[item].report_id)
                result+='<tr>\n' \
                        '<td>Similar Report</td>\n' \
                        '<td style="width:300px">Value: '+str(item)+'<br><br>BUG ID: '+desc['bug_id']+'<br><br>'+desc['description']+'</td>\n' \
                        '<td><img src="'+desc['image_url']+'" style="width:350px"></td>\n' \
                        '</tr>\n'
        result+='</table>\n</html>\n\n'
    else:
        # # 1.先打印序列标号
        # for i in range(0, level):
        #     result += '#'
        # result += ' '
        #
        # # 2.再打印分类名称，包括内容有 复现步骤、出错控件、错误类型、控件截图
        # choice = choices[level - 1]
        # for item in choice['relevant_data']:
        #     if changeChineseToEnum(item) == InputData.PROBLEM_WIDGET_VECTOR:
        #         result += 'Problem Widget Screenshots、'
        #     elif changeChineseToEnum(item) == InputData.OTHER_WIDGET_VECTOR:
        #         result += 'Other Widget Screenshots、'
        #     elif changeChineseToEnum(item) == InputData.PROBLEM_VECTOR:
        #         result += 'Bug Type、'
        #     elif changeChineseToEnum(item) == InputData.WIDGET_VECTOR:
        #         result += 'Problem Widget、'
        #     elif changeChineseToEnum(item) == InputData.PROCEDURE_VECTOR:
        #         result += 'Replay Steps、'
        # result = result[0:len(result) - 1]
        # result += ' —— <b>Category ' + str(num) + '</b>\n'
        # if (changeEnumToChinese(InputData.PROBLEM_WIDGET_VECTOR) in choice['relevant_data'])\
        #         or (changeEnumToChinese(InputData.OTHER_WIDGET_VECTOR) in choice['relevant_data']):
        #     if changeChineseToEnum(reduction)==Reduction.AVERAGE:
        #         result += '<b>Use Average Method to Execute Dimensional Reduction</b><br>'
        #     elif changeChineseToEnum(reduction)==Reduction.DIMENSIONAL:
        #         result += '<b>Use PCA Method to Execute Dimensional Reduction</b><br>'

        # 3.打印他的子节点内容
        for i in range(0, len(report_tree.sons)):
            result += produceReport(workid, choices, reduction, report_tree.sons[i], good_reports, bad_reports,False)
        if first and len(bad_reports) > 0:
            result += '<html>\n' \
                      '<table>\n' \
                      '<tr>\n' \
                      '<th colspan=3 style="text-align:center;font-size:30px">Incomplete Test Reports</th>\n' \
                      '</tr>\n'
            for i in range(0, len(bad_reports)):
                desc = getDescription(workid, bad_reports[i].report_id)
                result += '<tr>\n' \
                          '<td>Incomplete<br>Report '+str(i+1)+'</td>\n' \
                          '<td style="width:300px">BUG ID: ' + desc['bug_id'] + '<br><br>' + desc['description'] + '</td>\n' \
                          '<td><img src="' + desc['image_url'] + '" style="width:350px"></td>\n' \
                          '</tr>\n'
            result += '</table>\n</html>\n\n'


    return result

def getDescription(workid,bug_id):
    report=getOrigianlReport(workid,bug_id)
    feature=getReportFeature(bug_id)
    result={
        'description':report.bugDescription,
        'image_url':feature.pic_url,
        'bug_id':report.bugID
    }
    return result