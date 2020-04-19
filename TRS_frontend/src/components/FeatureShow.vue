<template>
  <div style="background: #f4f4f4;" v-bind:style="{minHeight:window_height+'px'}">
    <Top ref="top"></Top>
    <div class="layout">
      <Sider v-bind:style="{position: 'fixed', height: '100vh', left: 0, overflow: 'auto', minWidth: window_width*0.22+'px',
      maxWidth: window_width*0.22+'px'}" >
        <Card v-for="(report,index) in show_reports" style="width: 80%; margin-left: auto; margin-right: auto;
        margin-top: 10px; margin-bottom: 10px; cursor: pointer">
          <p slot="title" @click="selectReport(report)">报告<span>{{index+1}}</span></p>
          <p style="text-align: left" @click="selectReport(report)"><span style="font-weight: bold">bugID:</span><span>{{report.bug_id}}</span></p>
          <p style="text-align: left" @click="selectReport(report)"><span style="font-weight: bold">bug类别:</span><span>{{report.bug_category}}</span></p>
          <p style="text-align: left" @click="selectReport(report)"><span style="font-weight: bold">严重程度:</span><span>{{report.severity}}</span></p>
          <p style="text-align: left" @click="selectReport(report)"><span style="font-weight: bold">复现频率:</span><span>{{report.recurrent}}</span></p>
          <p style="text-align: left" @click="selectReport(report)"><span style="font-weight: bold">创建时间:</span><span>{{report.bug_create_time}}</span></p>
          <p style="text-align: left" @click="selectReport(report)"><span style="font-weight: bold">bug页面:</span><span>{{report.bug_page}}</span></p>
          <p style="text-align: left" @click="selectReport(report)"><span style="font-weight: bold">bug描述:</span><span>点击查看详情</span></p>
          <p style="text-align: left" @click="selectReport(report)"><span style="font-weight: bold">截屏url:</span><span>点击查看详情</span></p>
          <p style="text-align: left" @click="selectReport(report)"><span style="font-weight: bold">app名称:</span><span>{{report.app_name}}</span></p>
          <p style="text-align: left" @click="selectReport(report)"><span style="font-weight: bold">设备名称:</span><span>{{report.device}}</span></p>
        </Card>
        <Row style="height: 60px"></Row>
      </Sider>
      <Layout v-bind:style="{marginLeft: '200px', minWidth: window_width*0.78+'px', maxWidth: window_width*0.78+'px', minHeight: (window_height-80)+'px', maxHeight: (window_height-80)+'px'}">
        <Content :style="{padding: '20px 16px 16px'}">
            <Row>
              <Col span="12">
                <Card style="width: 90%" v-model="report_detail">
                  <p slot="title">报告详情</p>
                  <p style="text-align: left"><span style="font-weight: bold">bugID:</span><span>{{report_detail.bug_id}}</span></p>
                  <p style="text-align: left"><span style="font-weight: bold">bug类别:</span><span>{{report_detail.bug_category}}</span></p>
                  <p style="text-align: left"><span style="font-weight: bold">严重程度:</span><span>{{report_detail.severity}}</span></p>
                  <p style="text-align: left"><span style="font-weight: bold">复现频率:</span><span>{{report_detail.recurrent}}</span></p>
                  <p style="text-align: left"><span style="font-weight: bold">创建时间:</span><span>{{report_detail.bug_create_time}}</span></p>
                  <p style="text-align: left"><span style="font-weight: bold">bug页面:</span><span>{{report_detail.bug_page}}</span></p>
                  <p style="text-align: left"><span style="font-weight: bold">bug描述:</span><span>{{report_detail.description}}</span></p>
                  <p style="text-align: left"><span style="font-weight: bold">截屏图片:</span>
                    <viewer :images="original_img" :options="options">
                      <img v-for="src in original_img" :src="src" :key="src" class="images" style="height: 250px">
                    </viewer>
                  </p>
                  <p style="text-align: left"><span style="font-weight: bold">app名称:</span><span>{{report_detail.app_name}}</span></p>
                  <p style="text-align: left"><span style="font-weight: bold">设备名称:</span><span>{{report_detail.device}}</span></p>
                </Card>
              </Col>
              <Col span="12">
                <Row>
                  <Card v-model="text_feature" style="width: 90%;min-height: 200px">
                    <p slot="title">报告文本特征提取结果</p>
                    <p style="text-align: left"><span style="font-weight: bold">复现步骤识别结果:</span><span>{{text_feature.procedures}}</span></p>
                    <p style="text-align: left"><span style="font-weight: bold">问题控件识别结果:</span><span>{{text_feature.problem_widget}}</span></p>
                    <p style="text-align: left"><span style="font-weight: bold">bug描述识别结果:</span><span>{{text_feature.problems}}</span></p>
                  </Card>
                </Row>
                <Row style="margin-top: 20px">
                  <Card style="width: 90%;min-height: 350px">
                    <p slot="title">报告图片特征提取结果</p>
                    <p v-if="is_match" style="text-align: left"><span style="font-weight: bold">截屏图片控件识别结果(红色框标识的为问题控件，蓝色框标识的为其余控件):</span>
                      <viewer :images="result_img" :options="options">
                        <img v-for="src in result_img" :src="src" :key="src" class="images" style="height: 250px">
                      </viewer>
                    </p>
                    <h1 v-else>没有识别出截屏中对应的问题控件，该份报告图文信息不匹配，视为无效报告</h1>
                  </Card>
                </Row>
              </Col>
            </Row>
        </Content>
      </Layout>
    </div>
    <Spin fix v-if="spinShow" style="width: 100%;height: 100%">
      <Icon type="ios-loading" size=18 class="demo-spin-icon-load"></Icon>
      <div>{{spinText}}</div>
    </Spin>
  </div>
