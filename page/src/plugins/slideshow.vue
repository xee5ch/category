<template>
    <div class="category-slideshow">
	<span :class="current_index == index && !all ? 'category-slideshow-button category-slideshow-button-current' : 'category-slideshow-button category-slideshow-button-other'" v-for="(s,index) in slides" v-on:mouseover="tmp_set_index(index)" v-on:mouseout="reset_index()" v-on:click="set_index(index)">
	    {{index}}
	</span>
	<span :class="all ? 'category-slideshow-button category-slideshow-button-current' : 'category-slideshow-button category-slideshow-button-other'" v-on:click="all=!all">
	    all
	</span>
	<div class="category-slideshow-slide" v-html="slides[current_index]" v-if="!all">
	</div>
	<div class="category-slideshow-slide" v-for="(s,index) in slides" v-if="all" v-html="s">
	</div>
    </div>
</template>
<script>
 export default {
     name: 'cat-slideshow',
     props: ['root'],
     data() {
	 return {
	     current_index: 0,
	     lock_index: 0,
	     init_index: 0,
	     all: false,
	     slides: [],
	 };
     },
     mounted: function() {
	 var doc = this.root;
	 var elements = [];

	 // Iterate through li nodes and extract these as the slides
	 for(var n = doc.firstChild.firstChild; n != null; n = n.nextSibling){
	     if(n.nodeName.toLowerCase() == "li") elements.push(n.innerHTML);
	 }
	 
	 this.slides = elements;
     },
     methods: {
	 tmp_set_index: function(idx){
	     this.current_index = idx;
	 },
	 reset_index: function(){
	     this.current_index = this.lock_index;
	 },
	 set_index: function(idx){
	     this.all = false;
	     this.lock_index = idx;
	     this.current_index = idx;
	 }
     }
 }
</script>

<style scoped>
 .category-slideshow {
     text-align:center;
     width:100%;
     overflow-x:scroll;
 }

 .category-slideshow-slide >>> img {
     max-width: 100% !important;
 }
 
 .category-slideshow-slide {
     text-align:center;
 }

 .category-slideshow-caption {
     text-align:center;
     margin:auto;
     width:80%;
 }

 .category-slideshow-button {
     width:2em;
     display:inline-block;
     height:2em;
     border:2px solid black;
     text-align:center;
     cursor:pointer;
     margin:.5ex 0;
 }

 .category-slideshow-button-other {
     background-color:#ccc;
 }

 .category-slideshow-button-current {
     background-color:#8cf;
 }
</style>
