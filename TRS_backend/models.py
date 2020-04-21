from django.db import models


# Create your models here.
class User(models.Model):
    uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)
    password = models.CharField(max_length=20)

    class Meta:
        db_table = 'user'


class ReportSet(models.Model):
    sid = models.AutoField(primary_key=True)
    uid = models.IntegerField(null=False)
    upload_time = models.DateTimeField(auto_now_add=True)
    report_num = models.IntegerField(null=False, default=0)

    class Meta:
        db_table = 'report_set'


class Report(models.Model):
    rid = models.AutoField(primary_key=True)
    sid = models.IntegerField(null=False)
    bug_id = models.CharField(max_length=40)
    bug_category = models.CharField(max_length=10)
    severity = models.CharField(max_length=10)
    recurrent = models.CharField(max_length=10)
    bug_create_time = models.CharField(max_length=40)
    bug_page = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    img_url = models.CharField(max_length=200)
    app_name = models.CharField(max_length=20)
    device = models.CharField(max_length=20)

    class Meta:
        db_table = 'report'


class SelectResult(models.Model):
    srid = models.AutoField(primary_key=True)
    sid = models.IntegerField(null=False)
    create_time = models.CharField(max_length=15)
    reduction = models.IntegerField(null=True)
    select_parm = models.CharField(max_length=100)
    path = models.CharField(max_length=100)

    class Meta:
        db_table = 'select_result'


class FeatureResult(models.Model):
    frid = models.AutoField(primary_key=True)
    rid = models.IntegerField(null=False)
    sid = models.IntegerField(null=False,default=0)
    recurrent_procedure = models.CharField(max_length=200)
    bug_description = models.CharField(max_length=200)
    problem_widget = models.CharField(max_length=20)
    is_match = models.BooleanField(default=True)
    widget_path = models.CharField(max_length=200)
    pic_path = models.CharField(max_length=200)

    class Meta:
        db_table = 'feature_result'


class OtherWidget(models.Model):
    frid = models.IntegerField(null=False)
    path = models.CharField(max_length=200)

    class Meta:
        db_table = 'other_widget'
