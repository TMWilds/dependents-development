<template>
     <div id="app">
        <div class="controls">
            <div>
                <label>Adjust width</label>
                <input type="range" v-model="settings.width" min="0" max="100" />
            </div>
        </div>
        <div class="svg-container" :style="{width: settings.width + '%'}">
            <svg id="svg" pointer-events="all" viewBox="0 0 960 600" preserveAspectRatio="xMinYMin meet">
                <g :id="links"></g>
                <g :id="nodes"></g>
            </svg>
        </div>
    </div>
</template>


<script >
    import {select, event} from 'd3-selection'
    import {drag} from 'd3-drag'
    import {scaleLinear, scaleOrdinal} from 'd3-scale'
    import {forceSimulation, forceLink, forceManyBody, forceCenter} from 'd3-force'
    import {schemeCategory10} from 'd3-scale-chromatic'

    let d3 = {
          scaleLinear: scaleLinear,
          scaleOrdinal: scaleOrdinal,
          drag: drag,
          select: select,
          forceSimulation:forceSimulation,
          forceLink:forceLink,
          forceManyBody:forceManyBody,
          forceCenter:forceCenter,
          schemeCategory10: schemeCategory10,
          event: event
        }
        export default {
            name: "ForceGraph",
            data: function () {
                return {
                    graph: null,
                    simulation: null,
                    color: d3.scaleOrdinal(d3.schemeCategory10),
                    settings: {
                        strokeColor: "#29B5FF",
                        width: 100,
                        svgWigth: 960,
                        svgHeight: 600
                    }
                };
            },
            mounted: function () {
                var that = this;
                console.log("mounted");
                that.graph = {
    "nodes": [
        {
            "id": "Alice"
        },
        {
            "id": "Bob"
        },
        {
            "id": "Carol"
        }
    ],
    "links": [
        {
            "source": 0,
            "target": 1
        },
        {
            "source": 1,
            "target": 2
        }
    ]
};
                console.log("json");
                that.simulation = d3.forceSimulation(that.graph.nodes)
                    .force("link", d3.forceLink(that.graph.links).distance(100).strength(0.1))
                    .force("charge", d3.forceManyBody())
                    .force("center", d3.forceCenter(that.settings.svgWigth / 2, that.settings.svgHeight / 2));
            },
            computed: {
                nodes: function () {
                    var that = this;
                    if (that.graph) {
                        return d3.select("svg").append("g")
                            .attr("class", "nodes")
                            .selectAll("circle")
                            .data(that.graph.nodes)
                            .enter().append("circle")
                            .attr("r", 20)
                            .attr("fill", function (d ,i) {
                                return that.color(i);
                            })
                            .call(d3.drag()
                                .on("start", function dragstarted(d) {
                                    if (!d3.event.active) that.simulation.alphaTarget(0.3).restart();
                                    d.fx = d.x;
                                    d.fy = d.y;
                                })
                                .on("drag", function dragged(d) {
                                    d.fx = d3.event.x;
                                    d.fy = d3.event.y;
                                })
                                .on("end", function dragended(d) {
                                    if (!d3.event.active) that.simulation.alphaTarget(0);
                                    d.fx = null;
                                    d.fy = null;
                                }));
                    }
                },
                links: function () {
                    var that = this;
                    if (that.graph) {
                        return d3.select("svg").append("g")
                            .attr("class", "links")
                            .selectAll("line")
                            .data(that.graph.links)
                            .enter().append("line")
                            .attr("stroke-width", function (d) { return Math.sqrt(d.value); });
                    }
                },

            },
            updated: function () {
                var that = this;
                that.simulation.nodes(that.graph.nodes).on('tick', function ticked() {
                    that.links
                        .attr("x1", function (d) { return d.source.x; })
                        .attr("y1", function (d) { return d.source.y; })
                        .attr("x2", function (d) { return d.target.x; })
                        .attr("y2", function (d) { return d.target.y; });

                    that.nodes
                        .attr("cx", function (d) { return d.x; })
                        .attr("cy", function (d) { return d.y; });
                });
            }
        }
    </script>