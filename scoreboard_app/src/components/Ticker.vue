<template>
  <div style="">
    <h1 style="color: #e6e6e6;">{{msg}}</h1>
      <svg viewBox="0 3 30 18">
        <rect x="5" y="3" width="20" height="18" style="fill:black;stroke-width:.2;stroke:#575757" />
        <text x="15" y="13" dominant-baseline="middle" text-anchor="middle">
          {{ count }}
        </text>
      </svg>

    <button @click="count++">Increase</button>
  </div>
</template>

<script>
export default {
  name: 'Ticker',
  props: {
    msg: String
  },
  data() {
    return {
      count: 0
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
  src: url(../assets/scorefont.otf);
}

svg text {
  font-family: clock-look;
  text-align: center;
  fill: yellow;
  stroke: solid;
  background: black;
}
</style>




