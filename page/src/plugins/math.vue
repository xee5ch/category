<template>
    <span class="category-math-plugin">
	<a v-bind:name="'category-math-plugin-link-'+id"></a>
	<div v-bind:id="'category-math-plugin-expr-'+id" class="category-math-plugin-math" v-on:click="display_syms = !display_syms" v-html="rendered"></div>
	<div class="category-math-plugin-vars" v-bind:style="get_pos(id)" v-if="display_syms">
	    <a href="#" v-on:click="display_syms = false; query = ''">[x]</a>
	    Vars:
	    <ul>
		<li v-for="e in syms">
		    <a href="#" v-on:click="query = e">{{e}}</a>
		</li>
	    </ul>
	    <div class="category-math-plugin-refs" v-if="display_syms && query != ''">
		Uses:
		<ul>
		    <li v-for="x in master.index[query]">
			<a v-bind:href="'#category-math-plugin-link-'+x">{{master.snippets[x]}}</a>
		    </li>
		</ul>
	    </div>
	</div>
    </span>
</template>
<script>
 export default {
     name: 'cat-math',
     props: ['root'],
     data () {
	 return {
	     id: '',
	     rendered: '',
	     player: null
	 };
     },
     methods: {
	 get_pos: function() {
	     var el = document.getElementById("category-math-plugin-expr-"+this.id);
	     var top = el.getBoundingClientRect().y;
	     return {'position':'absolute','left':'-25%','top':top+'px','width':'25%'};
	 }
     },
     created: function(){
	 console.log("init");
	 this.$store.dispatch("RESET_PLUGIN_DATA","math");
	 //Guppy.init({"path":"/node_modules/guppy-js","symbols":"/node_modules/guppy-js/sym/symbols.json"});
     }, 
     mounted: function(){
	 var index = 0;
	 var doc_id = node+"-"+index;
	 var content = this.root.innerHTML.trim()
	 console.log("R",this.root,content);
	 //var res = Guppy.Doc.render(content, "text");
	 var res = {doc:content};
	 var doc_data = {};
	 //doc_data[index] = res.doc.get_vars().concat(res.doc.get_symbols());
	 doc_data[index] = ["x"];
	 //res.container.setAttribute("id","category-math-container-"+doc_id);
	 //var rendered_content = (new XMLSerializer()).serializeToString(res.container);

	 
	 // Put this doc ID in the index for each var and symbol in the document
	 for(var i = 0; i < this.docs[node][index].length; i++) {
	     var v = this.docs[node][index][i];
	     if (!this.index[v]) this.index[v] = [];
	     if (this.index[v].indexOf(doc_id) < 0) this.index[v].push(doc_id);
	 }

	 // Calculate the snippet that will be associated with this expression when it appears in listings
	 var snippet = "";
	 if(this.root.previousSibling){
	     snippet += this.root.previousSibling.textContent.split(" ").slice(-4).join(" ");
	 }
	 snippet += " [formula] "

	 if(this.root.nextSibling) {
	     snippet += this.root.nextSibling.textContent.split(" ").slice(0,4).join(" ");
	 }
	 snippet = "..." + snippet + "...";
	 console.log("parprev",this.root.parentNode.previousSibling);
	 console.log("parnext",this.root.parentNode.nextSibling);
	 this.snippets[doc_id] = snippet;

	 // Finally, set up component attributes
	 this.syms = this.docs[node][index];
	 this.rendered = rendered_content;
	 this.display_syms = false;
	 this.id = doc_id;
	 this.query = "";
	 this.node = node;
     }
 }
</script>
<style scoped>
 .category-math-plugin-math {
     cursor:pointer;
     display:inline-block;
 }

 .category-math-plugin-vars {
     background-color: #dd5;
     padding:1ex;
     border: 1px solid black;
     z-index:1;
 }

 .category-math-plugin-refs {
     background-color: #ff5;
     padding:2ex 1ex;
 }
</style>
