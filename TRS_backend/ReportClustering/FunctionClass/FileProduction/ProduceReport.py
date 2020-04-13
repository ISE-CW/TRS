from TRS_backend.ReportClustering.Dao.ReportDao import *
from TRS_backend.ReportClustering.Util.Enumeration import *

# 根据用户的个性化聚类选择将聚类结果保存到文档中
# cluster_id指该次聚类操作的编号
# choices指用户的个性化聚类选择，是个数组，其中每个数组项choice 包括：choice['relevant_data'], choice['algorithm_chosen'], choice['parameters']
# report_tree指通过聚类算法生成的报告树的根节点
# good_reports指符合要求的特征数据
# bad_reports指不符合要求的特征数据
# level指暂时打印的内容属于第几层，level>=1
# num指level中的第几个，num>=1
# 通过先根遍历生成测试选择报告
def produceReport(workid, choices, report_tree, good_reports, bad_reports, level, num):
    result = ''
    if report_tree.isLeave():
        desc = getDescription(workid, good_reports[report_tree.center]['bug_id'])
        result += '<b>Bug ' + str(num) + ': </b>' + desc['description'] + '\n'
        result += '![](' + desc['image_url'] + ')\n'
        result += '<br>\n'
    else:
        # 1.先打印序列标号
        for i in range(0, level):
            result += '#'
        result += ' '

        # 2.再打印分类名称，包括内容有 复现步骤、出错控件、错误类型、控件截图
        choice = choices[level - 1]
        for item in choice['relevant_data']:
            if item == InputData.IMAGE_VECTOR:
                result += '控件截图、'
            elif item == InputData.PROBLEM_VECTOR:
                result += '错误类型、'
            elif item == InputData.WIDGET_VECTOR:
                result += '出错控件、'
            elif item == InputData.PROCEDURE_VECTOR:
                result += '复现步骤、'
        result = result[0:len(result) - 1]
        result += ' —— <b>分类 ' + str(num) + '</b>\n'

        # 3.打印他的子节点内容
        for i in range(0, len(report_tree.sons)):
            result += produceReport(workid, choices, report_tree.sons[i], good_reports, bad_reports, level + 1, i + 1)

    if level == 1 and num == 1 and len(bad_reports) > 0:
        result += '# 不完整的测试报告\n'
        for i in range(0, len(bad_reports)):
            report = bad_reports[i]
            desc = getDescription(workid, bad_reports[i]['bug_id'])
            result += '<b>Bug ' + str(i) + ': </b>' + desc['description'] + '\n'
            result += '![](' + desc['image_url'] + ')'
            result += '<br>\n'

    return result

def getDescription(workid,bug_id):
    report=getOrigianlReport(workid,bug_id)
    result={
        'description':report.getBugDescription(),
        'image_url':report.getBugImageURL()
    }
    return result