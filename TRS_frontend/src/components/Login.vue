<template>
    <div>
      <Button type="primary" @click="test">测试</Button>
    </div>
</template>

<script>
    export default {
        name: "Login",
      methods:{
          test(){
            let data = new URLSearchParams()
            data.append('parm','前端传入数据示例')
            this.$axios
              .post('/server/test/', data)
              .then(function (response) {
                console.log(response)
                alert(response.data.msg)
                if (response.data.status === 0) {
                  location.href = '/'
                }
              })
              .catch(function (error) {
                console.log(error)
              })
            this.$Message.success('成功')
          }
      }
    }
</script>

<style scoped>

</style>
