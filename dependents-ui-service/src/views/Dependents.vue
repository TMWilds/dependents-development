<template>
    <v-container>
        <v-tabs
                v-model="tab"
                background-color="transparent"
                grow
        >
            <v-tab
                    key="overview"
            >
                Overview
            </v-tab>
            <v-tab
                    key="hierarchy"
            >
                Hierarchy View
            </v-tab>
        </v-tabs>

        <v-tabs-items v-model="tab">
            <v-tab-item key="overview">
                <edge-bundle v-if="overviewData" :analysed-project="analysedProject" :call-data="overviewData"/>
            </v-tab-item>
            <v-tab-item key="hierarchy">
                <v-row>
                    <v-col md="6">
                        <v-tabs
                                v-model="checked"

                        >
                            <v-tab
                                    key="treemap"
                            >
                                Treemap
                            </v-tab>
                            <v-tab
                                    key="sunburst"
                            >
                                Sunburst
                            </v-tab>
                        </v-tabs>
                        <v-tabs-items v-model="checked">
                            <v-tab-item key="treemap">
                                <treemap v-on:clickNode="onHierarchyNodeSelect" v-show="!checked"
                                         :data="hiearchyData"
                                         style="margin-bottom: 10rem">
                                    <template slot="tile-text" slot-scope="{ tile, x, y }">
                                        <tspan style="font-weight: bold" dx="0em" dy="1em">{{ tile.data.name }}</tspan>
                                        <tspan :x="x" dy="1em">{{ tile.data.value }} usage{{tile.data.value !== 1 ? 's':''}}</tspan>
                                        <tspan :x="x" dy="1em">{{ tile.data.dependent_projects }} dependent project{{tile.data.dependent_projects !== 1 ? 's':''}}</tspan>
                                    </template>
                                </treemap>
                            </v-tab-item>
                            <v-tab-item key="sunburst">
                                <sunburst ref="sunburst" v-on:clickNode="onHierarchyNodeSelect"
                                          :data="hiearchyData" style="height: 30rem; margin-top: 3rem">
                                    <!-- Add behaviors -->
                                    <template slot-scope="{ on, actions }">
                                        <highlightOnHover v-bind="{ on, actions }"/>
                                        <zoomOnClick v-bind="{ on, actions }"/>
                                    </template>

                                    <!-- Add information to be displayed on top the graph -->
                                    <SunburstNodeInfo slot="top" slot-scope="{ nodes }" :current="nodes.mouseOver"
                                                       :root="nodes.root" :show-all-number="true"
                                                       description="of visits begin with this sequence of pages">
                                        <template slot="display" slot-scope="{current}">
                                            <span> {{current.value}} usages </span> <br />
                                            <span> {{current.data.dependent_projects}} dependent projects </span>
                                        </template>
                                    </SunburstNodeInfo>

                                    <!-- Add bottom legend -->
                                    <breadcrumbTrail slot="legend" slot-scope="{ nodes, colorGetter, width }"
                                                     :current="nodes.mouseOver"
                                                     :root="nodes.root" :colorGetter="colorGetter"
                                                     :from="nodes.clicked"
                                                     :width="width"/>

                                </sunburst>
                            </v-tab-item>
                        </v-tabs-items>
                    </v-col>
                    <v-col md="6">
                        <v-tabs
                                v-model="checkedRel"

                        >
                            <v-tab
                                    key="treemap-sub"
                            >
                                Treemap
                            </v-tab>
                            <v-tab
                                    key="graph"
                            >
                                Force Directed Graph
                            </v-tab>
                            <v-tab>
                                Tree
                            </v-tab>
                        </v-tabs>
                        <v-tabs-items v-model="checkedRel">
                            <v-tab-item key="treemap-sub">
                                <treemap v-show="!checkedRel" :data="dummy" style="margin-bottom: 10rem">
                                    <template slot="tile-text" slot-scope="{ tile, x, y }">
                                        <tspan style="font-weight: bold" dx="0em" dy="1em">{{ tile.data.name }}</tspan>
                                        <tspan :x="x" dy="1em">{{ tile.data.value }} usage{{tile.data.value !== 1 ? 's':''}}</tspan>
                                        <tspan :x="x" dy="1em">{{ tile.data.distinct_usage }} distinct usage{{tile.data.distinct_usage !== 1 ? 's':''}}</tspan>
                                    </template>
                                </treemap>
                            </v-tab-item>
                            <v-tab-item key="graph">
                                <force-graph v-show="checkedRel" :data="forceTestData" style="height: 30rem"/>
                            </v-tab-item>
                            <v-tab-item key="tree">
                                <tidy-tree :data="forceTestData"/>
                            </v-tab-item>
                        </v-tabs-items>
                    </v-col>
                </v-row>
            </v-tab-item>
        </v-tabs-items>
        <v-row>
            <v-col md="12">
                <!--                            <edge-bundle/>-->
            </v-col>
        </v-row>

    </v-container>
</template>

