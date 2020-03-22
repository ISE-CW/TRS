import numpy as nu
from TRS_backend.ReportClustering.Util.Enumeration import *
# 将特征提取子系统中的某一份报告转化为聚类子系统的统一输入形式，默认报告均为规范报告
def changeSingleReport(data):
    # 1. 将多个procedure vector进行加和求平均
    original_procedure_vector=data['procedure_vector']
    new_procedure_vector=nu.zeros([len(original_procedure_vector[0]),])
    for vector in original_procedure_vector:
        new_procedure_vector=nu.add(vector,new_procedure_vector)
    new_procedure_vector=new_procedure_vector*1.0/len(original_procedure_vector)

    # 2. 将多个problem vector进行加和求平均
    original_problem_vector=data['problem_vector']
    new_problem_vector=nu.zeros([len(original_problem_vector[0]),])
    for vector in original_problem_vector:
        new_problem_vector=nu.add(new_problem_vector,vector)
    new_problem_vector=new_problem_vector*1.0/len(original_problem_vector)

    # 3. 将image vector的二维形式转化为一维向量
    original_image_vector=data['image_vector']
    new_image_vector=nu.array([])
    for item in original_image_vector:
        new_image_vector=nu.append(new_image_vector,item)

    result={
        'bug_id':data['bug_id'],
        'procedure_vector':new_procedure_vector,
        'widget_vector':data['widget_vector'],
        'problem_vector':new_problem_vector,
        'image_vector':new_image_vector,
        'is_widget_available':data['is_widget_available'],
        'andrimg_path':data['andrimg_path']
    }

    return result

# 将特征提取子系统提供的所有报告转化为聚类子系统需要的输入形式，默认均为可用有效数据
def changeAllReports(data):
    result=[]
    for report in data:
        result.append(changeSingleReport(report))
    return result

# 获取特征提取子系统提供的数据，并将其转化为报告聚类子系统的数据格式
def getInitClusteringData(workid):
    # 将读入的一行字符串转化为浮点数numpy数组
    def changeStrToFloatArray(line):
        array=line[1:len(line)-2].split(',')
        nums = []
        for i in array:
            nums.append(float(i))
        return nu.array(nums)

    # 1. 先拿到features，并识别哪些有用哪些没用
    bad_reports = [] #存储所有无法识别控件的特征值
    good_reports = [] #存储所有数据完整的特征值
    #file=open(workid+"_feature.txt","r") #根据workid打开相应的feature文件
    file=open('\TRS\TRS_backend\ReportClustering\DataFile\FeatureFile\\'+workid+'_feature.txt','r')
    line=file.readline()
    line=line[0:len(line)-1]
    temp_feature={}
    while line:
        if "bug_id" in line:
            temp_feature={'bug_id':line[8:]}
        elif "is_widget_available" in line:
            if "True" in line:
                temp_feature['is_widget_available']=True
            else:
                temp_feature['is_widget_available']=False
        elif "andrimg_path" in line:
            temp_feature['andrimg_path']=line[14:]
        elif "procedure_vector" in line:
            num=int(line[18:])
            procedure=[]
            for i in range(0,num):
                procedure.append(nu.array(changeStrToFloatArray(file.readline())))
            temp_feature['procedure_vector']=procedure
        elif "widget_vector" in line:
            num=int(line[15:])
            widget=nu.array([])
            if num>0:
                widget=nu.array(changeStrToFloatArray(file.readline()))
            temp_feature['widget_vector']=widget
        elif "problem_vector" in line:
            num=int(line[16:])
            problem=[]
            for i in range(0,num):
                problem.append(nu.array(changeStrToFloatArray(file.readline())))
            temp_feature['problem_vector']=problem
        elif "image_vector" in line:
            num=int(line[14:])
            image=[]
            for i in range(0,num):
                image.append(changeStrToFloatArray(file.readline()))
            temp_feature['image_vector']=nu.array(image)
            if temp_feature['is_widget_available']:
                good_reports.append(temp_feature)
            else:
                bad_reports.append(temp_feature)
        line=file.readline()
        line = line[0:len(line) - 1]

    # 2. 将特征提取子系统的数据格式转换为报告聚类子系统的数据格式
    good_cluster_data=changeAllReports(good_reports)
    bad_cluster_data=changeAllReports(bad_reports)

    # 3. 将转化的有效的特征、无效的特征 通过字典返回
    return {'bad_reports':bad_cluster_data,'good_reports':good_cluster_data}

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
    result=''
    if report_tree.isLeave():
        desc=getDescription(workid,good_reports[report_tree.center]['bug_id'])
        result+='<b>Bug '+str(num)+': </b>'+desc['description']+'\n'
        result+='![]('+desc['image_url']+')\n'
        result+='<br>\n'
    else:
        # 1.先打印序列标号
        for i in range(0, level):
            result += '#'
        result+=' '

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
        result=result[0:len(result)-1]
        result += ' —— <b>分类 ' + str(num) + '</b>\n'

        # 3.打印他的子节点内容
        for i in range(0,len(report_tree.sons)):
            result+=produceReport(workid,choices,report_tree.sons[i],good_reports, bad_reports, level+1, i+1)

    if level==1 and num==1 and len(bad_reports)>0:
        result+='# 不完整的测试报告\n'
        for i in range(0,len(bad_reports)):
            report=bad_reports[i]
            desc=getDescription(workid,bad_reports[i]['bug_id'])
            result+='<b>Bug '+str(i)+': </b>'+desc['description']+'\n'
            result+='![]('+desc['image_url']+')'
            result+='<br>\n'

    return result

# 根据workid与报告的索引来获取某个特定的报告
# workid为本次工作的id
# bug_id为bug的唯一标识
def getDescription(workid,bug_id):
    result={
        'description':bug_id,
        'image_url':bug_id
    }
    return result





