<template>
  <div style="background: #f4f4f4;" v-bind:style="{minHeight:window_height+'px'}">
    <Top ref="top"></Top>
    <div>
        <Row style="margin: 20px 0px">
          <Col span="8">
            <span style="font-size: 15px;margin-left: 5px">All Reports</span>
            <Button type="primary" style="font-size: 15px;margin-left: 30px" icon="ios-cloud-upload-outline" @click="click">Upload Reports</Button>
            <input type="file" ref="uploadFile" style="display:none" accept=".csv" @change="upload"/>
          </Col>
        </Row>
        <div ref="area">
          <Row style="margin-top: 20px" v-for="item in show_result_list" :key="row_key">
              <Card class="report_info" style="width: 90%;margin-left: auto;margin-right: auto">
                <p slot="title">
                  <Row>
                    <Col span="8"><Icon type="md-document" />Report Set Overview</Col>
                    <Col span="8"><Icon type="md-clock" />Upload Time：<span>{{item.upload_time}}</span></Col>
                    <Col span="8"><Icon type="md-square-outline" />Report Num：<span>{{item.report_num}}</span></Col>
                  </Row>
                </p>
                <Table class="report_table" size="small" border :columns="table_column" v-bind:data="item.reports"></Table>
                <Row style="margin-top: 20px">
                  <Col span="12">
                    <Button type="primary" @click="showFeatureResult(item.sid)" style="z-index: 99">View Report Feature</Button>
                  </Col>
                  <Col span="12">
                    <Button type="primary" @click="showClusterResult(item.sid)">View Selection Result</Button>
                  </Col>
                </Row>
              </Card>
          </Row>
          <Page style="margin-top: 40px" :total="dataCount" :page-size="pageSize" show-total show-elevator @on-change="changePage"></Page>
        </div>
    </div>
    <Spin fix v-if="spinShow" style="width: 100%;height: 100%">
      <Icon type="ios-loading" size=18 class="demo-spin-icon-load"></Icon>
      <div>loading</div>
    </Spin>
    <Spin fix v-if="uploadingShow" style="width: 100%;height: 100%">
      <Icon type="ios-loading" size=18 class="demo-spin-icon-load"></Icon>
      <div>Uploading</div>
    </Spin>
  </div>
</template>

<script>
  import Top from "./Top";
    export default {
      name: "Home",
      components: {Top},
      data(){
        return{
          user_id:0,
          window_height: '',
          window_width: '',
          table_column:[
            {
              title: 'bugID',
              key: 'bug_id',
              width: (window.innerWidth*0.9-32)*0.14-1,
            },
            {
              title: 'bug category',
              key: 'bug_category',
              width: (window.innerWidth*0.9-32)*0.085-1,
            },
            {
              title: 'severity',
              key: 'severity',
              width: (window.innerWidth*0.9-32)*0.075-1,
            },
            {
              title: 'recurrence',
              key: 'recurrent',
              width: (window.innerWidth*0.9-32)*0.075-1,
            },
            {
              title: 'create date',
              key: 'bug_create_time',
              width: (window.innerWidth*0.9-32)*0.11-1,
            },
            {
              title: 'bug page',
              key: 'bug_page',
              width: (window.innerWidth*0.9-32)*0.075-1,
            },
            {
              title: 'bug description',
              key: 'description',
              width: (window.innerWidth*0.9-32)*0.139-1,
            },
            {
              title: 'img url',
              key: 'img_url',
              width: (window.innerWidth*0.9-32)*0.134-1,
            },
            {
              title: 'app name',
              key: 'app_name',
              width: (window.innerWidth*0.9-32)*0.075-1,
            },
            {
              title: 'device name',
              key: 'device',
              width: (window.innerWidth*0.9-32)/10-1,
            }
          ],
          report_set_list:[],
          show_result_list:[],
          dataCount: 0,
          pageSize: 5,
          spinShow:true,
          uploadingShow:false,
          row_key:''
        }
      },
      async mounted () {
        this.window_height=window.innerHeight;
        this.window_width=window.innerWidth;
        this.user_id = sessionStorage.getItem('user_id');
        if(this.user_id == null){
          window.location.href = '/#/login'
        }
        //拿数据
        let data = new URLSearchParams();
        data.append('uid', this.user_id);
        await this.$axios.post('/server/simpleReportSet/', data).then(re=>{
          this.report_set_list = re.data.reportSet
        });
        this.dataCount = this.report_set_list.length;
        if(this.dataCount<this.pageSize){
          this.show_result_list = this.report_set_list;
        }else{
          this.show_result_list = this.report_set_list.slice(0,this.pageSize);
        }
        this.spinShow = false
      },
      methods:{
        changePage(index){
          let _start = (index-1)*this.pageSize;
          let _end = index*this.pageSize;
          this.show_result_list = this.report_set_list.slice(_start,_end);
        },
        upload(event){
          let files = event.target.files || event.dataTransfer.files;
          let report_file = files[0];
          let fileType = report_file.name.split('.');	//取到文件名并使用“.”进行切割
          if(fileType[1] !== 'csv') {	//判断文件类型
            this.$Message.error('文件类型错误,请上传.csv格式文件')
          }else{
            this.uploadingShow = true;
            let reader = new FileReader();
            reader.readAsText(report_file,'utf-8');
            reader.onload = () => {
              let fileData = reader.result;
              let row = fileData.split('\n');
              let report_list = [];
              for(let i = 1 ; i < row.length; i++){
                let column = row[i].split(',');
                report_list.push({'bug_id': column[1], 'bug_category': column[2], 'severity': column[3],
                  'recurrent': column[4], 'bug_create_time': column[5], 'bug_page': column[6], 'description': column[7],
                  'img_url': column[8], 'app_name': column[9], 'device': column[10]});
              }
              let data = new URLSearchParams();
              data.append('uid', this.user_id);
              data.append('report_list', JSON.stringify(report_list));
              this.$axios.post('/server/uploadReport/', data).then(re=>{
                let sid = re.data.sid;
                this.$axios.post('/server/simpleReportSet/', data).then(re=>{
                  this.report_set_list = re.data.reportSet;
                  this.changePage(1);
                  this.uploadingShow = false
                });
              });
            }
          }
        },
        click(){
          this.$refs.uploadFile.click()
        },
        showFeatureResult(sid){
          console.log("yes");
          sessionStorage.setItem('sid', sid);
          window.location.href = '/#/feature'
        },
        showClusterResult(sid){
          sessionStorage.setItem('sid',sid);
          this.$router.push('/show')
        }
      }
    }
</script>

<style scoped>
  .demo-spin-icon-load{
    animation: ani-demo-spin 1s linear infinite;
  }
  @keyframes ani-demo-spin {
    from { transform: rotate(0deg);}
    50%  { transform: rotate(180deg);}
    to   { transform: rotate(360deg);}
  }
  .demo-spin-col{
    height: 100px;
    position: relative;
    border: 1px solid #eee;
  }
</style>
