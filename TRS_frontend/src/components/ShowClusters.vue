<template>
    <div>
      <Top ref="top"></Top>

      <div id="set">
        <div id="set_content">
          <table>
            <tr>
              <th rowspan="2" id="set_name">数据集 {{set.sid}}</th>
              <th class="th1">上传日期</th>
              <td>{{set.upload_time}}</td>
            </tr>
            <tr>
              <th class="th1">报告数量</th>
              <td>{{set.report_num}}</td>
            </tr>
          </table>
        </div>
        <div class="data_back">
          <img src="../assets/data.jpg"/>
        </div>
      </div>

      <div id="new_cluster">
        <Button type="primary" size="large" @click="newCluster">新建聚类报告</Button>
      </div>

      <div id="clusters">
        <Collapse simple class="collapse">
          <Panel v-for="(item,index) in clusters" :key="item.srid" :name="item.srid+''" class="panel">
            <span class="title_icon" v-if="item.state=='State.FINISH'" style="background-color: #19be6b">已完成</span>
            <span class="title_icon" v-if="item.state=='State.RUNNING'" style="background-color: #ff9900">运行中</span>
            <span class="title_content">聚类报告{{index+1}}&emsp;&emsp;创建时间：{{item.create_time}}</span>
            <span class="title_button">
              <Button type="info" size="small" @click="preview(item.srid)" :disabled="item.state=='State.RUNNING'">查看</Button>
              <Button type="info" size="small" @click="download(item.srid)" :disabled="item.state=='State.RUNNING'">下载</Button>
            </span>
            <div slot="content" class="panel_content">
              <Card>
                <Tabs type="card">
                  <TabPane v-for="(choice,choice_index) in item.select_param" :key="choice_index" :label="'聚类层次' + (choice_index+1)">
                    <div class="title"><span>聚类输入数据</span></div>
                    <table>
                      <tr v-for="input in choice.relevant_data">
                        <td>{{input}}</td>
                      </tr>
                    </table>
                    <div class="title"><span>聚类使用算法</span></div>
                    <table>
                      <tr>
                        <td>{{choice.algorithm_chosen}}</td>
                      </tr>
                    </table>
                    <div class="title"><span>聚类算法参数</span></div>
                    <table class="param">
                      <tr v-for="(value,key,param_index) in choice.parameters">
                        <th>{{key}}</th>
                        <td>{{value}}</td>
                      </tr>
                    </table>
                  </TabPane>
                </Tabs>
              </Card>
            </div>
          </Panel>
        </Collapse>
      </div>
    </div>
</template>

<script>
  import Top from './Top'
    export default {
        name: "ShowClusters",
      components:{Top},
      beforeCreate(){
        var username=sessionStorage.getItem("username")
        if(username==null){
          this.$router.push('/login')
        }
        var check_num=sessionStorage.getItem("sid")
        if(check_num==null){
          this.$router.push('/home')
        }
      },
      data(){
          return{
            set:{
              sid:1,
              uid:2,
              upload_time:'2019.02.03 16:44:26',
              report_num:2
            },
            clusters:[
              {
                srid:'1',
                sid:'1',
                create_time:'2018.02.01 16:44:23',
                select_param:[
                  {
                    'relevant_data':['InputData.PROCEDURE_VECTOR','InputData.WIDGET_VECTOR'],
                    'algorithm_chosen':'ClusteringAlgorithm.KMEANS',
                    parameters:{
                      n_clusters:2,
                      init:'k-means++',
                      n_init: 10,
                      max_iter : 300,
                      tol : 0.0001,
                      precompute_distances : 'auto',
                      verbose : 0,
                      random_state : 'None',
                      copy_x : 'True',
                      n_jobs : 1,
                      algorithm: 'auto'
                    }
                  },
                  {
                    'relevant_data':['InputData.PROCEDURE_VECTOR','InputData.WIDGET_VECTOR'],
                    'algorithm_chosen':'ClusteringAlgorithm.GMM',
                    'parameters':{
                      'n_components' : 0,
                      'covariance_type' : 'full',
                      'tol' : 1e-3,
                      'reg_covar' : 1e-6,
                      'max_iter' : 100,
                      'n_init' :1,
                      'init_params' : 'random',
                      'weights_init' : 'None',
                      'means_init' : 'None',
                      'precisions_init' : 'None',
                      'random_state' : 'None',
                      'warm_start' : 'False',
                      'verbose' : 0,
                      'verbose_interval' : 10
                    }
                  }
                ],
                path:'\\TRS\\TRS_backend\\ReportClustering\\DataFile\\ClusteringFile\\1_20200416174120_clustering_report.md',
                reduction:'',
                state:'State.FINISH'
              },
              {
                srid:'2',
                sid:'1',
                create_time:'2018.02.01 16:44:23',
                select_param:[
                  {
                    'relevant_data':['InputData.PROCEDURE_VECTOR','InputData.WIDGET_VECTOR'],
                    'algorithm_chosen':'ClusteringAlgorithm.KMEANS',
                    'parameters':{
                      'n_clusters':2,
                      'init':'k-means++',
                      'n_init': 10,
                      'max_iter' : 300,
                      'tol' : 0.0001,
                      'precompute_distances' : 'auto',
                      'verbose' : 0,
                      'random_state' : 'None',
                      'copy_x' : 'True',
                      'n_jobs' : 1,
                      'algorithm': 'auto'
                    }
                  },
                  {
                    'n_components' : 0,
                    'covariance_type' : 'full',
                    'tol' : 1e-3,
                    'reg_covar' : 1e-6,
                    'max_iter' : 100,
                    'n_init' :1,
                    'init_params' : 'random',
                    'weights_init' : 'None',
                    'means_init' : 'None',
                    'precisions_init' : 'None',
                    'random_state' : 'None',
                    'warm_start' : 'False',
                    'verbose' : 0,
                    'verbose_interval' : 10
                  }
                ],
                path:'\\TRS\\TRS_backend\\ReportClustering\\DataFile\\ClusteringFile\\1_20200416174120_clustering_report.md',
                reduction:'',
                state:'State.RUNNING'
              }
            ],
            download_format:'markdown'
          }
      },
      async mounted() {
        let data = new URLSearchParams();
        data.append('sid',sessionStorage.getItem("sid"))
        await this.$axios.post('/server/getShowSet/',data).then(re=>{
          this.set=re.data
        })
        await this.$axios.post('/server/getShowClusters/',data).then(re=>{
          var temp=JSON.parse(re.data.info)
          this.clusters=temp
        })
      },
      methods:{
          preview(srid){
            sessionStorage.setItem("srid",srid)
            this.$router.push('/check')
          },
        download(srid){
          this.$Modal.confirm({
            title: '选择您要下载的格式',
            okText:'确认',
            cancelText:'取消',
            render: (h) => {
              return h('RadioGroup',
                {
                  props:
                    {
                      value:this.download_format
                    },
                  on:{
                    'on-change':(status)=>{
                      this.download_format=status
                    }
                  }
                },
                [
                  h('Radio',
                    {
                      props:
                        {
                          label:'markdown'
                        },
                    },
                  ),
                  h('Radio',
                    {
                      props:
                        {
                          label:'pdf'
                        },
                    },
                  ),
                  h('Radio',
                    {
                      props:
                        {
                          label:'doc'
                        },
                    },
                  )
                ]
                )
            },
            onOk: () => {
              let data=new URLSearchParams()
              data.append('srid',srid)
              data.append('format',this.download_format)
              this.$axios.post('/server/downloadFile/',data).then(re=>{
                this.content = re.data
                this.filename = '聚类报告_'+srid+'.md'
                const blob = new Blob([this.content])
                if (window.navigator.msSaveOrOpenBlob) {
                  // 兼容IE10
                  navigator.msSaveBlob(blob, this.filename)
                } else {
                  //  chrome/firefox
                  let aTag = document.createElement('a')
                  aTag.download = this.filename
                  aTag.href = URL.createObjectURL(blob)
                  aTag.click()
                  URL.revokeObjectURL(aTag.href)
                }
                this.download_format='markdown'
              })

            },
            onCancel: () => {
              this.download_format='markdown'
            }
          })
        },
        async getChoice(){
          for(var i=0;i<this.clusters.length;i++){
            let sub_data=new URLSearchParams();
            sub_data.append('path',this.clusters[i].select_param)
            console.log(this.clusters[i].select_param)
            await this.$axios.post('/server/getChoice/',sub_data).then(re=>{
              console.log(re)
            })
          }
          console.log(this.clusters)
        },
        newCluster(){
          sessionStorage.setItem('sid',this.set.sid)
          this.$router.push('/create')
        }
      }
    }
