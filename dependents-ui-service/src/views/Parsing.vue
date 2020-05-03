<template>
    <div class="container">
        <div class="row">
            <div class="col-md-12">
                <h3 id="header" align="center"> {{ `Waiting to complete dependents search for
                    ${this.analysedGroup}/${this.analysedProject}.` }} </h3>
                <p id="progress" align="center"> {{ parseStatus}} </p>
                <p align="center">{{artifactStatus}}</p>
                <p align="center">{{astStatus}}</p>
            </div>
        </div>

        <hr>

        <div class="row">
            <div class="col-md-12">
                <p align="center">This page will refresh every 5 seconds.</p>
                <p align="center">
                    This page will automatically redirect to the produced statistics on completion of the search. This
                    may take some time.
                    <router-link :to="'/dependents/analysis/'+this.analysedGroup+'/'+this.analysedProject"> Click here
                    </router-link>
                    to view the incomplete results.
                </p>
            </div>
        </div>
    </div>
</template>

<script>
    import router from "../router";

    export default {
        name: "Parsing",
        data: function () {
            return {
                projectParsed: false,
                artifacts: undefined,
                astParsedState: undefined,
                timeout: null,
                done: false
            }
        },
        mounted: function () {
            // TODO: params
            this.fetchProgress(this.analysedGroup, this.analysedProject);
        },
        beforeRouteLeave(to, from, next) {
            clearTimeout(this.timeout);
            next()
        },
        computed: {
            analysedGroup: function () {
                return this.$route.params.group
            },
            analysedProject: function () {
                return this.$route.params.project
            },
            url: function () {
                return window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/'
            },
            parseStatus: function () {
                if (this.projectParsed) {
                    return "Waiting for project to be parsed."
                } else {
                    return "Searched base project."
                }
            },
            artifactStatus: function () {
                if (this.artifacts == undefined || this.artifacts['artifacts'] == undefined) {
                    return `Searched 0 of 0 discovered Artifacts in Project.`
                } else {
                    var completedCount = 0;
                    var totalCount = this.artifacts['artifacts'].length;

                    for (var i = 0; i < this.artifacts['artifacts'].length; i++) {
                        console.log(this.artifacts['artifacts'][i]);
                        if (this.artifacts['artifacts'][i]['search-state'] == "completed") {
                            completedCount += 1;
                        }
                    }
                    return `Searched ${completedCount} of ${totalCount} discovered Artifacts in Project.`
                }
            },
            astStatus: function () {
                if (this.astParsedState == 'packageclassonly' || this.astParsedState == 'all') {
                    return `Abstract Syntax Tree analysis completed.`;
                } else if (this.astParsedState == 'failed') {
                    return `Abstract Syntax Tree analysis failed. Some visualisations will not be available.`;
                } else {
                    return `Abstract Syntax Tree analysis in progress.`;
                }
            }
        },
        methods: {
            isProjectParsed: async function (group, repo) {
                let url = `${this.api_url}/project/${group}/${repo}/dependents/state`;

                return fetch(url).then(response => {
                    if (response.status >= 200 && response.status < 300) {
                        return Promise.resolve(response)
                    } else {
                        return Promise.reject(new Error(response.statusText))
                    }
                }).then(response => {
                    return response.json().then(responseJson => {
                        // if the project has been parsed
                        if (responseJson.state == "True") {
                            return Promise.resolve(true);
                        } else {
                            return Promise.resolve(false);
                        }
                    });
                }).catch(err => {
                    return Promise.resolve(false);
                });
            },
            artifactsParsed: async function (group, repo) {
                let url = `${this.api_url}/artifact/${group}/${repo}/dependents/state`;

                return fetch(url).then(response => {
                    if (response.status >= 200 && response.status < 300) {
                        return Promise.resolve(response)
                    } else {
                        return Promise.reject(new Error(response.statusText))
                    }
                }).then(response => {
                    return response.json().then(responseJson => {
                        return Promise.resolve(responseJson);
                    });
                }).catch(err => {
                    return Promise.resolve(false);
                });
            },
            astParsed: async function (group, repo) {
                let url = `${this.api_url}/ast/${group}/${repo}/state`;

                // fetch the current state of the project
                return fetch(url).then(response => {
                    if (response.status >= 200 && response.status < 300) {
                        return Promise.resolve(response)
                    } else {
                        return Promise.reject(new Error(response.statusText))
                    }
                }).then(response => {
                    return response.json().then(responseJson => {
                        console.log(responseJson.state);

                        return responseJson['state'];
                    });
                }).catch(() => {
                    return Promise.resolve(null);
                });
            },
            fetchProgress: function (group, repo) {
                const vue = this;
                this.isProjectParsed(group, repo).then(projectParsed => {
                    vue.projectParsed = projectParsed;
                    if (projectParsed) {
                        return vue.artifactsParsed(group, repo).then(artifacts => {
                            vue.artifacts = artifacts;
                            if (artifacts == undefined || artifacts['artifacts'] == undefined) {
                                return Promise.resolve();
                            }
                            var completedCount = 0;
                            var totalCount = vue.artifacts['artifacts'].length;

                            for (var i = 0; i < vue.artifacts['artifacts'].length; i++) {
                                console.log(vue.artifacts['artifacts'][i]);
                                if (vue.artifacts['artifacts'][i]['search-state'] == "completed") {
                                    completedCount += 1;
                                }
                            }

                            return this.astParsed(group, repo).then(astParsedState => {
                                let isAstParsed = false;
                                vue.astParsedState = astParsedState;
                                if (astParsedState == 'packageclassonly' || astParsedState == 'all') {
                                    isAstParsed = true;
                                }
                                // if all artifacts have been parsed, and the ast tree
                                // of the project is parsed, redirect to the project visualisation page
                                if ((completedCount == totalCount) && isAstParsed) {
                                    vue.done = true;
                                    // window.location.replace(`${project_page_url}?group=${group}&repo=${repo}`);
                                    router.push({
                                        name: 'Analysis',
                                        params: {group: this.analysedGroup, project: this.analysedProject}
                                    })
                                    console.log("Would redirect");
                                }
                            });
                        });
                    }
                }).then(() => {
                    if (!vue.done) {
                        vue.timeout = setTimeout(function () {
                            vue.fetchProgress(vue.analysedGroup, vue.analysedProject)
                        }, 5000);
                    }
                })
            }

        }
    }
</script>

<style scoped>

</style>