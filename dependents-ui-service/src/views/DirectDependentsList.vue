<template>
    <div>
        <h2>Direct Dependents</h2>
        <h4>Initiate call graph generation for dependent projects, or explore a another project's dependents.</h4>
        <v-row>
            <v-col offset-md="6">
                            <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
      ></v-text-field>
            </v-col>
        </v-row>
        <v-row>
            <v-data-table v-on:current-items="fetchItemData" v-if="items" :headers="headers" :items="items" style="width: 100%" :search="search" :items-per-page=10>
                <template v-slot:item.state="{item}">
                    <a v-if="item.state === 'Initiate Generation'" @click="parseASTOfProject(item)">Initiate
                        Generation</a>
                    <span v-else> {{item.state}} </span>
                </template>
                <template v-slot:item.explore="{item}">
                    <router-link :to="'/dependents/parsing/'+item.github_short_url">Explore Project</router-link>
                </template>
            </v-data-table>
        </v-row>
    </div>
</template>

<script>
    export default {
        name: "DirectDependentsList",
        created: async function () {
            const response = await fetch(
                this.api_url + '/project/' + this.analysedProject + '/dependents',
                {
                    method: 'GET'
                }
            )
            const projects = await response.json()
            this.items = projects["projects-search"]["projects"]
        },
        data: function () {
            return {
                headers: [
                    {
                        text: 'Project Name',
                        align: 'start',
                        sortable: true,
                        value: 'github_short_url',
                    },
                    {
                        text: 'Total Dependents',
                        sortable: true,
                        value: 'dependents'
                    },
                    {
                        text: 'Call Graph',
                        sortable: true,
                        value: 'state'
                    },
                    {
                        text: 'Explore Project',
                        sortable: true,
                        value: 'explore'
                    }],
                items: null,
                projectDetails: {},
                search: ''
            }
        },
        computed: {
            analysedProject: function () {
                return this.$route.params.group + '/' + this.$route.params.project
            }
        },
        methods: {
            getDependentsCount: async function (project) {
                const responseCalls = await fetch(
                    this.api_url + '/project/' + project + '/dependents',
                    {
                        method: 'GET'
                    }
                )
                const statsCalls = await responseCalls.json()
                return statsCalls["projects-search"]["count"]
            },
            parseState: async function (project) {
                const responseCalls = await fetch(
                    this.api_url + '/ast/' + project + '/state',
                    {
                        method: 'GET'
                    }
                )
                const statsCalls = await responseCalls.json()
                if (statsCalls["state"] === 'all') {
                    return "Completed"
                } else if (statsCalls["state"] === 'in-progress') {
                    return "In Progress"
                } else {
                    return "Initiate Generation"
                }
            },
            fetchItemData: async function (items) {
                for (const item of items) {
                    console.log(item);
                    this.$set(item, "dependents", await this.getDependentsCount(item.github_short_url));
                    this.$set(item, "state", await this.parseState(item.github_short_url));
                }
                this.$forceUpdate();
            },
            parseASTOfProject: function (item) {
                // post a request to initiate the parsing of the project
                fetch(`${this.api_url}/init/ast-search/java`, {
                    method: "POST", // *GET, POST, PUT, DELETE, etc.
                    mode: "cors", // no-cors, cors, *same-origin
                    cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
                    credentials: "same-origin", // include, *same-origin, omit
                    headers: {
                        "Content-Type": "application/json",
                    },
                    redirect: "follow", // manual, *follow, error
                    referrer: "no-referrer", // no-referrer, *client
                    body: JSON.stringify({"github_short_url": item.github_short_url, "parsing_type": "all"}), // body data type must match "Content-Type" header
                }).then(async () => {
                    this.$set(item, "state", await this.parseState(item.github_short_url));
                });
            }
        }
    }
</script>

<style scoped>

</style>