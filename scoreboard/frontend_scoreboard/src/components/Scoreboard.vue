<template>
  <div v-if="this.details" class="container-fluid h-100 w-100 p-0" style="background-color: black;">
    <div class="container-fluid h-100 w-100">
      <div class="row align-items-center" style="height: 25%;">
        <div class="col h-100">
          <!-- <div class="txt">{{details.competitors[1].first_name.charAt(0)}}{{details.competitors[0].last_name.charAt(0)}}</div> -->
          <img class="logo" src="../assets/logos/tigers.jpg">
        </div>
        <div class="col h-100">
          <!-- <div class="txt">{{details.competitors[0].first_name.charAt(0)}}{{details.competitors[1].last_name.charAt(0)}}</div> -->
          <img class="logo"  src="../assets/logos/Jets.png">
        </div>
      </div>

      <div class="row align-items-center" style="height: 22%; padding-bottom: 100px;">
        <div class="col align-self-center">
          <Ticker :player="details.competitors[0]" 
                    :details="details"
                    fontSize="23" 
                    colour="red"/>
        </div>
        <div class="col">
          <Ticker :player="details.competitors[1]" 
                    :details="details"
                    fontSize="23" 
                    colour="black"/>
        </div>
      </div>

      <div class="row align-items-center" style="height: 28%;">
        <div class="col h-100 align-self-center">
          <img class="add" src="../assets/adds/belle_property.png">
        </div>
      </div>

      <div class="row align-items-center" style="height: 25%;">
        <div class="col">
          <Ticker :details="details"
                  :endsProp="ends"
                  player="ends" 
                  fontSize="20" 
                  fontColour="white" 
                  colour="black"/>
        </div>
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
}

.txt {
  font-family: bigText;
  color: white;
  font-size: 18vh;
  text-align: center;
  line-height: 1.0;
}

.ends {
  font-family: bigText;
  color: white;
  text-align: center;
  line-height: 1.0;
}

.logo {
  background-color: white;
  top: 10%;
  aspect-ratio: 4/3;
  position: relative;
  height: 75%;
  display: block;
  margin-left: auto;
  margin-right: auto;
}

.add {
  background-color: white;
  position: relative;
  height: 100%;
  display: block;
  margin-left: auto;
  margin-right: auto;
}


</style>
