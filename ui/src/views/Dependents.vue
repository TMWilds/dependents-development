<template>
    <v-container>
        <v-row>
            <v-col md="6">
                <div v-if="hiearchyData">
                    <!--<router-link to="/">Home</router-link> |-->
                    <!--<router-link to="/about">About</router-link>-->
                    <input v-model="checked" type="checkbox">
                    <treemap v-on:clickNode="onHierarchyNodeSelect" v-show="!checked" :data="hiearchyData" style="margin-bottom: 10rem"></treemap>
                    <sunburst v-on:clickNode="onHierarchyNodeSelect" v-show="checked" :data="hiearchyData">
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
                <input v-model="checkedRel" type="checkbox">
                <treemap v-show="!checkedRel" :data="dummy" style="margin-bottom: 10rem"/>
                <force-graph v-show="checkedRel" :data="forceTestData"/>
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
    import ForceGraph from "../components/ForceGraph";

    export default {
        components: {
            ForceGraph,
            Treemap,
            breadcrumbTrail,
            highlightOnHover,
            nodeInfoDisplayer,
            sunburst,
            zoomOnClick
        },
        created: async function () {
            const response = await fetch(
                'http://localhost:8080/api/v1/project/jhy/jsoup/retrieve/hierarchy',
                {
                    method: 'GET'
                }
            )
            const stats = await response.json()
            this.hiearchyData = stats["data"]
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
                // dummy: {
                //     "name": "org.jsoup",
                //     "size": 2,
                //     "children": [{
                //         "name": "org.jsoup.select",
                //         "size": 1,
                //         "children": [{
                //             "name": "org.jsoup.select.Elements",
                //             "size": 1,
                //             "children": [{
                //                 "name": "org.jsoup.select.Elements.first",
                //                 "size": 1,
                //                 "children": []
                //             }, {
                //                 "name": "org.jsoup.select.Elements.select",
                //                 "size": 1,
                //                 "children": []
                //             }, {"name": "org.jsoup.select.Elements.attr", "size": 1, "children": []}]
                //         }]
                //     }, {
                //         "name": "org.jsoup.nodes",
                //         "size": 2,
                //         "children": [{
                //             "name": "org.jsoup.nodes.Node",
                //             "size": 1,
                //             "children": [{"name": "org.jsoup.nodes.Node.attr", "size": 1, "children": []}]
                //         }, {
                //             "name": "org.jsoup.nodes.Element",
                //             "size": 2,
                //             "children": [{
                //                 "name": "org.jsoup.nodes.Element.select",
                //                 "size": 1,
                //                 "children": []
                //             }, {
                //                 "name": "org.jsoup.nodes.Element.tagName",
                //                 "size": 1,
                //                 "children": []
                //             }, {
                //                 "name": "org.jsoup.nodes.Element.children",
                //                 "size": 1,
                //                 "children": []
                //             }, {
                //                 "name": "org.jsoup.nodes.Element.text",
                //                 "size": 2,
                //                 "children": []
                //             }, {
                //                 "name": "org.jsoup.nodes.Element.child",
                //                 "size": 1,
                //                 "children": []
                //             }, {
                //                 "name": "org.jsoup.nodes.Element.nextElementSibling",
                //                 "size": 1,
                //                 "children": []
                //             }, {
                //                 "name": "org.jsoup.nodes.Element.siblingElements",
                //                 "size": 1,
                //                 "children": []
                //             }, {"name": "org.jsoup.nodes.Element.getElementsByClass", "size": 1, "children": []}]
                //         }]
                //     }, {
                //         "name": "org.jsoup.Connection",
                //         "size": 2,
                //         "children": [{
                //             "name": "org.jsoup.Connection.userAgent",
                //             "size": 1,
                //             "children": []
                //         }, {"name": "org.jsoup.Connection.get", "size": 2, "children": []}]
                //     }, {
                //         "name": "org.jsoup.Jsoup",
                //         "size": 2,
                //         "children": [{
                //             "name": "org.jsoup.Jsoup.parse",
                //             "size": 1,
                //             "children": []
                //         }, {"name": "org.jsoup.Jsoup.connect", "size": 2, "children": []}]
                //     }]
                // },
                dummy: {"children":[{"children":[{"children":[{"children":[{"children":[],"id":7520,"label":"Method","name":"sites.Senado.parseData","properties":{"id":"sites.Senado.parseData","name":"parseData"},"size":5,"usage":20,"value":5}],"id":7515,"label":"ClassOrInterface","name":"sites.Senado","properties":{"id":"sites.Senado","name":"Senado"},"size":5,"usage":5,"value":5},{"children":[{"children":[],"id":7397,"label":"Method","name":"sites.Camara.scrapDataCriaPolitico","properties":{"id":"sites.Camara.scrapDataCriaPolitico","name":"scrapDataCriaPolitico"},"size":8,"usage":32,"value":8},{"children":[],"id":7393,"label":"Method","name":"sites.Camara.pegaUrlsNavega","properties":{"id":"sites.Camara.pegaUrlsNavega","name":"pegaUrlsNavega"},"size":3,"usage":12,"value":3}],"id":7387,"label":"ClassOrInterface","name":"sites.Camara","properties":{"id":"sites.Camara","name":"Camara"},"size":9,"usage":11,"value":9},{"children":[{"children":[],"id":7277,"label":"Method","name":"sites.Veja.getData","properties":{"id":"sites.Veja.getData","name":"getData"},"size":4,"usage":16,"value":4}],"id":7274,"label":"ClassOrInterface","name":"sites.Veja","properties":{"id":"sites.Veja","name":"Veja"},"size":4,"usage":4,"value":4},{"children":[{"children":[],"id":7476,"label":"Method","name":"sites.Infografo.getData","properties":{"id":"sites.Infografo.getData","name":"getData"},"size":2,"usage":8,"value":2}],"id":7475,"label":"ClassOrInterface","name":"sites.Infografo","properties":{"id":"sites.Infografo","name":"Infografo"},"size":2,"usage":2,"value":2},{"children":[{"children":[],"id":7474,"label":"Method","name":"sites.ContraCorrupcao.getData","properties":{"id":"sites.ContraCorrupcao.getData","name":"getData"},"size":2,"usage":8,"value":2}],"id":7472,"label":"ClassOrInterface","name":"sites.ContraCorrupcao","properties":{"id":"sites.ContraCorrupcao","name":"ContraCorrupcao"},"size":2,"usage":2,"value":2},{"children":[{"children":[],"id":7385,"label":"Method","name":"sites.Politicosorg.getData","properties":{"id":"sites.Politicosorg.getData","name":"getData"},"size":1,"usage":4,"value":1}],"id":7383,"label":"ClassOrInterface","name":"sites.Politicosorg","properties":{"id":"sites.Politicosorg","name":"Politicosorg"},"size":1,"usage":1,"value":1},{"children":[{"children":[],"id":7378,"label":"Method","name":"sites.MovimentoFichaLimpa.getData","properties":{"id":"sites.MovimentoFichaLimpa.getData","name":"getData"},"size":2,"usage":8,"value":2}],"id":7376,"label":"ClassOrInterface","name":"sites.MovimentoFichaLimpa","properties":{"id":"sites.MovimentoFichaLimpa","name":"MovimentoFichaLimpa"},"size":2,"usage":2,"value":2},{"children":[{"children":[],"id":7299,"label":"Method","name":"sites.Site.lePagina","properties":{"id":"sites.Site.lePagina","name":"lePagina"},"size":4,"usage":16,"value":4}],"id":7275,"label":"ClassOrInterface","name":"sites.Site","properties":{"id":"sites.Site","name":"Site"},"size":4,"usage":4,"value":4}],"id":7273,"label":"Package","name":"sites","properties":{"id":"sites","name":"sites"},"size":15,"usage":31,"value":15}],"id":6208,"label":"Project","name":"egrohs/Politicos","properties":{"id":"egrohs/Politicos"},"size":15,"usage":31,"value":15},{"children":[{"children":[{"children":[{"children":[],"id":8024,"label":"Method","name":"hu.fnf.devel.forex.utils.MarketWebProxy.isMarketOpen","properties":{"id":"hu.fnf.devel.forex.utils.MarketWebProxy.isMarketOpen","name":"isMarketOpen"},"size":1,"usage":9,"value":1},{"children":[],"id":8022,"label":"Method","name":"hu.fnf.devel.forex.utils.MarketWebProxy.MarketWebProxy","properties":{"id":"hu.fnf.devel.forex.utils.MarketWebProxy.MarketWebProxy","name":"MarketWebProxy"},"size":3,"usage":27,"value":3}],"id":8021,"label":"ClassOrInterface","name":"hu.fnf.devel.forex.utils.MarketWebProxy","properties":{"id":"hu.fnf.devel.forex.utils.MarketWebProxy","name":"MarketWebProxy"},"size":4,"usage":8,"value":4}],"id":7958,"label":"Package","name":"hu.fnf.devel.forex.utils","properties":{"id":"hu.fnf.devel.forex.utils","name":"utils"},"size":4,"usage":8,"value":4},{"children":[{"children":[{"children":[{"children":[],"id":8024,"label":"Method","name":"hu.fnf.devel.forex.utils.MarketWebProxy.isMarketOpen","properties":{"id":"hu.fnf.devel.forex.utils.MarketWebProxy.isMarketOpen","name":"isMarketOpen"},"size":1,"usage":9,"value":1},{"children":[],"id":8022,"label":"Method","name":"hu.fnf.devel.forex.utils.MarketWebProxy.MarketWebProxy","properties":{"id":"hu.fnf.devel.forex.utils.MarketWebProxy.MarketWebProxy","name":"MarketWebProxy"},"size":3,"usage":27,"value":3}],"id":8021,"label":"ClassOrInterface","name":"hu.fnf.devel.forex.utils.MarketWebProxy","properties":{"id":"hu.fnf.devel.forex.utils.MarketWebProxy","name":"MarketWebProxy"},"size":4,"usage":8,"value":4}],"id":7958,"label":"Package","name":"hu.fnf.devel.forex.utils","properties":{"id":"hu.fnf.devel.forex.utils","name":"utils"},"size":4,"usage":8,"value":4}],"id":7955,"label":"Package","name":"hu.fnf.devel.forex","properties":{"id":"hu.fnf.devel.forex","name":"forex"},"size":4,"usage":4,"value":4}],"id":6167,"label":"Project","name":"csikosbalint/forex-strategy","properties":{"id":"csikosbalint/forex-strategy"},"size":4,"usage":8,"value":4}],"name":"jsoup"},
                checked: false,
                checkedRel: false,
                hiearchyData: null,
                forceTestData: {
                    "name": "root",
                    "id": "root",
                    "children": [
                        {
                            "children": [{
                                "children": [{
                                    "children": [{
                                        "children": [],
                                        "id": 7520,
                                        "label": "Method",
                                        "name": "sites.Senado.parseData",
                                        "properties": {"id": "sites.Senado.parseData", "name": "parseData"},
                                        "size": 1
                                    }],
                                    "id": 7515,
                                    "label": "ClassOrInterface",
                                    "name": "sites.Senado",
                                    "properties": {"id": "sites.Senado", "name": "Senado"},
                                    "size": 1
                                }, {
                                    "children": [{
                                        "children": [],
                                        "id": 7397,
                                        "label": "Method",
                                        "name": "sites.Camara.scrapDataCriaPolitico",
                                        "properties": {
                                            "id": "sites.Camara.scrapDataCriaPolitico",
                                            "name": "scrapDataCriaPolitico"
                                        },
                                        "size": 1
                                    }, {
                                        "children": [],
                                        "id": 7393,
                                        "label": "Method",
                                        "name": "sites.Camara.pegaUrlsNavega",
                                        "properties": {"id": "sites.Camara.pegaUrlsNavega", "name": "pegaUrlsNavega"},
                                        "size": 1
                                    }],
                                    "id": 7387,
                                    "label": "ClassOrInterface",
                                    "name": "sites.Camara",
                                    "properties": {"id": "sites.Camara", "name": "Camara"},
                                    "size": 1
                                }, {
                                    "children": [{
                                        "children": [],
                                        "id": 7277,
                                        "label": "Method",
                                        "name": "sites.Veja.getData",
                                        "properties": {"id": "sites.Veja.getData", "name": "getData"},
                                        "size": 1
                                    }],
                                    "id": 7274,
                                    "label": "ClassOrInterface",
                                    "name": "sites.Veja",
                                    "properties": {"id": "sites.Veja", "name": "Veja"},
                                    "size": 1
                                }, {
                                    "children": [{
                                        "children": [],
                                        "id": 7476,
                                        "label": "Method",
                                        "name": "sites.Infografo.getData",
                                        "properties": {"id": "sites.Infografo.getData", "name": "getData"},
                                        "size": 1
                                    }],
                                    "id": 7475,
                                    "label": "ClassOrInterface",
                                    "name": "sites.Infografo",
                                    "properties": {"id": "sites.Infografo", "name": "Infografo"},
                                    "size": 1
                                }, {
                                    "children": [{
                                        "children": [],
                                        "id": 7474,
                                        "label": "Method",
                                        "name": "sites.ContraCorrupcao.getData",
                                        "properties": {"id": "sites.ContraCorrupcao.getData", "name": "getData"},
                                        "size": 1
                                    }],
                                    "id": 7472,
                                    "label": "ClassOrInterface",
                                    "name": "sites.ContraCorrupcao",
                                    "properties": {"id": "sites.ContraCorrupcao", "name": "ContraCorrupcao"},
                                    "size": 1
                                }, {
                                    "children": [{
                                        "children": [],
                                        "id": 7385,
                                        "label": "Method",
                                        "name": "sites.Politicosorg.getData",
                                        "properties": {"id": "sites.Politicosorg.getData", "name": "getData"},
                                        "size": 1
                                    }],
                                    "id": 7383,
                                    "label": "ClassOrInterface",
                                    "name": "sites.Politicosorg",
                                    "properties": {"id": "sites.Politicosorg", "name": "Politicosorg"},
                                    "size": 1
                                }, {
                                    "children": [{
                                        "children": [],
                                        "id": 7378,
                                        "label": "Method",
                                        "name": "sites.MovimentoFichaLimpa.getData",
                                        "properties": {"id": "sites.MovimentoFichaLimpa.getData", "name": "getData"},
                                        "size": 1
                                    }],
                                    "id": 7376,
                                    "label": "ClassOrInterface",
                                    "name": "sites.MovimentoFichaLimpa",
                                    "properties": {"id": "sites.MovimentoFichaLimpa", "name": "MovimentoFichaLimpa"},
                                    "size": 1
                                }, {
                                    "children": [{
                                        "children": [],
                                        "id": 7299,
                                        "label": "Method",
                                        "name": "sites.Site.lePagina",
                                        "properties": {"id": "sites.Site.lePagina", "name": "lePagina"},
                                        "size": 1
                                    }],
                                    "id": 7275,
                                    "label": "ClassOrInterface",
                                    "name": "sites.Site",
                                    "properties": {"id": "sites.Site", "name": "Site"},
                                    "size": 1
                                }],
                                "id": 7273,
                                "label": "Package",
                                "name": "sites",
                                "properties": {"id": "sites", "name": "sites"},
                                "size": 1
                            }],
                            "id": 6208,
                            "label": "Project",
                            "name": "egrohs/Politicos",
                            "properties": {"id": "egrohs/Politicos"},
                            "size": 1
                        },
                        {
                            "children": [{
                                "children": [{
                                    "children": [{
                                        "children": [],
                                        "id": 8024,
                                        "label": "Method",
                                        "name": "hu.fnf.devel.forex.utils.MarketWebProxy.isMarketOpen",
                                        "properties": {
                                            "id": "hu.fnf.devel.forex.utils.MarketWebProxy.isMarketOpen",
                                            "name": "isMarketOpen"
                                        },
                                        "size": 1
                                    }, {
                                        "children": [],
                                        "id": 8022,
                                        "label": "Method",
                                        "name": "hu.fnf.devel.forex.utils.MarketWebProxy.MarketWebProxy",
                                        "properties": {
                                            "id": "hu.fnf.devel.forex.utils.MarketWebProxy.MarketWebProxy",
                                            "name": "MarketWebProxy"
                                        },
                                        "size": 1
                                    }],
                                    "id": 8021,
                                    "label": "ClassOrInterface",
                                    "name": "hu.fnf.devel.forex.utils.MarketWebProxy",
                                    "properties": {
                                        "id": "hu.fnf.devel.forex.utils.MarketWebProxy",
                                        "name": "MarketWebProxy"
                                    },
                                    "size": 1
                                }],
                                "id": 7958,
                                "label": "Package",
                                "name": "hu.fnf.devel.forex.utils",
                                "properties": {"id": "hu.fnf.devel.forex.utils", "name": "utils"},
                                "size": 1
                            }, {
                                "children": [{
                                    "children": [{
                                        "children": [{
                                            "children": [],
                                            "id": 8024,
                                            "label": "Method",
                                            "name": "hu.fnf.devel.forex.utils.MarketWebProxy.isMarketOpen",
                                            "properties": {
                                                "id": "hu.fnf.devel.forex.utils.MarketWebProxy.isMarketOpen",
                                                "name": "isMarketOpen"
                                            },
                                            "size": 1
                                        }, {
                                            "children": [],
                                            "id": 8022,
                                            "label": "Method",
                                            "name": "hu.fnf.devel.forex.utils.MarketWebProxy.MarketWebProxy",
                                            "properties": {
                                                "id": "hu.fnf.devel.forex.utils.MarketWebProxy.MarketWebProxy",
                                                "name": "MarketWebProxy"
                                            },
                                            "size": 1
                                        }],
                                        "id": 8021,
                                        "label": "ClassOrInterface",
                                        "name": "hu.fnf.devel.forex.utils.MarketWebProxy",
                                        "properties": {
                                            "id": "hu.fnf.devel.forex.utils.MarketWebProxy",
                                            "name": "MarketWebProxy"
                                        },
                                        "size": 1
                                    }],
                                    "id": 7958,
                                    "label": "Package",
                                    "name": "hu.fnf.devel.forex.utils",
                                    "properties": {"id": "hu.fnf.devel.forex.utils", "name": "utils"},
                                    "size": 1
                                }],
                                "id": 7955,
                                "label": "Package",
                                "name": "hu.fnf.devel.forex",
                                "properties": {"id": "hu.fnf.devel.forex", "name": "forex"},
                                "size": 1
                            }],
                            "id": 6167,
                            "label": "Project",
                            "name": "csikosbalint/forex-strategy",
                            "properties": {"id": "csikosbalint/forex-strategy"},
                            "size": 1
                        }]
                }
            }
        },
        methods: {
            onHierarchyNodeSelect: async function(node){
             const response = await fetch(
                'http://localhost:8080/api/v1/ast/jhy/jsoup/dependent_asts?label=Package&id=' + node.node.data.name,
                {
                    method: 'GET'
                }
            )
            console.log(node)
            const stats = await response.json()
            this.forceTestData = stats["data"]
            }
        }
    }
</script>
