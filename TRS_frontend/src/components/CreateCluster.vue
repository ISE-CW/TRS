<template>
    <div style="text-align: left">
      <Top ref="top"></Top>

      <ButtonGroup style="margin-top: 20px;margin-bottom: 20px">
        <Button type="warning" :size="'large'" style="width: 150px" @click="createLevels">
          新建聚类层次
        </Button>
        <Button type="success" :size="'large'" style="width: 150px" @click="finishConfiguration">
          完成聚类配置
        </Button>
      </ButtonGroup>

      <Collapse simple class="collapse" :value="page">
        <Panel v-for="(item,index) in levels" :key="item" class="panel" :name="item+''">
          <span class="title">聚类层次 {{index+1}}</span>
          <span class="delete" @click="deleteLevel(index)">删除</span>
          <Level :ref="getRefName(item)" slot="content"></Level>
        </Panel>
      </Collapse>
    </div>
</template>

<script>
  import Top from './Top'
  import Level from '../modules/CreateCluster/Level'
    export default {
        name: "CreateCluster",
      components: {Top,Level},
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
            levels:[1],
            page:[1],
          }
      },
      methods:{
          createLevels(){
            var new_value=this.levels[this.levels.length-1]+1
            this.levels.push(new_value)
            this.page=[new_value]
          },
        deleteLevel(index){
            this.levels.splice(index,1)
        },
        getRefName(name){
            return 'Level'+name
        },
        async finishConfiguration(){
            var invalid_config=[]
            for(var i=0;i<this.levels.length;i++){
              var name='Level'+this.levels[i]
              await this.$refs[name][0].handleSubmit()
              if(!this.$refs[name][0].isValid){
                invalid_config.push(this.levels[i])
              }
            }
            //成功
            if(invalid_config.length==0){
              let data = new URLSearchParams();
              data.append('sid', sessionStorage.getItem("sid"));
              data.append('choices',JSON.stringify(this.getChoices()))
              this.$axios.post('/server/createCluster/',data).then(re=>{})
              this.$Message.success('成功配置聚类信息')
              this.$router.push('/show')
            }
            //失败
          else{
            this.$Message.error('您有信息未填写完整')
              this.page=invalid_config
            }
        },
        getChoices(){
            var choices=[]
            for(var i=0;i<this.levels.length;i++){
              var name=this.getRefName(this.levels[i])
              var choice=this.$refs[name][0].getChoice()
              choices.push(choice)
            }
            return choices
        }
      }
    }
</script>

<style scoped>
  .collapse{
    margin-left: 10%;
    margin-right: 10%;
  }

  .title{
    font-size: 15px;
    padding: 5px;
    background-color: rgb(0,101,186);
    -webkit-text-fill-color: white;
    border-radius: 10px;
  }

  .delete{
    -webkit-text-fill-color: #ed4014;
    background-color: white;
    border: 1px solid #ed4014;
    padding: 5px;
    font-size: 14px;
    border-radius: 10px;
    margin-left: 15px;
  }

  .delete:hover{
    background-color: #ed4014;
    -webkit-text-fill-color: white;
  }

</style>
