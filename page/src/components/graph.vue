<template>
    <div class="graph_index">
	<div id="graph_container"></div>
    </div>
</template>

<script>
 import {DirectedGraph} from 'graphology';
 import FA2 from 'graphology-layout-forceatlas2';
 import FA2Layout from 'graphology-layout-forceatlas2/worker';
 import WebGLRenderer from 'sigma/renderers/webgl';
 
 import { mapState } from 'vuex'
 import { mapGetters } from 'vuex'
 
 export default {
     name: 'graph-index',
     props: ['nodeset','highlight'],
     computed: {
	 num_nodes: function() {
	     var ans = 0;
	     for(var id in this.nodeset) {
		 ans++;
	     }
	     return ans;
	 },
	 subgraph: function() {
	     return this.graph.subgraph(this.nodeset);
	 },
	 graph_data: function() {
	     return this.subgraph.sigma_graph();
	 },
	 ...mapState([
	     'graph'
	 ]),
	 ...mapGetters(['sorted','sortedby'])
     },
     watch: {
	 nodeset: function(val) {
	     this.$nextTick(function () {
		 this.update_graph();
	     });
	 },
	 highlight: function(val) {
	     this.$nextTick(function () {
		 this.update_highlight();
	     });
	 }
     },
     methods: {
	 label_neighbours: function(n, label) {
	     var ans = [];
	     var tgts = this.nodes[n].edges[this.mode == 'menu' ? 'has' : 'is'][label];
	     for(var i = 0; i < tgts.length; i++) {
		 var m = tgts[i].target;
		 console.log(m);
		 if(m in this.nodeset) ans.push(m);
	     }
	     console.log(ans);
	     return ans;
	 },
	 update_graph: function() {
	     if(this.layout) {
		 this.layout.stop();
		 this.layout = null;
	     }
	     if(this.layout_timer) {
		 clearTimeout(this.layout_timer);
		 this.layout_timer = null;
	     }
	     this.graph_display.clear();
	     this.graph_display.import(this.graph_data);
	     this.graph_display.nodes().forEach(node => {
		 this.graph_display.mergeNodeAttributes(node, {
		     x: Math.random(),
		     y: Math.random(),
		     size: Math.max(3,Math.min(this.graph_display.degree(node), 8)),
		     color: node in this.highlight ? "#f00" : "#00f"
		 });
	     });
	     
	     var settings = FA2.inferSettings(this.graph_display);
	     console.log(settings);
	     settings.slowDown = 10;
	     //saneSettings.strongGravityMode = true;
	     //saneSettings.gravity = 3;
	     this.layout = new FA2Layout(this.graph_display, {settings: settings});
	     this.layout.start();
	     var self = this;
	     this.layout_timer = setTimeout(function(){self.layout.stop(); self.layout.kill(); self.layout = null; self.layout_timer = null;}, Math.max(10, 3+(this.num_nodes/100)*1000));
	 },
	 update_highlight: function() {
	     console.log("updating highlight",this.highlight);
	     this.graph_display.nodes().forEach(node => {
		 console.log("N",node, node in this.highlight);
		 this.graph_display.mergeNodeAttributes(node, {color: node in this.highlight ? "#f00" : "#00f"});
	     });
	     
	 }
     },
     mounted: function () {
	 this.$nextTick(function () {
	     console.log("initing graph container");
	     this.graph_display = new DirectedGraph({multi: true});
	     this.renderer = new WebGLRenderer(this.graph_display, document.getElementById("graph_container"), {
		 defaultEdgeType: 'arrow',
		 defaultEdgeColor: '#888',
		 renderEdgeLabels: true,
		 labelSize: 12,
		 labelGrid: {
		     cell: {
			 width: 40,
			 height: 20
		     },
		     renderedSizeThreshold: 1}});
	     const camera = this.renderer.getCamera();
	     const captor = this.renderer.getMouseCaptor();

	     // State
	     let draggedNode = null, dragging = false;

	     var self = this;
	     
	     /* this.renderer.on('downNode', (e) => {
		dragging = true;
		console.log("down",e);
		draggedNode = e.node;
		camera.disable();
		});
	      */
	     this.renderer.on('clickNode', (e) => {
		 console.log("nav",e.node,e);
		 //this.$router.push("/node/"+e.node);
		 if(e.captor.ctrlKey) {
		     this.$emit("selectedNode",e.node);
		 }
		 else {
		     this.$emit("clickedNode",e.node);
		 }
	     });
	     
	     /* this.renderer.on('doubleClickNode', (e) => {
		console.log("nav",e.node);
		//this.$router.push("/node/"+e.node);
		this.$emit("doubleClickedNode",e.node);
		});*/

	     /* captor.on('mouseup', e => {
		dragging = false;
		console.log("up",e);
		draggedNode = null;
		camera.enable();
		});*/

	     /* captor.on('mousemove', e => {
		if (!dragging)
		return;

		// Get new position of node
		const pos = self.renderer.normalizationFunction.inverse(
		camera.viewportToGraph(self.renderer, e.x, e.y)
		);

		self.graph_display.setNodeAttribute(draggedNode, 'x', pos.x);
		self.graph_display.setNodeAttribute(draggedNode, 'y', pos.y);
		});*/

	     this.update_graph();
	     this.update_highlight();
	 });
     }
 }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
 .graph_index {
     height: 80%;
     min-height:80vh;
     width: 100%;
 }
 #graph_container {
     height: 80%;
     min-height:80vh;
     width: 100%;
     color: unset;
     border: 1px solid #ccc;
 }
</style>
