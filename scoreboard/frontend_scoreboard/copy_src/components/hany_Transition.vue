<template>
  <div class="transition"></div>
  <div class="content">
    <h1>Heading title</h1>
    <p>Lorem ipsum dolor sit amet</p>
    {{count}}
    <button class="cta" @click="e => e.target.classList.toggle('anim-trans')" >button
</button>
    <!-- <Board></Board> -->

  </div>

</template>

<script>
import Board from './Board.vue'


export default {
  name: 'Frame',
  components: {
    Board,
  },
  data() {
    return {
      count: 0
    }
  },
  methods: {
    increment() {
      this.count++
      $( ".cta" ).click(function() {
      $( ".transition").toggleClass( "anim-trans" );
        });
    }
  },
  // mounted() {
  //   this.increment()
  // }
}
</script>
<style scoped type="text/css">
* {
  padding:0;
  margin:0;
}

body {
  background:#fff;
  overflow-x:hidden;
  font-family:arial;
}

.transition {
  position:absolute;
  height:100%;
  width:30%;
  background:#d6d6d6;
  transform: skewX(-5deg) translateX(-50px);
  transition:2s all ease-in-out;
  -webkit-transition:2s all ease-in-out;
}

.content {
  position:relative;
  padding:200px 0 0 200px;
  color:#000;
  z-index:10;
  height:300px;
}

.cta {
  outline:none;
  border:none;
  text-decoration:none;
  text-transform:uppercase;
  background:#202020;
  color:#eaeaea;
  box-sizing:border-box;
  margin-top:20px;
  padding:10px 40px;
}

.anim-trans {
  animation: anim 4s ease-in-out;
  }

@keyframes anim{
     0% { }
     20%  { z-index:11;\transform: skewX(5deg) translateX(-100%); }
     40%   { transform: skewX(0deg) translateX(0);
 width:100%; z-index:11; box-shadow: 10px 10px 5px #eaeaea;}
     60%   { transform: skewX(3deg) translateX(0);
 width:100%;z-index:11; box-shadow: 10px 10px 5px #eaeaea;}
     80%   { transform: skewX(1deg) translateX(-100%);
 width:60%;z-index:11; box-shadow: 10px 10px 5px #eaeaea;}
     100%   { transform: skewX(-5deg) translateX(-50px);
 width:30%;z-index:1; box-shadow: none;}
}
</style>
