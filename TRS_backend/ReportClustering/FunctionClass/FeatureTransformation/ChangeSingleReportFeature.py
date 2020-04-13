import numpy as nu
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