<script>
    import Treemap from "../components/Treemap";
    import {
        breadcrumbTrail,
        highlightOnHover,
        sunburst,
        zoomOnClick
    } from 'vue-d3-sunburst';
    import SunburstNodeInfo from "../components/SunburstNodeInfo";
    import "vue-d3-sunburst/dist/vue-d3-sunburst.css";
    import ForceGraph from "../components/ForceGraph";
    import EdgeBundle from "../components/EdgeBundle";
    import TidyTree from "../components/TidyTree";

    export default {
        components: {
            EdgeBundle,
            ForceGraph,
            Treemap,
            breadcrumbTrail,
            highlightOnHover,
            sunburst,
            zoomOnClick,
            SunburstNodeInfo,
            TidyTree
        },
        mounted: async function () {
            const response = await fetch(
                'http://localhost:8080/api/v1/project/jhy/jsoup/retrieve/hierarchy',
                {
                    method: 'GET'
                }
            )
            const stats = await response.json()
            this.hiearchyData = stats["data"]

            const responseCalls = await fetch(
                'http://localhost:8080/api/v1/project/jhy/jsoup/retrieve/project_calls',
                {
                    method: 'GET'
                }
            )
            const statsCalls = await responseCalls.json()
            this.overviewData = statsCalls["data"]
        },
        data: function () {
            return {
                dummy: {
                    "children": [{
                        "children": [{
                            "children": [{
                                "children": [{
                                    "children": [],
                                    "id": 7520,
                                    "label": "Method",
                                    "name": "sites.Senado.parseData",
                                    "properties": {"id": "sites.Senado.parseData", "name": "parseData"},
                                    "size": 5,
                                    "usage": 20,
                                    "value": 5
                                }],
                                "id": 7515,
                                "label": "ClassOrInterface",
                                "name": "sites.Senado",
                                "properties": {"id": "sites.Senado", "name": "Senado"},
                                "size": 5,
                                "usage": 5,
                                "value": 5
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
                                    "size": 8,
                                    "usage": 32,
                                    "value": 8
                                }, {
                                    "children": [],
                                    "id": 7393,
                                    "label": "Method",
                                    "name": "sites.Camara.pegaUrlsNavega",
                                    "properties": {"id": "sites.Camara.pegaUrlsNavega", "name": "pegaUrlsNavega"},
                                    "size": 3,
                                    "usage": 12,
                                    "value": 3
                                }],
                                "id": 7387,
                                "label": "ClassOrInterface",
                                "name": "sites.Camara",
                                "properties": {"id": "sites.Camara", "name": "Camara"},
                                "size": 9,
                                "usage": 11,
                                "value": 9
                            }, {
                                "children": [{
                                    "children": [],
                                    "id": 7277,
                                    "label": "Method",
                                    "name": "sites.Veja.getData",
                                    "properties": {"id": "sites.Veja.getData", "name": "getData"},
                                    "size": 4,
                                    "usage": 16,
                                    "value": 4
                                }],
                                "id": 7274,
                                "label": "ClassOrInterface",
                                "name": "sites.Veja",
                                "properties": {"id": "sites.Veja", "name": "Veja"},
                                "size": 4,
                                "usage": 4,
                                "value": 4
                            }, {
                                "children": [{
                                    "children": [],
                                    "id": 7476,
                                    "label": "Method",
                                    "name": "sites.Infografo.getData",
                                    "properties": {"id": "sites.Infografo.getData", "name": "getData"},
                                    "size": 2,
                                    "usage": 8,
                                    "value": 2
                                }],
                                "id": 7475,
                                "label": "ClassOrInterface",
                                "name": "sites.Infografo",
                                "properties": {"id": "sites.Infografo", "name": "Infografo"},
                                "size": 2,
                                "usage": 2,
                                "value": 2
                            }, {
                                "children": [{
                                    "children": [],
                                    "id": 7474,
                                    "label": "Method",
                                    "name": "sites.ContraCorrupcao.getData",
                                    "properties": {"id": "sites.ContraCorrupcao.getData", "name": "getData"},
                                    "size": 2,
                                    "usage": 8,
                                    "value": 2
                                }],
                                "id": 7472,
                                "label": "ClassOrInterface",
                                "name": "sites.ContraCorrupcao",
                                "properties": {"id": "sites.ContraCorrupcao", "name": "ContraCorrupcao"},
                                "size": 2,
                                "usage": 2,
                                "value": 2
                            }, {
                                "children": [{
                                    "children": [],
                                    "id": 7385,
                                    "label": "Method",
                                    "name": "sites.Politicosorg.getData",
                                    "properties": {"id": "sites.Politicosorg.getData", "name": "getData"},
                                    "size": 1,
                                    "usage": 4,
                                    "value": 1
                                }],
                                "id": 7383,
                                "label": "ClassOrInterface",
                                "name": "sites.Politicosorg",
                                "properties": {"id": "sites.Politicosorg", "name": "Politicosorg"},
                                "size": 1,
                                "usage": 1,
                                "value": 1
                            }, {
                                "children": [{
                                    "children": [],
                                    "id": 7378,
                                    "label": "Method",
                                    "name": "sites.MovimentoFichaLimpa.getData",
                                    "properties": {"id": "sites.MovimentoFichaLimpa.getData", "name": "getData"},
                                    "size": 2,
                                    "usage": 8,
                                    "value": 2
                                }],
                                "id": 7376,
                                "label": "ClassOrInterface",
                                "name": "sites.MovimentoFichaLimpa",
                                "properties": {"id": "sites.MovimentoFichaLimpa", "name": "MovimentoFichaLimpa"},
                                "size": 2,
                                "usage": 2,
                                "value": 2
                            }, {
                                "children": [{
                                    "children": [],
                                    "id": 7299,
                                    "label": "Method",
                                    "name": "sites.Site.lePagina",
                                    "properties": {"id": "sites.Site.lePagina", "name": "lePagina"},
                                    "size": 4,
                                    "usage": 16,
                                    "value": 4
                                }],
                                "id": 7275,
                                "label": "ClassOrInterface",
                                "name": "sites.Site",
                                "properties": {"id": "sites.Site", "name": "Site"},
                                "size": 4,
                                "usage": 4,
                                "value": 4
                            }],
                            "id": 7273,
                            "label": "Package",
                            "name": "sites",
                            "properties": {"id": "sites", "name": "sites"},
                            "size": 15,
                            "usage": 31,
                            "value": 15
                        }],
                        "id": 6208,
                        "label": "Project",
                        "name": "egrohs/Politicos",
                        "properties": {"id": "egrohs/Politicos"},
                        "size": 15,
                        "usage": 31,
                        "value": 15
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
                                    "size": 1,
                                    "usage": 9,
                                    "value": 1
                                }, {
                                    "children": [],
                                    "id": 8022,
                                    "label": "Method",
                                    "name": "hu.fnf.devel.forex.utils.MarketWebProxy.MarketWebProxy",
                                    "properties": {
                                        "id": "hu.fnf.devel.forex.utils.MarketWebProxy.MarketWebProxy",
                                        "name": "MarketWebProxy"
                                    },
                                    "size": 3,
                                    "usage": 27,
                                    "value": 3
                                }],
                                "id": 8021,
                                "label": "ClassOrInterface",
                                "name": "hu.fnf.devel.forex.utils.MarketWebProxy",
                                "properties": {
                                    "id": "hu.fnf.devel.forex.utils.MarketWebProxy",
                                    "name": "MarketWebProxy"
                                },
                                "size": 4,
                                "usage": 8,
                                "value": 4
                            }],
                            "id": 7958,
                            "label": "Package",
                            "name": "hu.fnf.devel.forex.utils",
                            "properties": {"id": "hu.fnf.devel.forex.utils", "name": "utils"},
                            "size": 4,
                            "usage": 8,
                            "value": 4
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
                                        "size": 1,
                                        "usage": 9,
                                        "value": 1
                                    }, {
                                        "children": [],
                                        "id": 8022,
                                        "label": "Method",
                                        "name": "hu.fnf.devel.forex.utils.MarketWebProxy.MarketWebProxy",
                                        "properties": {
                                            "id": "hu.fnf.devel.forex.utils.MarketWebProxy.MarketWebProxy",
                                            "name": "MarketWebProxy"
                                        },
                                        "size": 3,
                                        "usage": 27,
                                        "value": 3
                                    }],
                                    "id": 8021,
                                    "label": "ClassOrInterface",
                                    "name": "hu.fnf.devel.forex.utils.MarketWebProxy",
                                    "properties": {
                                        "id": "hu.fnf.devel.forex.utils.MarketWebProxy",
                                        "name": "MarketWebProxy"
                                    },
                                    "size": 4,
                                    "usage": 8,
                                    "value": 4
                                }],
                                "id": 7958,
                                "label": "Package",
                                "name": "hu.fnf.devel.forex.utils",
                                "properties": {"id": "hu.fnf.devel.forex.utils", "name": "utils"},
                                "size": 4,
                                "usage": 8,
                                "value": 4
                            }],
                            "id": 7955,
                            "label": "Package",
                            "name": "hu.fnf.devel.forex",
                            "properties": {"id": "hu.fnf.devel.forex", "name": "forex"},
                            "size": 4,
                            "usage": 4,
                            "value": 4
                        }],
                        "id": 6167,
                        "label": "Project",
                        "name": "csikosbalint/forex-strategy",
                        "properties": {"id": "csikosbalint/forex-strategy"},
                        "size": 4,
                        "usage": 8,
                        "value": 4
                    }], "name": "jsoup"
                },
                checked: false,
                tab: null,
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
                },
                overviewData: null,
            }
        },
        computed: {
            analysedProject: function () {
                return 'jhy/jsoup'
            }
        },
        methods: {
            onHierarchyNodeSelect: async function (node) {
                const response = await fetch(
                    'http://localhost:8080/api/v1/ast/jhy/jsoup/dependent_asts?label=' + node.node.data.label + '&id=' + node.node.data.id,
                    {
                        method: 'GET'
                    }
                )
                const stats = await response.json()
                this.forceTestData = stats["data"]
                this.dummy = stats["data"]
            }
        }
    }
</script>
