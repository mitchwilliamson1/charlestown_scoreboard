<template>
  <div style="text-align: center;">
    <div class="container">
      <div class="row align-items-center">

        <div class="col-1"></div>

        <div class="col-10 align-self-center count " :style="addstyle"> 
          {{count}}
        </div>

        <div class="col-1"></div>
      </div>
    </div>
    <button @click="count++">Increase</button>

  </div>
</template>

<script>
export default {
  name: 'Ticker',
  props: {
    msg: String,
    colour: String,
    fontSize: String,
    fontColour: String,
  },
  data() {
    return {
      count: 0
    }
  },
  computed: {
    addstyle() {
      return "font-size:"+this.fontSize+"vh; color:"+this.fontColour+";"
    }
  }
}
</script>
<style scoped type="text/css">
@font-face {
  font-family: clock-look;
  /*src: url(../assets/CursedTimerUlil-Aznm.ttf);*/
  /*src: url(../assets/Freshman-POdx.ttf);*/
  /*src: url(../assets/college.ttf);*/
  /*src: url(../assets/Graduate-Regular.ttf);*/
  src: url(../assets/scorefont1.otf);
  /*src: url(../assets/bold.otf);*/

}

.count {
  font-family: clock-look;
  color: yellow;
  font-size: 28vh;
  text-align: center;
  stroke: solid;
  background-color: black;
  line-height: 0.9;
}
</style>




