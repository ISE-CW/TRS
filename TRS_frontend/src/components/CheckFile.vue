<template>
  <div>
    <mavon-editor
      class="md"
      :value="value"
      :subfield="false"
      :defaultOpen="'preview'"
      :toolbarsFlag="false"
      :editable="false"
      :scrollStyle="true"
      :ishljs="true"
    ></mavon-editor>
  </div>
</template>

<script>
    export default {
        name: "CheckFile",
      beforeCreate(){
          var username=sessionStorage.getItem("username")
        if(username==null){
          this.$router.push('/login')
        }
        var check_num=sessionStorage.getItem("srid")
        if(check_num==null){
          this.$router.push('/home')
        }
      },
      mounted(){
        let data=new URLSearchParams()
        data.append('srid',sessionStorage.getItem("srid"))
        data.append('format','markdown')
        this.$axios.post('/server/previewFile/',data).then(re=>{
          this.value=re.data.result
        })
      },
      data() {
        return {
          value: '' // markdown语法
        };
      },
    }
</script>

<style scoped>
.md{
  width: 60%;
  margin-left: 20%;
}
</style>
