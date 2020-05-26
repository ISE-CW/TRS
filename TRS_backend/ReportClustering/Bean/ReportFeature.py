class ReportFeature:
    feature_id=''
    report_id=''
    set_id=''
    procedure=''
    problem= ''
    widget=''
    is_widget_available = ''
    widget_path=''
    other_widget=''
    andrimg_path=''
    pic_url=''

    def __init__(self,feature):
        self.feature_id=feature['frid']
        self.report_id=feature['rid']
        self.set_id=feature['sid']
        self.procedure=feature['procedure']
        self.problem= feature['problem']
        self.widget=feature['widget']
        self.is_widget_available = feature['is_widget_available']
        self.widget_path=feature['widget_path']
        self.other_widget=feature['other_widget']
        self.andrimg_path=feature['andrimg_path']
        self.pic_url=feature['pic_url']
        return