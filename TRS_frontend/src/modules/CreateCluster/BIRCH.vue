<template>
  <Form ref="parametersValidate" :model="parameters" :rules="parametersValidate" :label-width="150">
    <FormItem label="threshold" prop="threshold">
      <InputNumber :min="0" v-model="parameters.threshold" :step="0.0001"></InputNumber>
    </FormItem>
    <FormItem label="branching_factor" prop="branching_factor">
      <InputNumber :min="1" v-model="parameters.branching_factor"></InputNumber>
    </FormItem>
    <FormItem label="n_clusters" prop="n_clusters">
      <InputNumber :min="1" v-model="parameters.n_clusters" :disabled="n_clusters_disabled"></InputNumber>
      <Button type="primary" @click="changeNClusters">{{n_clusters_button_text}}</Button>
    </FormItem>
    <FormItem label="compute_labels" prop="compute_labels">
      <RadioGroup v-model="parameters.compute_labels">
        <Radio label="True"></Radio>
        <Radio label="False"></Radio>
      </RadioGroup>
    </FormItem>
    <FormItem label="copy" prop="copy">
      <RadioGroup v-model="parameters.copy">
        <Radio label="True"></Radio>
        <Radio label="False"></Radio>
      </RadioGroup>
    </FormItem>
  </Form>
</template>

<script>
    export default {
        name: "BIRCH",
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
              threshold : 0,
              branching_factor : 0,
              n_clusters : 'None',
              compute_labels : 'True',
              copy : 'True',
            },
            parametersValidate:{
              threshold: [
                { validator: validateNumber, trigger: 'blur' }
              ],
              branching_factor: [
                { validator: validateNumber, trigger: 'blur' }
              ],
              n_clusters: [
                { validator: validateNumber, trigger: 'blur' }
              ],
              compute_labels: [
                { required: true, message: '请选择compute_labels', trigger: 'change' }
              ],
              copy: [
                { required: true, message: '请选择copy', trigger: 'change' }
              ],
            },
            n_clusters_disabled:'True',
            n_clusters_button_text:'设置n_clusters非None'
          }
      },
      methods:{
          changeNClusters(){
            if(this.n_clusters_disabled){
              this.n_clusters_disabled=!this.n_clusters_disabled
              this.parameters.n_clusters=1
              this.n_clusters_button_text='设置n_clusters为None'
            }
            else {
              this.n_clusters_disabled=!this.n_clusters_disabled
              this.parameters.n_clusters='None'
              this.n_clusters_button_text='设置n_clusters非None'
            }
          },
      }
    }
</script>

<style scoped>

</style>
