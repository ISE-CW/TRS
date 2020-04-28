// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import iView from 'iview'
import 'iview/dist/styles/iview.css'
import axios from 'axios'
import ElementUI from 'element-ui';     //引入element库
import 'element-ui/lib/theme-chalk/index.css';        //引入element的css
import './assets/iconfont/iconfont.css';
import $ from 'jquery';
import mavonEditor from 'mavon-editor'
import 'mavon-editor/dist/css/index.css'

Vue.prototype.$axios = axios
axios.defaults.withCredentials = false

Vue.config.productionTip = false
Vue.use(iView)
Vue.use(ElementUI)

Vue.use(mavonEditor)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
