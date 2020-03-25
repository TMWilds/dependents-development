<template>
    <div style="overflow-x: scroll; overflow-y: scroll" >
    <div :class="'tree'+this._uid" style="height: inherit;">
        <svg id="graph"></svg>
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
        linkVertical: linkVertical
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
            const [viewport] = this.$el.getElementsByClassName("tree"+this._uid);
            this.width = viewport.clientWidth;
            this.height = viewport.clientHeight;
            this.render()
        },
        watch: {
          data (newData, oldData) {
              console.log("data changed");
              // this.simulation.stop();
              d3.select("#graph").selectAll("*").remove();
              this.$nextTick(() => {
                  this.render()
              });
          }
        },
        methods: {
            render: function () {
                  const width = 500
                  function tree(data) {
                  const root = d3.hierarchy(data);
                  root.dx = 10;
                  root.dy = width / (root.height + 1);
                  return d3.tree().nodeSize([root.dx, root.dy])(root);
                }
                const root = tree(this.data);


  let x0 = Infinity;
  let x1 = -x0;
  root.each(d => {
    if (d.x > x1) x1 = d.x;
    if (d.x < x0) x0 = d.x;
  });

  const svg = d3.select("#graph")
      .attr("viewBox", [0, 0, width, x1 - x0 + root.dx * 2]);

  const g = svg.append("g")
      .attr("font-family", "sans-serif")
      .attr("font-size", 10)
      .attr("transform", `translate(${root.dy / 3},${root.dx - x0})`);

  const link = g.append("g")
    .attr("fill", "none")
    .attr("stroke", "#555")
    .attr("stroke-opacity", 0.4)
  .selectAll("path")
    .data(root.links())
    .join("path")
      .attr("d", d3.linkHorizontal()
          .x(d => d.y)
          .y(d => d.x))
      .attr("stroke-width", d => Math.log10(d.target.value) * 2);



  const node = g.append("g")
      .attr("stroke-linejoin", "round")
      .attr("stroke-width", 3)
    .selectAll("g")
    .data(root.descendants())
    .join("g")
      .attr("transform", d => `translate(${d.y},${d.x})`);

  node.append("circle")
      .attr("fill", d => d.children ? "#555" : "#999")
      .attr("r", 2.5);

  node.append("text")
      .attr("dy", "0.31em")
      .attr("x", d => d.children ? -3 : 3)
      .attr("text-anchor", d => d.children ? "end" : "start")
      .text(d => d.data.name)
    .clone(true).lower()
      .attr("stroke", "white")
      .append("title")
      .text(d => d.data.value + ' calls to selected dependent');

  node.append("title")
    .text(d => d.data.value + ' calls to selected dependent');

  return svg.node();
            }
        }
    }
</script>