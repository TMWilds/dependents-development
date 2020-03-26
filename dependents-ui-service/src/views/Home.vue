<template>
    <v-container>
        <h1> Select Project to Analyse</h1>
        <div class="home">
            <v-row>
                <v-col sm="5">
                    <v-text-field  placeholder="jhy"
                                  disabled
                                  @keypress.enter="show"
                                  color="primary"
                                  label="Project Owner"
                                  v-model="group">

                        <template v-slot:prepend>
                            github.com/

                        </template>

                    </v-text-field>
                </v-col>
                <v-col sm="5">
                    <v-text-field placeholder="jsoup"
                                  disabled
                                  value="jsoup"
                                  @keypress.enter="show"
                                  color="primary"
                                  label="Project Name"
                                  v-model="project">

                        <template v-slot:prepend>
                            /

                        </template>

                        <template v-slot:append>

                        </template>

                    </v-text-field>
                </v-col>
                <v-col sm="2">
                     <v-btn
                                    depressed
                                    tile
                                    color="primary"
                                    class="ma-0"
                                    :to="'/dependents/analysis/'+group+'/'+project">

                                show

                            </v-btn>
                </v-col>
            </v-row>
            <router-link to="/dependents/analysis">Link</router-link>
        </div>
    </v-container>
</template>

<script>

    export default {
        name: 'Home',
        data: function () {
            return {
                group: 'jhy',
                project: 'jsoup'
            }
        }
    }
</script>
