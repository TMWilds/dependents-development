<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >

      <h1>dependents.dev</h1>

      <v-spacer></v-spacer>

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
};
</script>
