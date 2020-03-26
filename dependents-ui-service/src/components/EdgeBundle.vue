<template>
    <div class="outer">
        <div class="inner-left" style="margin-top: 2rem">
            <h4> Analysed Project </h4>
            <p><span style="color: #ff5c45"> ⬤ </span> <span> {{analysedProject}} </span></p>
            <h4> Dependent Projects </h4>
            <div v-for="project in projectList">
                <input type="checkbox" :id="project" :value="project" v-model="filteredProjects">
                <label :for="project"><span :style="{color: projectColours[project]}"> ⬤ {{project}} </span></label>
            </div>
        </div>
        <div id="bundle" class="inner-right">
        </div>
    </div>
</template>

<script>

    import {select, selectAll} from 'd3-selection'
    import {interpolateViridis} from 'd3-scale-chromatic'
    import {hierarchy, cluster} from 'd3-hierarchy'
    import {lineRadial, curveBundle} from 'd3-shape'
    import {ascending} from 'd3-array'


    export const d3 = {
        select: select,
        selectAll: selectAll,
        hierarchy: hierarchy,
        lineRadial: lineRadial,
        curveBundle: curveBundle,
        cluster: cluster,
        ascending: ascending,
        interpolateViridis: interpolateViridis,
    }

    export default {
        name: "EdgeBundle",
        props: {
            callData: {
                type: Array,
                required: true,
            },
            analysedProject: {
                type: String,
                required: true,
            },
        },
        data: function () {
            return {
                filteredProjects: [],
            }
        },
        mounted: function () {
            this.filteredProjects = this.projectList
        },
        watch: {
            filteredCallData(newData, oldData) {
                console.log("data changed");

                d3.select("#bundle").selectAll("*").remove();

                this.$nextTick(() => {
                    this.render(newData)
                });
            }
        },
        computed: {
            projectList: function () {
                let projectSet = new Set();
                for (const datum of this.callData) {
                    if (datum.project !== this.analysedProject) {
                        projectSet.add(datum.project)
                    }
                }
                return Array.from(projectSet)
            },
            projectColours: function () {
                const output = {}
                const colourSelectInterval = 1 / this.projectList.length
                const projects = this.projectList
                for (const [index, project] of projects.entries()) {
                    output[project] = d3.interpolateViridis(index * colourSelectInterval)
                }
                output[this.analysedProject] = "#ff5c45"
                return output
            },
            filteredCallData: function () {
                const copy = this.callData.slice()
                return copy.filter(obj => this.filteredProjects.includes(obj.project) || obj.project === this.analysedProject)
            }
        },
        methods: {
            render: async function (callData) {
                const newData = JSON.parse(JSON.stringify(this.filteredCallData))
                const data = hierarchy(newData);

                function hierarchy(data, delimiter = ".") {
                    let root;
                    const map = new Map;
                    data.forEach(function find(data) {
                        const {name} = data;
                        if (map.has(name)) return map.get(name);
                        const i = name.lastIndexOf(delimiter);
                        map.set(name, data);
                        if (i >= 0) {
                            find({name: name.substring(0, i), children: []}).children.push(data);
                            data.name = name.substring(i + 1);
                        } else {
                            root = data;
                        }
                        return data;
                    });
                    return root;
                }

                function bilink(root) {
                    const map = new Map(root.leaves().map(d => [id(d), d]));
                    for (const d of root.leaves()) d.incoming = [], d.outgoing = d.data.imports.map(i => [d, map.get(i)]);
                    for (const d of root.leaves()) for (const o of d.outgoing) o[1].incoming.push(o);
                    return root;
                }

                function id(node) {
                    return `${node.parent ? id(node.parent) + "." : ""}${node.data.name}`;
                }

                const colours = this.projectColours


                function overed(d) {
                    link.style("mix-blend-mode", null);
                    d3.select(this).attr("font-weight", "bold");
                    d3.selectAll(d.incoming.map(d => d.path)).attr("stroke", colorin).raise();
                    d3.selectAll(d.incoming.map(([d]) => d.text)).attr("fill", colorin).attr("font-weight", "bold");
                    d3.selectAll(d.outgoing.map(d => d.path)).attr("stroke", colorout).raise();
                    d3.selectAll(d.outgoing.map(([, d]) => d.text)).attr("fill", colorout).attr("font-weight", "bold");
                }

                function outed(d) {
                    link.style("mix-blend-mode", "multiply");
                    d3.select(this).attr("font-weight", null);
                    d3.selectAll(d.incoming.map(d => d.path)).attr("stroke", null);
                    d3.selectAll(d.incoming.map(([d]) => d.text)).attr("fill", d => colours[d.data.project]).attr("font-weight", null);
                    d3.selectAll(d.outgoing.map(d => d.path)).attr("stroke", null);
                    d3.selectAll(d.outgoing.map(([, d]) => d.text)).attr("fill", d => colours[d.data.project]).attr("font-weight", null);
                }

                const colorin = "#00f"
                const colorout = "#f00"
                const colornone = "#ccc"
                const width = 500
                const radius = width / 2

                let line = d3.lineRadial()
                    .curve(d3.curveBundle.beta(0.85))
                    .radius(d => d.y)
                    .angle(d => d.x)
                const analysedProject = this.analysedProject
                let tree = d3.cluster()
                    .size([2 * Math.PI, radius - 100])
                    .separation(function separation(a, b) {
                        if (a.data.project === b.data.project) {
                            return 1
                        } else if (a.data.project === analysedProject || b.data.project === analysedProject) {
                            return 5
                        } else {
                            return 3
                        }
                    })


                const root = tree(bilink(d3.hierarchy(data)
                    .sort((a, b) => d3.ascending(a.height, b.height) || d3.ascending(a.data.name, b.data.name))));

                const svg = d3.select("#bundle").append("svg")
                    .attr("viewBox", [-width / 2, -width / 2, width, width]);

                let node = svg.append("g")
                    .attr("font-family", "sans-serif")
                    .attr("font-size", 10)
                    .selectAll("g")
                    .data(root.leaves())
                    .join("g")
                    .attr("transform", d => `rotate(${d.x * 180 / Math.PI - 90}) translate(${d.y},0)`)

                node.append("text")
                    .attr("dy", "0.31em")
                    .attr("x", d => d.x < Math.PI ? 15 : -15)
                    .attr("text-anchor", d => d.x < Math.PI ? "start" : "end")
                    .attr("transform", d => d.x >= Math.PI ? "rotate(180)" : null)
                    .text(d => d.data.name)
                    .each(function (d) {
                        d.text = this;
                    })
                    .on("mouseover", overed)
                    .on("mouseout", outed)
                    .call(text => text.append("title").text(d => `${id(d)}
${d.outgoing.length} outgoing
${d.incoming.length} incoming`))

                node.append("text")
                    .attr("dy", "0.31em")
                    .attr("x", d => d.x < Math.PI ? 6 : -6)
                    .attr("text-anchor", d => d.x < Math.PI ? "start" : "end")
                    .attr("transform", d => d.x >= Math.PI ? "rotate(180)" : null)
                    .attr("fill", d => colours[d.data.project])
                    .attr("font-weight", "bold")
                    .text(d => "●")
                    .each(function (d) {
                        d.text = this;
                    })
                    .on("mouseover", overed)
                    .on("mouseout", outed)
                    .call(text => text.append("title").text(d => `${id(d)}
${d.outgoing.length} outgoing
${d.incoming.length} incoming`))

                const link = svg.append("g")
                    .attr("stroke", colornone)
                    .attr("fill", "none")
                    .selectAll("path")
                    .data(root.leaves().flatMap(leaf => leaf.outgoing))
                    .join("path")
                    .style("mix-blend-mode", "multiply")
                    .attr("d", ([i, o]) => line(i.path(o)))
                    .each(function (d) {
                        d.path = this;
                    });
                return svg.node();

            }
        }
    }
</script>

<style scoped>
 div.outer {
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -ms-flex-wrap: wrap;
    flex-wrap: wrap;
    -webkit-box-flex: 1;
    -ms-flex: 1 1 auto;
    flex: 1 1 auto;
    margin-right: -12px;
    margin-left: -12px;
 }

    div.inner-left {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 50%;
    flex: 0 0 20%;
    max-width: 20%;
    }

    div.inner-right {
            -webkit-box-flex: 0;
    -ms-flex: 0 0 50%;
    flex: 0 0 80%;
    max-width: 80%;
    }


</style>