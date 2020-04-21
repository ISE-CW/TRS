import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Add from '@/components/Add'
import Login from '@/components/Login'
import Register from "@/components/Register";
import Home from "../components/Home";
import FeatureShow from "../components/FeatureShow";
Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/add',
      name: 'Add',
      component: Add
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/register',
      name: 'Register',
      component: Register
    },
    {
      path: '/home',
      name: 'Home',
      component: Home
    },
    {
      path: '/feature',
      name: 'FeatureShow',
      component: FeatureShow
    }
  ]
})
