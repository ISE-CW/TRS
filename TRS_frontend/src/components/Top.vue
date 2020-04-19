<template>
  <div>
    <div style="height: 80px;width: 100%;background: white;box-shadow: #dcdee2 0px 0px 5px 1px">
      <div id="logo" style="width: 10%;float: left;text-align: left">
        <img src="../assets/logo.png" style="height: 80px">
      </div>
      <span style="font-size: 2em;position: absolute;left: 10%;padding-top: 15px">移动应用众包测试报告选择系统</span>
      <div v-if="login" style="float: right;padding-top: 20px;width: 200px;text-align: right;margin-right: 5%">
        <Avatar icon="ios-person" size="large"/><span style="font-size: 15px;">&nbsp&nbsp{{username}}</span>
        <p id="out_frame" style="display: inline;margin-left: 15px" @click="logout"><Icon type="md-exit" size="25" id="out"/><span style="font-size: 15px">&nbsp登出</span></p>
      </div>
      <div v-else style="float: right;padding-top: 20px;width: 120px;text-align: right;margin-right: 5%">
        <button class="login" @click="toLogin">登录</button>
        <button class="login" @click="toRegister">注册</button>
      </div>
    </div>
  </div>
</template>

<script>
    export default {
      name: "Top",
      mounted(){
        var username=sessionStorage.getItem("username")
        if(username==null || username===''){
          this.login=false
        }
        else{
          this.username=username;
          this.login=true;
        }
      },
      data(){
        return{
          username:'',
          login:'',
        }
      },
      methods:{
        logout(){
          this.$Message.info({
            content:'登出成功',
            duration:1.5,
            onClose:function() {
              sessionStorage.setItem("username",'');
              sessionStorage.setItem("user_id",'');
              window.location.href = "/#/login";
            }
          });
        },
        toLogin(){
          window.location.href = "/#/login";
        },
        toRegister(){
          window.location.href = "/#/register";
        }
      },
      props:['frame']
    }
</script>

<style scoped>
  #out:hover{
    color: #e64919;
  }

  #out_frame:hover{
    cursor: pointer;
    -webkit-text-fill-color: #e64919;
  }
  .menu_default{
    font-size: 18px;
    font-weight: bold;
    -webkit-text-fill-color: #17233d;
    border: #FFFFFF solid 3px;
  }
  .menu_default:hover{
    -webkit-text-fill-color: #e64919;
    border: rgba(230,73,25,0.5) solid 3px;
  }
  .menu_default:focus{
    -webkit-text-fill-color: #e64919;
    border: rgba(230,73,25,0.5) solid 3px;
  }

  .menu_active{
    font-size: 18px;
    font-weight: bold;
    -webkit-text-fill-color: #e64919;
    border: #FFFFFF solid 3px;
  }
  .menu_active:hover{
    -webkit-text-fill-color: #e64919;
    border: rgba(230,73,25,0.5) solid 3px;
  }
  .menu_active:focus{
    -webkit-text-fill-color: #e64919;
    border: rgba(230,73,25,0.5) solid 3px;
  }

  .login{
    background: none;
    border: 1px solid rgba(230,73,25,0.5);
    -webkit-text-fill-color: rgba(230,73,25,0.5);
    font-size: 15px;
    padding: 2px;
    border-radius: 15px;
    width: 50px;
    outline: none;
  }

  .login:hover{
    /*border: 2px solid rgba(230,73,25,0.5);*/
    /*-webkit-text-fill-color: rgba(230,73,25,0.5);*/
    background-color: rgba(230,73,25,0.5);
    -webkit-text-fill-color: #ffffff;
    font-weight: bold;
  }
</style>
