<template>
  <Card class="card">
    <div class="title"><span>选择聚类数据</span></div>
    <Form ref="inputValidate" :model="input" :rules="inputValidate" :label-width="150">
      <FormItem label="聚类输入数据" prop="relevant_data">
        <CheckboxGroup v-model="input.relevant_data">
          <Checkbox label="复现步骤"></Checkbox>
          <Checkbox label="问题控件"></Checkbox>
          <Checkbox label="故障类型"></Checkbox>
          <Checkbox label="错误控件截图"></Checkbox>
          <Checkbox label="其他控件截图"></Checkbox>
        </CheckboxGroup>
      </FormItem>
      <FormItem label="选择图片降维方式" prop="reduction">
        <RadioGroup v-model="input.reduction">
          <Radio label="均值降维"></Radio>
          <Radio label="PCA降维"></Radio>
        </RadioGroup>
      </FormItem>
    </Form>

    <div class="title"><span>配置聚类算法</span></div>
    <Form ref="algorithmValidate" :model="algorithm" :rules="algorithmValidate" :label-width="150">
      <FormItem label="聚类算法" prop="algorithm_chosen">
        <RadioGroup v-model="algorithm.algorithm_chosen">
          <Radio label="KMeans"></Radio>
          <Radio label="BIRCH"></Radio>
          <Radio label="DBSCAN"></Radio>
          <Radio label="GMM"></Radio>
        </RadioGroup>
      </FormItem>
    </Form>

    <BIRCH v-if="algorithm.algorithm_chosen=='BIRCH'" ref="birch"></BIRCH>
    <DBSCAN v-if="algorithm.algorithm_chosen=='DBSCAN'" ref="dbscan"></DBSCAN>
    <GMM v-if="algorithm.algorithm_chosen=='GMM'" ref="gmm"></GMM>
    <KMeans v-if="algorithm.algorithm_chosen=='KMeans'" ref="kmeans"></KMeans>
  </Card>
</template>

<script>
  import BIRCH from './BIRCH'
  import DBSCAN from './DBSCAN'
  import GMM from './GMM'
  import KMeans from './KMeans'
    export default {
        name: "Level",
      components: {KMeans, GMM, DBSCAN, BIRCH},
      comments:{BIRCH,DBSCAN,GMM,KMeans},
      data () {
        return {
          input: {
            relevant_data: [],
            reduction:'',
          },
          inputValidate: {
            relevant_data: [
              { required: true, type: 'array', min: 1, message: '至少选择一项相关数据', trigger: 'change' },
            ],
            reduction: [
              { required: true, message: '请选择图片降维方式', trigger: 'change' }
            ],
          },
          algorithm:{
            algorithm_chosen:''
          },
          algorithmValidate:{
            algorithm_chosen: [
              { required: true, message: '请选择聚类算法', trigger: 'change' }
            ],
          },
          isValid:false
        }
      },
      methods: {
        async handleSubmit () {
          var isValid=true
          var refs=['inputValidate','algorithmValidate']
          for(var i=0;i<refs.length;i++){
            var ref_item=refs[i]
            await this.$refs[ref_item].validate((valid)=>{
              if(!valid){
                isValid=false
              }
            })
          }
          if (this.algorithm.algorithm_chosen=='BIRCH'){
            await this.$refs.birch.$refs['parametersValidate'].validate((valid)=>{
              if(!valid){
                isValid=false
              }
            })
          }
          else if(this.algorithm.algorithm_chosen=='DBSCAN'){
            await this.$refs.dbscan.$refs['parametersValidate'].validate((valid)=>{
              if(!valid){
                isValid=false
              }
            })
          }
          else if(this.algorithm.algorithm_chosen=='GMM'){
            await this.$refs.gmm.$refs['parametersValidate'].validate((valid)=>{
              if(!valid){
                isValid=false
              }
            })
          }
          else if(this.algorithm.algorithm_chosen=='KMeans'){
            await this.$refs.kmeans.$refs['parametersValidate'].validate((valid)=>{
              if(!valid){
                isValid=false
              }
            })
          }
          this.isValid=isValid
        },
        getChoice(){
          var choice={}
          choice['relevant_data']=this.input.relevant_data
          choice['reduction']=this.input.reduction
          choice['algorithm_chosen']=this.algorithm.algorithm_chosen
          if (this.algorithm.algorithm_chosen=='BIRCH'){
            var parameters={}
            for(var key in this.$refs.birch.parameters){
              parameters[key]=this.$refs.birch.parameters[key]
            }
            choice['parameters']=parameters
          }
          else if(this.algorithm.algorithm_chosen=='DBSCAN'){
            var parameters={}
            for(var key in this.$refs.dbscan.parameters){
              parameters[key]=this.$refs.dbscan.parameters[key]
            }
            choice['parameters']=parameters
          }
          else if(this.algorithm.algorithm_chosen=='GMM'){
            var parameters={}
            for(var key in this.$refs.gmm.parameters){
              parameters[key]=this.$refs.gmm.parameters[key]
            }
            choice['parameters']=parameters
          }
          else if(this.algorithm.algorithm_chosen=='KMeans'){
            var parameters={}
            for(var key in this.$refs.kmeans.parameters){
              parameters[key]=this.$refs.kmeans.parameters[key]
            }
            choice['parameters']=parameters
          }

          console.log(choice)
          return choice
        }
      }
    }
</script>

<style scoped>
  .title{
    text-align: left;
    margin: 0 auto;
    padding: 0 auto;
    margin-bottom: 20px;
    margin-top: 20px;

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