</template>

<script>
  import Top from "./Top"
  import 'viewerjs/dist/viewer.css'
  import Viewer from 'v-viewer'
  import Vue from 'vue'
  Vue.use(Viewer);
    export default {
      name: "FeatureShow",
      components: {Top},
      data(){
        return{
          sid : 0,
          window_height: 0,
          window_width: 0,
          show_reports:[],
          report_detail:{
            'bug_id': '',
            'bug_category': '',
            'severity': '',
            'recurrent': '',
            'bug_create_time': '',
            'bug_page': '',
            'description':'',
            'app_name':'',
            'device':'',
          },
          options:{
            toolbar:false,
            navbar:false
          },
          text_feature:{
            'procedures': [],
            'problem_widget': '',
            'problems': [],
          },
          original_img:[],
          result_img:[],
          is_match: true,
          spinShow: true,
          spinText: '加载中...'
        }
      },
      mounted() {
        this.window_height = window.innerHeight;
        this.window_width = window.innerWidth;
        this.sid = sessionStorage.getItem('sid');
        if(this.sid == null){
          window.location.href = "/#/home";
        }
        let data = new URLSearchParams();
        data.append('sid', this.sid);
        this.$axios.post('/server/isFeatureExist/', data).then(re=>{
          this.spinText = re.data.msg;
          this.$axios.post('/server/getReportSetFeature/',data).then(re=>{
            this.show_reports = re.data.featureResult;
            this.selectReport(this.show_reports[0]);
            this.spinShow = false
          })
        });
      },
      methods:{
        selectReport(report){
          this.report_detail = {'bug_id':report.bug_id,'bug_category': report.bug_category, 'severity': report.severity,
            'recurrent': report.recurrent, 'bug_create_time': report.bug_create_time, 'bug_page': report.bug_page,
            'description': report.description, 'app_name': report.app_name, 'device': report.device};
          this.text_feature ={'procedures': report.procedures, 'problem_widget': report.problem_widget,
            'problems': report.problems};
          this.original_img = [];
          this.original_img.push(report.img_url);
          this.is_match = report.is_match;
          this.result_img = [];
          this.result_img.push(report.result_img)
        }
      }
    }
</script>

<style scoped>
  .layout{
    border: 1px solid #d7dde4;
    background: #f5f7f9;
    position: relative;
    border-radius: 4px;
    overflow: hidden;
  }
  .layout-header-bar{
    background: #fff;
    box-shadow: 0 1px 1px rgba(0,0,0,.1);
  }
  .images{
    cursor: pointer;
    margin: 5px;
    display: inline-block;
  }
</style>
