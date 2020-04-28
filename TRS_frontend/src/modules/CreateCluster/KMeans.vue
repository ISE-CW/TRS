<template>
    <Form ref="parametersValidate" :model="parameters" :rules="parametersValidate" :label-width="150">
      <FormItem label="n_clusters" prop="n_clusters">
        <InputNumber :min="0" v-model="parameters.n_clusters"></InputNumber>
      </FormItem>
      <FormItem label="init" prop="init">
        <RadioGroup v-model="parameters.init">
          <Radio label="k-means++"></Radio>
          <Radio label="random"></Radio>
        </RadioGroup>
      </FormItem>
      <FormItem label="n_init" prop="n_init">
        <InputNumber :min="1" v-model="parameters.n_init"></InputNumber>
      </FormItem>
      <FormItem label="max_iter" prop="max_iter">
        <InputNumber :min="1" v-model="parameters.max_iter"></InputNumber>
      </FormItem>
      <FormItem label="tol" prop="tol">
        <InputNumber :min="0" v-model="parameters.tol" :step="0.0001"></InputNumber>
      </FormItem>
      <FormItem label="verbose" prop="verbose">
        <InputNumber :min="0" v-model="parameters.verbose"></InputNumber>
      </FormItem>
      <FormItem label="random_state" prop="random_state">
        <InputNumber :min="0" v-model="parameters.random_state" :disabled="random_state_disabled"></InputNumber>
        <Button type="primary" @click="changeRandomState">{{random_state_button_text}}</Button>
      </FormItem>
      <FormItem label="copy_x" prop="copy_x">
        <RadioGroup v-model="parameters.copy_x">
          <Radio label="True"></Radio>
          <Radio label="False"></Radio>
        </RadioGroup>
      </FormItem>
      <FormItem label="n_jobs" prop="n_jobs">
        <InputNumber :min="-1" v-model="parameters.n_jobs" :disabled="n_jobs_disabled"></InputNumber>
        <Button type="primary" @click="changeNJobs">{{n_jobs_button_text}}</Button>
      </FormItem>
      <FormItem label="algorithm" prop="algorithm">
        <RadioGroup v-model="parameters.algorithm">
          <Radio label="auto"></Radio>
          <Radio label="full"></Radio>
          <Radio label="elkan"></Radio>
        </RadioGroup>
      </FormItem>
    </Form>
</template>

<script>
    export default {
        name: "KMeans",
      data(){
        const validateNumber = (rule, value, callback) => {
          if (value==null) {
            return callback(new Error('该选项不能为空'));
          }
          else{
            callback()
          }
        };
          return{
            parameters:{
              n_clusters:0,
              init:'k-means++',
              n_init: 10,
              max_iter : 300,
              tol : 0.0001,
              precompute_distances : 'auto',
              verbose : 0,
              random_state : 'None',
              copy_x : 'True',
              n_jobs : 'None',
              algorithm: 'auto'
            },
            parametersValidate:{
              n_clusters: [
                { validator: validateNumber, trigger: 'blur' }
              ],
              init: [
                { required: true, message: '请选择init', trigger: 'change' }
              ],
              n_init: [
                { validator: validateNumber, trigger: 'blur' }
              ],
              max_iter: [
                { validator: validateNumber, trigger: 'blur' }
              ],
              tol: [
                { validator: validateNumber, trigger: 'blur' }
              ],
              precompute_distances: [
                { required: true, message: '请选择precompute_distances', trigger: 'change' }
              ],
              verbose: [
                { validator: validateNumber, trigger: 'blur' }
              ],
              random_state: [
                { validator: validateNumber, trigger: 'blur' }
              ],
              copy_x: [
                { required: true, message: '请选择copy_x', trigger: 'change' }
              ],
              n_jobs: [
                { validator: validateNumber, trigger: 'blur' }
              ],
              algorithm: [
                { required: true, message: '请选择algorithm', trigger: 'change' }
              ],
            },
            random_state_disabled:'True',
            random_state_button_text:'设置random_state非None',
            n_jobs_disabled:'True',
            n_jobs_button_text:'设置n_jobs非None'
          }
      },
      methods:{
          changeRandomState(){
            if(this.random_state_disabled){
              this.random_state_disabled=!this.random_state_disabled
              this.parameters.random_state=0
              this.random_state_button_text='设置random_sate为None'
            }
            else {
              this.random_state_disabled=!this.random_state_disabled
              this.parameters.random_state='None'
              this.random_state_button_text='设置random_sate非None'
            }
          },

          changeNJobs(){
            if(this.n_jobs_disabled){
              this.n_jobs_disabled=!this.n_jobs_disabled
              this.parameters.n_jobs=1
              this.n_jobs_button_text='设置n_jobs为None'
            }
            else{
              this.n_jobs_disabled=!this.n_jobs_disabled
              this.parameters.n_jobs='None'
              this.n_jobs_button_text='设置n_jobs非None'
            }
          },
      }
    }
</script>

<style scoped>

</style>
