class ReportVector:
    feature_id = ''
    report_id = ''
    set_id = ''
    procedure_vector=''
    widget_vector=''
    problem_vector=''
    is_widget_available=''
    problem_widget_vector=''
    other_widget_vector=''
    def __init__(self,feature, text_vector, image_vector):
        self.feature_id=feature.feature_id
        self.report_id=feature.report_id
        self.set_id=feature.set_id
        self.procedure_vector=text_vector['procedure_vector']
        self.widget_vector=text_vector['widget_vector']
        self.problem_vector=text_vector['problem_vector']
        self.is_widget_available=image_vector['is_widget_available']
        self.problem_widget_vector=image_vector['problem_widget_vector']
        self.other_widget_vector=image_vector['other_widget_vector']