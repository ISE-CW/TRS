<template>
  <Form ref="parametersValidate" :model="parameters" :rules="parametersValidate" :label-width="150">
    <FormItem label="eps" prop="eps">
      <InputNumber :min="0" v-model="parameters.eps" :step="0.0001"></InputNumber>
    </FormItem>
    <FormItem label="min_samples" prop="min_samples">
      <InputNumber :min="1" v-model="parameters.min_samples"></InputNumber>
    </FormItem>
    <FormItem label="metric" prop="metric">
      <RadioGroup v-model="parameters.metric">
        <Radio label="cityblock"></Radio>
        <Radio label="cosine"></Radio>
        <Radio label="euclidean"></Radio>
        <Radio label="l1"></Radio>
        <Radio label="l2"></Radio>
        <Radio label="manhattan"></Radio>
      </RadioGroup>
    </FormItem>
    <FormItem label="algorithm" prop="algorithm">
      <RadioGroup v-model="parameters.algorithm">
        <Radio label="auto"></Radio>
        <Radio label="ball_tree"></Radio>
        <Radio label="kd_tree"></Radio>
        <Radio label="brute"></Radio>
      </RadioGroup>
    </FormItem>
    <FormItem label="leaf_size" prop="leaf_size">
      <InputNumber :min="1" v-model="parameters.leaf_size"></InputNumber>
    </FormItem>
    <FormItem label="p" prop="p">
      <InputNumber :min="0.0001" v-model="parameters.p" :step="0.0001" :disabled="p_disabled"></InputNumber>
      <Button type="primary" @click="changeP">{{p_button_text}}</Button>
    </FormItem>
    <FormItem label="n_jobs" prop="n_jobs">
      <InputNumber :min="-1" v-model="parameters.n_jobs" :disabled="n_jobs_disabled"></InputNumber>
      <Button type="primary" @click="changeNJobs">{{n_jobs_button_text}}</Button>
    </FormItem>
  </Form>
</template>

<script>
    export default {
        name: "DBSCAN",
      data(){
        const validateNumber = (rule, value, callback) => {
          if (value==null) {
            return callback(new Error('The option can not be empty.'));
          }
          else{
            callback()
          }
        };
          return{
            parameters:{
              eps : 0,
              min_samples : 0,
              metric : 'euclidean',
              metric_params : 'None',
              algorithm : 'auto',
              leaf_size : 30,
              p : 'None',
              n_jobs : 'None',
            },
            parametersValidate:{
              eps: [
                { validator: validateNumber, trigger: 'blur' }
              ],
              min_samples: [
                { validator: validateNumber, trigger: 'blur' }
              ],
              metric: [
                { required: true, message: 'please select metric', trigger: 'change' }
              ],
              algorithm: [
                { required: true, message: 'please select algorithm', trigger: 'change' }
              ],
              leaf_size: [
                { validator: validateNumber, trigger: 'blur' }
              ],
              p: [
                { validator: validateNumber, trigger: 'blur' }
              ],
              n_jobs: [
                { validator: validateNumber, trigger: 'blur' }
              ],
            },
            n_jobs_disabled:'True',
            n_jobs_button_text:'set n_jobs not None',
            p_disabled:'True',
            p_button_text:'set p None'
          }
      },
      methods:{
          changeNJobs(){
            if(this.n_jobs_disabled){
              this.n_jobs_disabled=!this.n_jobs_disabled
              this.parameters.n_jobs=1
              this.n_jobs_button_text='set n_jobs None'
            }
            else{
              this.n_jobs_disabled=!this.n_jobs_disabled
              this.parameters.n_jobs='None'
              this.n_jobs_button_text='set n_jobs not None'
            }
          },
        changeP(){
          if(this.p_disabled){
            this.p_disabled=!this.p_disabled
            this.parameters.p=1
            this.p_button_text='set p None'
          }
          else{
            this.p_disabled=!this.p_disabled
            this.parameters.p='None'
            this.p_button_text='set p not None'
          }
        },
      }
    }
</script>

<style scoped>

</style>
