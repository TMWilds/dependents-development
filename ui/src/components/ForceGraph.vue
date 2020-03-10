<template>
    <div v-if="show" id="app">
        <svg id="graph"></svg>
        <!--        <div class="controls">-->
        <!--            <div>-->
        <!--                <label>Adjust width</label>-->
        <!--                <input type="range" v-model="settings.width" min="0" max="100" />-->
        <!--            </div>-->
        <!--        </div>-->
        <!--        <div class="svg-container" :style="{width: settings.width + '%'}">-->
        <!--            <svg id="svg" pointer-events="all" viewBox="0 0 960 600" preserveAspectRatio="xMinYMin meet">-->
        <!--                <g :id="links"></g>-->
        <!--                <g :id="nodes"></g>-->
        <!--            </svg>-->
        <!--        </div>-->
    </div>
</template>


<script>
    import {select, create, event} from 'd3-selection'
    import {drag} from 'd3-drag'
    import {scaleLinear, scaleOrdinal} from 'd3-scale'
    import {forceSimulation, forceLink, forceManyBody, forceCenter, forceX, forceY} from 'd3-force'
    import {schemeCategory10} from 'd3-scale-chromatic'
    import {hierarchy} from 'd3-hierarchy'

    const getEvent = () => event;

    export const d3 = {
        scaleLinear: scaleLinear,
        scaleOrdinal: scaleOrdinal,
        drag: drag,
        select: select,
        forceSimulation: forceSimulation,
        forceLink: forceLink,
        forceManyBody: forceManyBody,
        forceCenter: forceCenter,
        schemeCategory10: schemeCategory10,
        event: getEvent,
        hierarchy: hierarchy,
        create: create,
        forceX: forceX,
        forceY: forceY
    }
    export default {
        name: "ForceGraph",
        // data: function () {
        // },
        props: {
            data: {
                type: Object,
                required: true,
            }
        },
        data: function() {
            return {
                simulation: null,
                show: true
            }
        },
        mounted: function () {
            this.render()
        },
        watch: {
          data (newData, oldData) {
              console.log("data changed");
              this.simulation.stop();
              d3.select("#graph").selectAll("*").remove();
              this.$nextTick(() => {
                  this.render()
              });
          }
        },
        methods: {
            render: function () {
                const height = 600
                const width = 600

                const drag = simulation => {

                    function dragstarted(d) {
                        if (!d3.event().active) simulation.alphaTarget(0.3).restart();
                        d.fx = d.x;
                        d.fy = d.y;
                    }

                    function dragged(d) {
                        d.fx = d3.event().x;
                        d.fy = d3.event().y;
                    }

                    function dragended(d) {
                        if (!d3.event().active) simulation.alphaTarget(0);
                        d.fx = null;
                        d.fy = null;
                    }

                    return d3.drag()
                        .on("start", dragstarted)
                        .on("drag", dragged)
                        .on("end", dragended);
                }

                const root = d3.hierarchy(this.data);
                const links = root.links();
                const nodes = root.descendants();

                const simulation = d3.forceSimulation(nodes)
                    .force("link", d3.forceLink(links).id(d => d.id).distance(0).strength(1))
                    .force("charge", d3.forceManyBody().strength(-50))
                    .force("x", d3.forceX())
                    .force("y", d3.forceY());

                this.simulation = simulation;

                const svg = d3.select("#graph")
                    .attr("viewBox", [-width / 2, -height / 2, width, height]);
                console.log(svg)

                const link = svg.append("g")
                    .attr("stroke", "#999")
                    .attr("stroke-opacity", 0.6)
                    .selectAll("line")
                    .data(links)
                    .join("line");

                const node = svg.append("g")
                    .attr("fill", "#fff")
                    .attr("stroke", "#000")
                    .attr("stroke-width", 1.5)
                    .selectAll("circle")
                    .data(nodes)
                    .join("circle")
                    .attr("fill", d => d.children ? null : "#000")
                    .attr("stroke", d => d.children ? null : "#fff")
                    .attr("r", 3.5)
                    .call(drag(simulation));

                node.append("title")
                    .text(d => d.data.name);

                simulation.on("tick", () => {
                    link
                        .attr("x1", d => d.source.x)
                        .attr("y1", d => d.source.y)
                        .attr("x2", d => d.target.x)
                        .attr("y2", d => d.target.y);

                    node
                        .attr("cx", d => d.x)
                        .attr("cy", d => d.y);
                });

                // invalidation.then(() => simulation.stop());

                return svg.node();
            }
        }
    }
</script>