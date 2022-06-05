<template>

  <div class="container">
    <div class="row align-items-center teamAndTime">
      
      <div class="col-6 align-self-center shadow p-1 mb-5 rounded">
          <div class="txt">D K</div>
          <!-- <img class="logo" src="../assets/Jets.png" style="background-color: white;"> -->
      </div>
      <div class="col-6 align-self-center shadow p-1 mb-5 rounded">
        <div style="height: 100%;" class="ticker">
          <Ticker msg="Team Name" fontSize="35" colour="black"/>
        </div>
      </div>
    </div>

    <div class="row align-items-center scores">
      <div class="col-6 align-self-center shadow p-1 mb-5 rounded">
          <div class="txt">M W</div>
          <!-- <img class="logo" src="../assets/tigers.jpg"> -->
      </div>
      <div class="col-6 align-self-center shadow p-1 mb-5 rounded">
        <div style="height: 100%;" class="ticker">
          <Ticker msg="Team Name" fontSize="35" colour="red"/>
        </div>
      </div>
    </div>
    <div class="row align-items-center scores">
      <div class="col-6 align-self-center shadow p-1 mb-5 rounded ends">
        ENDS
      </div>
      <div class="col-6 align-self-center shadow p-1 mb-5 rounded">
        <Ticker msg="ENDS" fontSize="15" fontColour="white" colour="black"/>
      </div>
    </div>
  </div>

</template>

<script>
import Ticker from './Ticker.vue'


export default {
  name: 'Board',
  components: {
    Ticker,
  }
}
</script>

<style scoped type="text/css">
@font-face {
  font-family: bigText;
  /*src: url(../assets/CursedTimerUlil-Aznm.ttf);*/
  /*src: url(../assets/Freshman-POdx.ttf);*/
  /*src: url(../assets/college.ttf);*/
  /*src: url(../assets/Graduate-Regular.ttf);*/
  src: url(../assets/bold.otf);
}


.row {
    background-color: #363535;
    /*height:50vh;*/
}

.txt {
  font-family: bigText;
  color: white;
  font-size: 32vh;
  text-align: center;
  line-height: 1.0;
}

.ends {
  font-family: bigText;
  color: white;
  font-size: 15vh;
  text-align: center;
  line-height: 1.0;
}

img {
  width: 60%;
  display: block;
  margin-left: auto;
  margin-right: auto;
}


</style>
