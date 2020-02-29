<template>
    <v-container>
        <v-row>
            <v-col md="6">
                <div>
                    <!--<router-link to="/">Home</router-link> |-->
                    <!--<router-link to="/about">About</router-link>-->
                    <input v-model="checked" type="checkbox">
                    <treemap v-show="!checked" style="margin-bottom: 10rem"></treemap>
                    <sunburst v-show="checked" :data="dummy">
                        <!-- Add behaviors -->
                        <template slot-scope="{ on, actions }">
                            <highlightOnHover v-bind="{ on, actions }"/>
                            <zoomOnClick v-bind="{ on, actions }"/>
                        </template>

                        <!-- Add information to be displayed on top the graph -->
                        <nodeInfoDisplayer slot="top" slot-scope="{ nodes }" :current="nodes.mouseOver"
                                           :root="nodes.root"
                                           description="of visits begin with this sequence of pages"/>

                        <!-- Add bottom legend -->
                        <breadcrumbTrail slot="legend" slot-scope="{ nodes, colorGetter, width }"
                                         :current="nodes.mouseOver"
                                         :root="nodes.root" :colorGetter="colorGetter" :from="nodes.clicked"
                                         :width="width"/>

                    </sunburst>
                </div>
            </v-col>
            <v-col md="6">

            </v-col>
        </v-row>
    </v-container>
</template>

<script>
    import Treemap from "../components/Treemap";
    import {
        breadcrumbTrail,
        highlightOnHover,
        nodeInfoDisplayer,
        sunburst,
        zoomOnClick
    } from 'vue-d3-sunburst';
    import "vue-d3-sunburst/dist/vue-d3-sunburst.css";

    export default {
        components: {
            Treemap,
            breadcrumbTrail,
            highlightOnHover,
            nodeInfoDisplayer,
            sunburst,
            zoomOnClick
        },
        data: function () {
            return {
                // dummy: {
                //         "name": "org.jsoup",
                //         "children": [{
                //             "name": "org.jsoup.select",
                //             "children": [{
                //                 "name": "org.jsoup.select.Elements",
                //                 "children": [{
                //                     "name": "org.jsoup.select.Elements.first",
                //                     "size": 1,
                //                 }, {
                //                     "name": "org.jsoup.select.Elements.select",
                //                     "size": 1,
                //                 }, {"name": "org.jsoup.select.Elements.attr", "size": 1}]
                //             }]
                //         }, {
                //             "name": "org.jsoup.nodes",
                //             "children": [{
                //                 "name": "org.jsoup.nodes.Node",
                //                 "children": [{"name": "org.jsoup.nodes.Node.attr", "size": 1}]
                //             }, {
                //                 "name": "org.jsoup.nodes.Element",
                //                 "children": [{
                //                     "name": "org.jsoup.nodes.Element.select",
                //                     "size": 1,
                //                 }, {
                //                     "name": "org.jsoup.nodes.Element.tagName",
                //                     "size": 1,
                //                 }, {
                //                     "name": "org.jsoup.nodes.Element.children",
                //                     "size": 1,
                //                 }, {
                //                     "name": "org.jsoup.nodes.Element.text",
                //                     "size": 2,
                //                 }, {
                //                     "name": "org.jsoup.nodes.Element.child",
                //                     "size": 1,
                //                 }, {
                //                     "name": "org.jsoup.nodes.Element.nextElementSibling",
                //                     "size": 1,
                //                 }, {
                //                     "name": "org.jsoup.nodes.Element.siblingElements",
                //                     "size": 1,
                //                 }, {"name": "org.jsoup.nodes.Element.getElementsByClass", "size": 1,}]
                //             }]
                //         }, {
                //             "name": "org.jsoup.Connection",
                //             "children": [{
                //                 "name": "org.jsoup.Connection.userAgent",
                //                 "size": 1,
                //             }, {"name": "org.jsoup.Connection.get", "size": 2}]
                //         }, {
                //             "name": "org.jsoup.Jsoup",
                //             "children": [{
                //                 "name": "org.jsoup.Jsoup.parse",
                //                 "size": 2,
                //             }, {"name": "org.jsoup.Jsoup.connect", "size": 2}]
                //         }]
                //     }
                dummy: {
                    "name": "org.jsoup",
                    "size": 2,
                    "children": [{
                        "name": "org.jsoup.select",
                        "size": 1,
                        "children": [{
                            "name": "org.jsoup.select.Elements",
                            "size": 1,
                            "children": [{
                                "name": "org.jsoup.select.Elements.first",
                                "size": 1,
                                "children": []
                            }, {
                                "name": "org.jsoup.select.Elements.select",
                                "size": 1,
                                "children": []
                            }, {"name": "org.jsoup.select.Elements.attr", "size": 1, "children": []}]
                        }]
                    }, {
                        "name": "org.jsoup.nodes",
                        "size": 2,
                        "children": [{
                            "name": "org.jsoup.nodes.Node",
                            "size": 1,
                            "children": [{"name": "org.jsoup.nodes.Node.attr", "size": 1, "children": []}]
                        }, {
                            "name": "org.jsoup.nodes.Element",
                            "size": 2,
                            "children": [{
                                "name": "org.jsoup.nodes.Element.select",
                                "size": 1,
                                "children": []
                            }, {
                                "name": "org.jsoup.nodes.Element.tagName",
                                "size": 1,
                                "children": []
                            }, {
                                "name": "org.jsoup.nodes.Element.children",
                                "size": 1,
                                "children": []
                            }, {
                                "name": "org.jsoup.nodes.Element.text",
                                "size": 2,
                                "children": []
                            }, {
                                "name": "org.jsoup.nodes.Element.child",
                                "size": 1,
                                "children": []
                            }, {
                                "name": "org.jsoup.nodes.Element.nextElementSibling",
                                "size": 1,
                                "children": []
                            }, {
                                "name": "org.jsoup.nodes.Element.siblingElements",
                                "size": 1,
                                "children": []
                            }, {"name": "org.jsoup.nodes.Element.getElementsByClass", "size": 1, "children": []}]
                        }]
                    }, {
                        "name": "org.jsoup.Connection",
                        "size": 2,
                        "children": [{
                            "name": "org.jsoup.Connection.userAgent",
                            "size": 1,
                            "children": []
                        }, {"name": "org.jsoup.Connection.get", "size": 2, "children": []}]
                    }, {
                        "name": "org.jsoup.Jsoup",
                        "size": 2,
                        "children": [{
                            "name": "org.jsoup.Jsoup.parse",
                            "size": 1,
                            "children": []
                        }, {"name": "org.jsoup.Jsoup.connect", "size": 2, "children": []}]
                    }]
                },
                checked: false,
            }

        }
    }
</script>
