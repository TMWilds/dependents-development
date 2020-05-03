<template>
    <v-container>
        <h1> Select Project to Analyse</h1>
        <div class="home">
            <v-row>
                <v-col sm="5">
                    <v-text-field @keypress.enter="show"
                                  color="primary"
                                  label="Project Owner"
                                  v-model="group">

                        <template v-slot:prepend>
                            github.com/

                        </template>

                    </v-text-field>
                </v-col>
                <v-col sm="5">
                    <v-text-field @keypress.enter="show"
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
                            @click="dependentsSearchOnClick(group, project)">
                        Analyse
                    </v-btn>
                </v-col>
            </v-row>
        </div>
        <v-snackbar v-model="displaySnackbar" top right :timeout=3000 color="red"> {{snackbarText}} </v-snackbar>
    </v-container>
</template>

<script>

    import router from "../router";

    export default {
        name: 'Home',
        data: function () {
            return {
                group: 'jhy',
                project: 'jsoup',
                displaySnackbar: false,
                snackbarText: ''
            }
        },
        methods: {
            dependentsSearchOnClick: function (ownerValue, repositoryValue) {
                /**
                 *  Validate inputs
                 * */
                // let validation = document.getElementById(validationResponse);

                // if the owner field is empty, flag it
                if (ownerValue == "") {
                    this.snackbarText = "Repository Owner must not be empty";
                    this.displaySnackbar = true;
                    console.log("Repository Owner must not be empty");
                    // validation.innerHTML = "Repository Owner must not be empty";
                    return false;
                }

                // if the repository field is empty, flag it
                if (repositoryValue == "") {
                    this.snackbarText = "Repository Name field must not be empty";
                    this.displaySnackbar = true;
                    console.log("Repository Name field must not be empty");
                    // validation.innerHTML = "Repository Name field must not be empty";
                    return false;
                }

                // check if the github url given exists, else flag the error
                console.log(this.api_url);
                let url = `${this.api_url}/project/${ownerValue}/${repositoryValue}/validate`;
                var http = new XMLHttpRequest();
                http.open('HEAD', url, false);
                http.send();
                if (http.status != 200) {
                    this.snackbarText = "GitHub project entered is either private, does not exist, or is not a Java project built using Maven.";
                    this.displaySnackbar = true;
                    console.log("GitHub project entered is either private, does not exist, or is not a Java project built using Maven.");
                    // validation.innerHTML = "GitHub project entered is either private, does not exist, or is not a Java project built using Maven.";
                    return false;
                }

                // validation.innerHTML = "";

                // initiate searching for dependent repositories
                return fetch(`${this.api_url}/init/dependents-search/pom`, {
                    method: "POST",
                    mode: "cors",
                    cache: "no-cache",
                    credentials: "same-origin",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    redirect: "follow",
                    referrer: "no-referrer",
                    body: JSON.stringify({"github_short_url": `${ownerValue}/${repositoryValue}`})
                }).then(() => {
                    // initiate parsing of the ast tree for this project. If it has already been parsed, it won't
                    // be parsed again in the back end
                    return fetch(`${this.api_url}/ast/${ownerValue}/${repositoryValue}/state`).then(response => {
                        if (response.status >= 200 && response.status < 300) {
                            return Promise.resolve(response)
                        } else {
                            return Promise.reject(new Error(response.statusText))
                        }
                    }).then(response => {
                        return response.json().then(responseJson => {
                            console.log(responseJson);
                            console.log(responseJson['state']);

                            return responseJson['state'];
                        });
                    }).then(parseState => {
                        console.log("parse state is " + parseState);
                        // initiate parsing if it has not already completed
                        if (parseState == "failed" || parseState == "not-parsed" || parseState == null) {
                            console.log("initiating parsing ");

                            return fetch(`${this.api_url}/init/ast-search/java`, {
                                method: "POST",
                                mode: "cors",
                                cache: "no-cache",
                                credentials: "same-origin",
                                headers: {
                                    "Content-Type": "application/json",
                                },
                                redirect: "follow",
                                referrer: "no-referrer",
                                body: JSON.stringify({
                                    "github_short_url": `${ownerValue}/${repositoryValue}`,
                                    "parsing_type": "packageclassonly"
                                }),
                            });
                        } else {
                            return Promise.resolve();
                        }
                    });
                }).then(() => {
                    // redirect the user to the parse waiting loop page to retrieve analysis progress updates
                    router.push({ name: 'Parsing', params: { group: this.group, project: this.project } })
                });
            }
        },
    }
</script>