</script>
<style scoped>
  #new_cluster{
    text-align: left;
    margin-left: 12%;
  }

  #new_cluster button{
    width: 200px;
    margin-bottom: 20px;
  }

  #set{
    width: 100%;
    height: 220px;
    margin-top: 20px;
  }

  .data_back{
    position: absolute;
    height: 200px;
    z-index: -1;
  }

  .data_back img{
    width: 76%;
    margin-left: 12%;
    margin-right: 12%;
    height: 200px;
  }

  #set_content{
    position: absolute;
    width: 76%;
    margin-left: 12%;
    margin-right: 12%;
    background-color: rgba(0,0,0,0.7);
    height: 200px;
    z-index: 0;

  }

  #set_content table{
    margin: 0 auto;
    -webkit-text-fill-color: white;
    font-weight: bold;
    font-family: 宋体;
    font-size: 20px;
    margin-top: 30px;
  }

  .th1{
    font-weight: bold;
    font-size: 30px;
    padding: 10px;
    padding-left: 20px;
    padding-right: 20px;
  }

  #set_content td{
    padding: 10px
  }

  #set_name{
    font-size: 50px;
    width: 55%;
    text-align: left;
  }


#clusters{
  margin-left: 12%;
  margin-right: 12%;
  text-align: left;
}

.panel_content{
  padding-left: 10%;
  padding-right: 10%;
  margin-top: 20px;
}

.title_icon{
  -webkit-text-fill-color: white;
  font-weight: bold;
  padding: 5px;
  border-radius: 5px;
  margin-right: 20px;
}

.title_content{
  font-weight: bold;
  font-size: 14px;
}

.title_button{
  float: right;
  margin-right: 20px;
}

.title_button button{
  margin-left: 5px;
  margin-right: 5px;
}

.panel table{
  margin: 0 auto;
  font-size: 15px;
  text-align: center;
  font-family: Arial;
}

.panel td{
  padding-top: 3px;
  padding-bottom: 3px;
  -webkit-text-fill-color: #515a6e;
}

.param th{
  text-align: right;
  padding-right: 30px;
  width: 55%;
}

.param td{
  text-align: left;
  padding-left: 5px;
  width: 45%;
}

.title{
  text-align: left;
  margin: 0 auto;
  padding: 0 auto;
  margin-bottom: 20px;
  margin-top: 20px;
  margin-left: 20%;

}
.title span{
  font-size: 20px;
  font-weight: bold;
  -webkit-text-fill-color: #515a6e;
  border-left: 6px solid rgb(0,101,186);
  border-bottom: 4px solid rgb(252,214,146);
  padding-left: 5px;
  padding-bottom: 5px;
  padding-top: 5px;
}



</style>
