class ReportFeature:
    bug_id=''
    procedure_vector=''
    widget_vector=''
    problem_vector=''
    image_vector=''
    is_widget_available=''
    andrimg_path=''

    def __init__(self,feature):
        self.bug_id=feature['bug_id']
        self.procedure_vector=feature['procedure_vector']
        self.widget_vector=feature['widget_vector']
        self.problem_vector=feature['problem_vector']
        self.image_vector=feature['image_vector']
        self.is_widget_available=feature['is_widget_available']
        self.andrimg_path=feature['andrimg_path']
        return