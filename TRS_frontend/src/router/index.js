import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Add from '@/components/Add'
import Login from '@/components/Login'

Vue.use(Router)

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
    }
  ]
})
