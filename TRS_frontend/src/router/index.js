import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Add from '@/components/Add'
import Login from '@/components/Login'
import Register from "@/components/Register";
import Home from "../components/Home";
import FeatureShow from "../components/FeatureShow";
import CreateCluster from "../components/CreateCluster"
import ShowClusters from "../components/ShowClusters"
import CheckFile from "../components/CheckFile"
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
    },
    {
      path:'/create',
      name:'CreateCluster',
      component:CreateCluster
    },
    {
      path:'/show',
      name:'ShowClusters',
      component:ShowClusters
    },
    {
      path:'/check',
      name:'CheckFile',
      component:CheckFile
    }
  ]
})
