<template>
    <div style="overflow-x: scroll; overflow-y: scroll" >
    <div :class="'app'+this._uid" style="height: inherit;">
        <svg :id="'graph'+this._uid"></svg>
    </div>
    </div>
</template>


<script>
    import {select, create, event} from 'd3-selection'
    import {drag} from 'd3-drag'
    import {scaleLinear, scaleOrdinal} from 'd3-scale'
    import {forceSimulation, forceLink, forceManyBody, forceCenter, forceX, forceY} from 'd3-force'
    import {schemeCategory10} from 'd3-scale-chromatic'
    import {hierarchy, tree} from 'd3-hierarchy'
    import {linkHorizontal, linkVertical} from 'd3-shape'
    import {interpolateCool} from 'd3-scale-chromatic'

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
        forceY: forceY,
        tree: tree,
        linkHorizontal: linkHorizontal,
        linkVertical: linkVertical,
        interpolateCool: interpolateCool
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
                width: null,
                height: null
            }
        },
        mounted: function () {
            const [viewport] = this.$el.getElementsByClassName("app"+this._uid);
            this.width = viewport.clientWidth;
            this.height = viewport.clientHeight;
            this.render()
        },
        watch: {
          data (newData, oldData) {
              console.log("data changed");
              // this.simulation.stop();
              d3.select("#graph" + this._uid).selectAll("*").remove();
              this.$nextTick(() => {
                  this.render()
              });
          }
        },
        computed: {
            projectList: function () {
                let projectSet = new Set();
                for (const datum of this.data.children) {
                        projectSet.add(datum.project)
                }
                return Array.from(projectSet)
            },
            projectColours: function () {
                const output = {}
                const colourSelectInterval = 1 / this.projectList.length
                const projects = this.projectList
                for (const [index, project] of projects.entries()) {
                    output[project] = d3.interpolateCool(index * colourSelectInterval)
                }
                return output
            },
        },
        methods: {
            render: function () {
                // const height = 600
                // const width = 600

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
                    .force("link", d3.forceLink(links).id(d => d.id).distance(1).strength(1))
                    .force("charge", d3.forceManyBody().strength(-150))
                    .force("x", d3.forceX())
                    .force("y", d3.forceY());

                this.simulation = simulation;

                const svg = d3.select("#graph" + this._uid)
                    .attr("viewBox", [-this.width / 2, -this.height / 2, this.width, this.height]);
                console.log(svg)

                const link = svg.append("g")
                    .attr("stroke", "#000000")
                    .attr("stroke-opacity", 0.6)
                    .selectAll("line")
                    .data(links)
                    .join("line")
                    .attr("stroke-width", d => Math.log10(d.target.value) * 2);


                link.append("title")
                    .text(d => 'Dependent calls ' +  d.target.value);

                console.log(links)

                const colors = this.projectColours

                const node = svg.append("g")
                    .attr("stroke-width", 1.5)
                    .selectAll("circle")
                    .data(nodes)
                    .join("circle")
                    .attr("fill", d => colors[d.data.project])
                    .attr("stroke", d => d.children ? "#000" : "#fff")
                    .attr("r", 6.5)
                    .call(drag(simulation));

                node.append("title")
                    .text(d => d.data.name);

                const text = svg.append("g")
                    .attr("stroke", "#999")
                    .attr("stroke-opacity", 0.6)
                    .selectAll("text")
                    .data(nodes)
                    .join("text")
                    .attr("fill", "black")
                    .style("font-size", "12")// <=== Set the fill
                    .text(d => !d.children ? d.data.name : '')
                    .call(drag(simulation));

                simulation.on("tick", () => {
                    link
                        .attr("x1", d => d.source.x)
                        .attr("y1", d => d.source.y)
                        .attr("x2", d => d.target.x)
                        .attr("y2", d => d.target.y);

                    node
                        .attr("cx", d => d.x)
                        .attr("cy", d => d.y);

                    text
                        .attr("x", d => d.x - 10)
                        .attr("y", d => d.y - 10);
                });

                // invalidation.then(() => simulation.stop());

                return svg.node();
            },
        }
    }
</script>