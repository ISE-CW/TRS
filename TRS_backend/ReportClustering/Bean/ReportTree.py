class ReportTree:
    sons=[] #包含从这个层级进行分类后的树节点集合
    values=[] #包含在当前层报告索引的集合
    center=0 #指明values中哪个feature可以作为最终聚类的选择描述
    def __init__(self, values):
        self.values=values;
        self.center=values[0]
        self.sons=[]

    def isLeave(self):
        if len(self.sons)==0:
            return True
        else:
            return False

    def addSon(self,son):
        self.sons.append(son)