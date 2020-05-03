import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify';

Vue.config.productionTip = false

Vue.mixin ({
  data: function() {
    return {
      get api_url() {
        return window.location.protocol + '//' + window.location.hostname + ':' +  window.location.port + '/api/v1';
        // return "http://localhost:8080/api/v1";
      },
    }
  }
});

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app');