<template>
  <div v-if="this.details" class="container-fluid h-100 w-100 p-0" style="background-color: black;">
    <div class="container-fluid h-100 w-100">
      <div class="row h-25 align-items-center bg-primary">
        <div class="col-6 h-100 text-justify rounded">
          <img class="logo" src="../assets/logos/tigers.jpg">
        </div>
        <div class="col-6 h-100 text-justify rounded">
          <img class="logo"  src="../assets/logos/Jets.png">
        </div>
      </div>
      <div class="row h-25 bg-success"></div>
      <div class="row h-25 bg-danger"></div>
      <div class="row h-25 bg-warning"></div>
    </div>

    <div class="row h-25 align-items-center">
      <div class="col text-justify rounded">
          <!-- <div class="txt">{{details.competitors[1].first_name.charAt(0)}}{{details.competitors[0].last_name.charAt(0)}}</div> -->
          <img class="logo" src="../assets/logos/tigers.jpg">
      </div>
      <div class="col text-justify rounded">
          <!-- <div class="txt">{{details.competitors[0].first_name.charAt(0)}}{{details.competitors[1].last_name.charAt(0)}}</div> -->
          <img class="logo" src="../assets/logos/Jets.png" >
      </div>
    </div>

    <div class="row h-25 align-items-center scores">
    <div class=""></div>
      <div class="col text-justify mb-5 rounded">
        <div class="ticker">
          <Ticker :player="details.competitors[0]" 
                  :details="details"
                  fontSize="20" 
                  colour="red"/>
        </div>
      </div>
      <div class="col text-justify mb-5 rounded">
        <div class="ticker">
          <Ticker :player="details.competitors[1]" 
                  :details="details"
                  fontSize="20" 
                  colour="black"/>
        </div>
      </div>
    </div>

    <div class="row h-25 align-items-center scores">
      <div class="col align-self-center mb-5rounded ends">
        <img class="logo" src="../assets/adds/belle_property.png" style="background-color: white; width: 80%;">
      </div>
    </div>

    <div class="row h-25 align-items-center scores">
      <div class="col align-self-center mb-5 rounded">
        {{ends}}
        <Ticker :details="details"
                :endsProp="ends"
                player="ends" 
                fontSize="20" 
                fontColour="white" 
                colour="black"/>
      </div>
    </div>
  </div>

</template>

<script>
import Ticker from './Ticker.vue'
import { reactive, onMounted } from "vue";


export default {
  name: 'Board',
  props: {
    detail: Object,
  },
  components: {
    Ticker,
  },
  data() {
    return {
      // game: null,
    }
  },
  watch: {
    // details() {
    //   this.updateGame();
    // },
  },
  computed: {
    details() {
      return this.detail
    },
    ends() {
      return this.detail.ends
    }
  },
  methods: {
    // updateGame() {
    //   this.game = this details
    // },
  }
}
</script>

<style scoped type="text/css">
@font-face {
  font-family: bigText;
  src: url(../assets/fonts/ebrima-bold.ttf);
}

.row {
    background-color: black;
    /*height:25vh;*/
    /*width: 100vh;*/
}

.txt {
  font-family: bigText;
  color: white;
  font-size: 14vh;
  text-align: center;
  line-height: 1.0;
}

.ends {
  font-family: bigText;
  color: white;
  font-size: 10vh;
  text-align: center;
  line-height: 1.0;
}

.logo {
  background-color: white;
  height: 70%;
  display: block;
  margin: auto;
}


</style>
