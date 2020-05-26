<template>
  <Form ref="parametersValidate" :model="parameters" :rules="parametersValidate" :label-width="150">
    <FormItem label="n_components" prop="n_components">
      <InputNumber :min="0" v-model="parameters.n_components"></InputNumber>
    </FormItem>
    <FormItem label="covariance_type" prop="covariance_type">
      <RadioGroup v-model="parameters.covariance_type">
        <Radio label="full"></Radio>
        <Radio label="tied"></Radio>
        <Radio label="diag"></Radio>
        <Radio label="spherical"></Radio>
      </RadioGroup>
    </FormItem>
    <FormItem label="tol" prop="tol">
      <InputNumber :min="0.00001" v-model="parameters.tol" :step="0.00001"></InputNumber>
    </FormItem>
    <FormItem label="reg_covar" prop="reg_covar">
      <InputNumber :min="0.000000001" v-model="parameters.reg_covar" :step="0.000000001"></InputNumber>
    </FormItem>
    <FormItem label="max_iter" prop="max_iter">
      <InputNumber :min="1" v-model="parameters.max_iter"></InputNumber>
    </FormItem>
    <FormItem label="n_init" prop="n_init">
      <InputNumber :min="1" v-model="parameters.n_init"></InputNumber>
    </FormItem>
    <FormItem label="init_params" prop="init_params">
      <RadioGroup v-model="parameters.init_params">
        <Radio label="kmeans"></Radio>
        <Radio label="random"></Radio>
      </RadioGroup>
    </FormItem>
    <FormItem label="random_state" prop="random_state">
      <InputNumber :min="0" v-model="parameters.random_state" :disabled="random_state_disabled"></InputNumber>
      <Button type="primary" @click="changeRandomState">{{random_state_button_text}}</Button>
    </FormItem>
    <FormItem label="warm_start" prop="warm_start">
      <RadioGroup v-model="parameters.warm_start">
        <Radio label="True"></Radio>
        <Radio label="False"></Radio>
      </RadioGroup>
    </FormItem>
    <FormItem label="verbose" prop="verbose">
      <InputNumber :min="0" v-model="parameters.verbose"></InputNumber>
    </FormItem>
    <FormItem label="verbose_interval" prop="verbose_interval">
      <InputNumber :min="1" v-model="parameters.verbose_interval"></InputNumber>
    </FormItem>
  </Form>
</template>

<script>
    export default {
        name: "GMM",
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
              n_components : 0,
              covariance_type : 'full',
              tol : 1e-3,
              reg_covar : 1e-6,
              max_iter : 100,
              n_init :1,
              init_params : 'random',
              weights_init : 'None',
              means_init : 'None',
              precisions_init : 'None',
              random_state : 'None',
              warm_start : 'False',
              verbose : 0,
              verbose_interval : 10
            },
            parametersValidate:{
              n_components: [
                { validator: validateNumber, trigger: 'blur' }
              ],
              covariance_type: [
                { required: true, message: 'please select covariance_type', trigger: 'change' }
              ],
              tol: [
                { validator: validateNumber, trigger: 'blur' }
              ],
              reg_covar: [
                { validator: validateNumber, trigger: 'blur' }
              ],
              max_iter: [
                { validator: validateNumber, trigger: 'blur' }
              ],
              n_init: [
                { validator: validateNumber, trigger: 'blur' }
              ],
              init_params: [
                { required: true, message: 'please select init_params', trigger: 'change' }
              ],
              random_state: [
                { validator: validateNumber, trigger: 'blur' }
              ],
              warm_start: [
                { required: true, message: 'please select warm_start', trigger: 'change' }
              ],
              verbose: [
                { validator: validateNumber, trigger: 'blur' }
              ],
              verbose_interval: [
                { validator: validateNumber, trigger: 'blur' }
              ],
            },
            random_state_disabled:'True',
            random_state_button_text:'set random_state not None',
          }
      },
      methods:{
        changeRandomState(){
          if(this.random_state_disabled){
            this.random_state_disabled=!this.random_state_disabled
            this.parameters.random_state=0
            this.random_state_button_text='set random_state None'
          }
          else {
            this.random_state_disabled=!this.random_state_disabled
            this.parameters.random_state='None'
            this.random_state_button_text='set random_state not None'
          }
        },
      }
    }
</script>

<style scoped>

</style>
