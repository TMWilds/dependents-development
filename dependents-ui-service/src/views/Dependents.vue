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
                <edge-bundle style="max-width: 1000px;" v-if="overviewData" :analysed-project="analysedProject" :call-data="overviewData"/>
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
                                        <tspan :x="x" dy="1em">{{ tile.data.value }} call{{tile.data.value !== 1 ? 's':''}} to analysed entity</tspan>
                                        <tspan :x="x" dy="1em">Calls {{ tile.data.distinct_usage }} distinct method{{tile.data.distinct_usage !== 1 ? 's':''}}</tspan>
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
                this.url+'/api/v1/project/'+this.analysedProject+'/retrieve/hierarchy',
                {
                    method: 'GET'
                }
            )
            const stats = await response.json()
            this.hiearchyData = stats["data"]

            const responseCalls = await fetch(
                this.url+'/api/v1/project/'+this.analysedProject+'/retrieve/project_calls',
                {
                    method: 'GET'
                }
            )
            const statsCalls = await responseCalls.json()
            this.overviewData = statsCalls["data"]
        },
        data: function () {
            return {
                dummy: null,
                checked: false,
                tab: null,
                checkedRel: false,
                hiearchyData: null,
                forceTestData: null,
                overviewData: null,
            }
        },
        computed: {
            analysedProject: function () {
                return this.$route.params.group + '/' + this.$route.params.project
            },
            url: function () {
                return window.location.protocol + '//' + window.location.hostname + ':' +  window.location.port + '/'
            }
        },
        methods: {
            onHierarchyNodeSelect: async function (node) {
                const response = await fetch(
                    this.url+'/api/v1/ast/' + this.analysedProject + '/dependent_asts?label=' + node.node.data.label + '&id=' + node.node.data.id,
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
