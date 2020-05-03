<template>
    <v-row>
        <v-col>
            <h2>Artifacts Produced</h2>
            <v-data-table v-if="artifactItems" :headers="headers" :items=artifactItems :items-per-page=5></v-data-table>
        </v-col>
        <v-col>
            <h2>Project Dependencies</h2>
            <v-data-table v-if="dependenciesItems" :headers="headers" :items="dependenciesItems" :items-per-page=5></v-data-table>
        </v-col>
    </v-row>
</template>

<script>
    export default {
        name: "BasicInfo",
        created: async function () {
            const response = await fetch(
                this.api_url+'/project/'+this.analysedProject+'/artifacts',
                {
                    method: 'GET'
                }
            )
            const stats = await response.json()
            this.artifactItems = stats["packages"]

            const responseCalls = await fetch(
                this.api_url+'/project/'+this.analysedProject+'/dependencies',
                {
                    method: 'GET'
                }
            )
            const statsCalls = await responseCalls.json()
            this.dependenciesItems = statsCalls["artifacts"]
        },
        data: function () {
            return {
                headers: [
                    {
                        text: 'Group ID',
                        align: 'start',
                        sortable: true,
                        value: 'group',
                    },
                    {
                        text: 'Artifact ID',
                        sortable: true,
                        value: 'artifact'
                    }],
                artifactItems: null,
                dependenciesItems: null,
            }
        },
        computed: {
            analysedProject: function() {
                return this.$route.params.group + '/' + this.$route.params.project
            }
        }
    }
</script>