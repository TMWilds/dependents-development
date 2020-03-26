<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >

      <router-link to="/"><h1 style="color: white">dependents.dev</h1></router-link>
      <h3 style="margin-left: 1rem"> Software Dependency Analysis</h3>
            <v-spacer></v-spacer>

      <span v-if="analysedProject" style="margin-right: 5rem">
        <h2>{{ analysedProject }}</h2>
      </span>


    </v-app-bar>

    <v-content>
      <router-view/>
    </v-content>
  </v-app>
</template>

<script>
import HelloWorld from './components/HelloWorld';

export default {
  name: 'App',

  components: {
    HelloWorld,
  },

  data: () => ({
    //
  }),
  computed: {
    analysedProject: function () {
      if (this.$route.params.group && this.$route.params.project){
        return this.$route.params.group + '/' + this.$route.params.project
      }
      return null
    }
  }
};
</script>
