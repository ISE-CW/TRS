<template>
  <div v-bind:style="{width:100+'%',height:window_height+'px'}" style="background:none">
    <div id="back" v-bind:style="{width: 500+'px', height:350+'px', marginTop:(window_height-350)/2+'px'}" style="margin-left: auto;margin-right: auto">
      <div>
        <div class="close" style="float: right;text-align: center" @click="handleClose">
          ×
        </div>
        <div style="width: 100%;height: 80px;margin: 10px">
          <div style="float: left;width: 25%;text-align: right">
            <img src="../assets/logo.png" style="width: 80px">
          </div>
          <div style="float: left">
            <p style="padding-top: 50px;font-weight: bold;font-size: 18px;font-family: 楷体;padding-left: 10px">欢迎注册TRS</p>
          </div>
        </div>
        <Form ref="formCustom" :model="formCustom" :rules="ruleCustom" :label-width="100" style="width: 400px">
          <FormItem prop="user" label="用户名">
            <Input type="text" v-model="formCustom.user" placeholder="用户名/邮箱"></Input>
          </FormItem>
          <FormItem label="密码" prop="passwd">
            <Input type="password" v-model="formCustom.passwd" placeholder="请输入密码"></Input>
          </FormItem>
          <FormItem label="确认密码" prop="passwdCheck">
            <Input type="password" v-model="formCustom.passwdCheck" placeholder="请再次输入密码"></Input>
          </FormItem>
          <FormItem>
            <Button type="error" @click="handleSubmit('formCustom')" style="margin-left: 15px">注册</Button>
          </FormItem>
        </Form>
      </div>
    </div>
  </div>
</template>

<script>
  Vue.use(iview);
  export default {
    name: "Register",
    data () {
      const validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入密码'));
        } else {
          if (this.formCustom.passwdCheck !== '') {
            // 对第二个密码框单独验证
            this.$refs.formCustom.validateField('passwdCheck');
          }
          callback();
        }
      };
      const validatePassCheck = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入确认密码'));
        } else if (value !== this.formCustom.passwd) {
          callback(new Error('两次输入的密码不一致！'));
        } else {
          callback();
        }
      };
      return {
        formCustom: {
          passwd: '',
          passwdCheck: '',
          user:''
        },
        ruleCustom: {
          user: [
            { required: true, message: '请填写用户名', trigger: 'blur' }
          ],
          passwd: [
            { required: true, message: '请填写密码', trigger: 'blur' },
            { validator: validatePass, trigger: 'blur' }
          ],
          passwdCheck: [
            { required: true, message: '请填写确认密码', trigger: 'blur' },
            { validator: validatePassCheck, trigger: 'blur' }
          ],
        },
        window_width:window.innerWidth,
        window_height:window.innerHeight,
        firstPage:true
      }
    },
    methods: {
      handleSubmit(name){
        this.$refs[name].validate((valid) => {
          if (valid) {
            this.$Message.success('测试')
            // let data = new URLSearchParams()
            // data.append('name', this.formCustom.user)
            // data.append('password', this.formCustom.passwd)
            // this.$axios
            //   .post('/register/', data)
            //   .then(function (response) {
            //     console.log(response.data);
            //     if (response.data.status === 1) {
            //       this.$Message.success({
            //         content:'注册成功',
            //         duration:1.5,
            //         onClose:function() {
            //           window.location.href = "/login";
            //         }
            //       });
            //     }else{
            //       this.$Message.error(response.data.msg);
            //       this.formCustom.user = '';
            //       this.formCustom.passwd = '';
            //       this.formCustom.passwdCheck = '';
            //     }
            //   })
            //   .catch(function (error) {
            //     console.log(error)
            //   })
          }
        })
      },
      handleClose(){
        this.$emit('closeFrame','close')
      }
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

  .close{
    font-size: 30px;
  }
  .close:hover{
    -webkit-text-fill-color: rgb(230,73,25);
    cursor: pointer;
  }
  .link{
    -webkit-text-fill-color: #515a6e;
  }
  .link:hover{
    -webkit-text-fill-color: rgb(230,73,25);
    cursor: pointer;
  }
</style>
