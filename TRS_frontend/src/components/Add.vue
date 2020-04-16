<!--
  添加博文组件
  TODO: 开发添加博文的功能
-->
<template>
  <div class="container">
    <div class="main">
      <!--<h1 class="display-3">Add</h1>-->
      <hr class="my-1">

      <form class="main-form">
        <label for="name">Title:</label>
        <input type="text" class="form-control" id="name" placeholder="Title" v-model="name">
        <label for="content">Content:</label>
        <textarea class="form-control" id="content" rows="10" placeholder="Content" v-model="content"></textarea>
        <input type="button" class="btn btn-secondary" value="Submit" @click="post">
        <Button type="primary" @click="test">测试</Button>
      </form>

    </div>
  </div>
</template>

<script>
  export default {
    name: 'Add',
    data() {
      return {
        'name': '',
        'content': ''
      }
    },
    mounted () {
      // let allCookies = document.cookie
      // if (allCookies.indexOf('username') === -1) {
      //   this.$router.push('/login')
      // }
    },
    methods: {
      post() {
        let data = new URLSearchParams()
        data.append('parm','前端传入数据示例')
        this.$axios
          .post('/server/test/', data)
          .then(re=>{
            console.log(re);
            this.$Message.success(re.data.msg);
            if (re.data.status === 0) {
              location.href = '/'
            }
          })
          .catch(function (error) {
            console.log(error)
          })
      },
      test(){
        this.$Message.info('测试')
      }
    }
  }
</script>

<style scoped>

  .main {
    /*padding-top: 100px;*/
  }

  label {
    font-size: 1.5em;
    margin: 15px 0 0 0;
  }

  .main-form {
    margin-top: 20px;
  }

  .btn {
    margin-top: 15px;
  }
</style>
