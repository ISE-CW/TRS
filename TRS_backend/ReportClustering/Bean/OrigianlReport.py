class OriginalReport:
    setID=''
    reportID=''
    bugID=''
    bugType=''
    bugSeverity=''
    bugRepeatRate=''
    createReportTime=''
    bugPage=''
    bugDescription=''
    bugImageURL=''
    appName=''
    device=''
    def __init__(self, data):
        self.setID=data['sid']
        self.reportID=data['rid']
        self.bugID=data['bug_id']
        self.bugType=data['bug_category']
        self.bugSeverity=data['severity']
        self.bugRepeatRate=data['recurrent']
        self.createReportTime=data['bug_create_time']
        self.bugPage=data['bug_page']
        self.bugDescription=data['description']
        self.bugImageURL=data['img_url']
        self.appName=data['app_name']
        self.device=data['device']
        return