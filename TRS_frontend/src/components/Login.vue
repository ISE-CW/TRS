<template>
  <div v-bind:style="{width:100+'%',height:window_height+'px'}" style="background: #f4f4f4">
    <Top ref="top"></Top>
    <div id="back" v-bind:style="{width: 500+'px', height:350+'px', marginTop:(window_height-350)/2+'px'}" style="margin-left: auto;margin-right: auto">
      <div id="close" style="float: right;text-align: center" @click="handleClose('close')">
        ×
      </div>
      <div style="width: 100%;height: 80px;margin: 10px">
        <div style="float: left;width: 25%;text-align: right">
          <img src="../assets/logo.png" style="width: 80px">
        </div>
        <div style="float: left">
          <p style="padding-top: 50px;font-weight: bold;font-size: 18px;font-family: 楷体;padding-left: 10px">欢迎登录TRS</p>
        </div>
      </div>
      <Form ref="formInline" :model="formInline" :rules="ruleInline" :label-width="100" style="width: 400px">
        <FormItem prop="user" label="用户名">
          <Input type="text" v-model="formInline.user" placeholder="用户名/邮箱"></Input>
        </FormItem>
        <FormItem prop="password" label="密码">
          <Input type="password" v-model="formInline.password" placeholder="请输入您的密码"></Input>
        </FormItem>
        <FormItem style="text-align: right">
          <a class="link" href="">忘记密码</a>
          <Divider type="vertical"></Divider>
          <a class="link" href="/#/register">注册用户</a>
          <Button type="error" @click="handleSubmit('formInline')" style="margin-left: 15px">登 录</Button>
        </FormItem>
      </Form>
    </div>
  </div>
</template>

<script>
  import Top from './Top'
  export default {
    name: "Login",
    components: {Top},
    data () {
      return {
        formInline: {
          user: '',
          password: ''
        },
        ruleInline: {
          user: [
            { required: true, message: '请填写用户名', trigger: 'blur' }
          ],
          password: [
            { required: true, message: '请填写密码', trigger: 'blur' },
          ]
        },
        window_width:window.innerWidth,
        window_height:window.innerHeight
      }
    },
    methods: {
      handleSubmit(name) {
        this.$refs[name].validate((valid) => {
          if (valid) {
            let data = new URLSearchParams();
            data.append('name', this.formInline.user);
            data.append('password', this.formInline.password);
            this.$axios
              .post('/server/login/', data)
              .then(re=>{
                if (re.data.status === 1) {
                  sessionStorage.setItem("username",this.formInline.user);
                  sessionStorage.setItem("user_id",re.data.msg);
                  this.$Message.success({
                    content:'登录成功',
                    onClose:function() {
                      window.location.href = "/#/home";
                    }
                  });
                }else{
                  this.$Message.error(re.data.msg);
                  this.formInline.password=''
                }
              })
              .catch(function (error) {
                console.log(error)
              });
          }
        })
      },
      handleClose(para){
        this.$emit('closeFrame',para)
      },
    },
    props:['close_frame']
  }
</script>

<style scoped>
  #back{
    background-color: rgba(255,255,255,0.8);
    padding: 20px;
    box-shadow: #dcdee2 0px 0px 5px 1px
  }

  #close{
    font-size: 30px;
  }
  #close:hover{
    -webkit-text-fill-color: rgb(39, 54, 230);
    cursor: pointer;
  }
  .link{
    -webkit-text-fill-color: #515a6e;
  }
  .link:hover{
    -webkit-text-fill-color: rgb(39, 54, 230);
    cursor: pointer;
  }
</style>
