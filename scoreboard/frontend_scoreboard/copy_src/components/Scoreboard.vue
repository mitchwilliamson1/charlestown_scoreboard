<template>
  <div v-if="this.details" class="container-fluid p-0" style="background-color: white">
    <div class="row align-items-center teamAndTime">
      <div class="col align-self-center p-2 shadow rounded">
          <!-- <div class="txt">{{details.competitors[0].first_name.charAt(0)}} {{details.competitors[0].last_name.charAt(0)}}</div> -->
          <img class="logo" src="../assets/logos/tigers.jpg">
      </div>
      <div class="col align-self-center p-2 shadow rounded">
          <!-- <div class="txt">{{details.competitors[1].first_name.charAt(0)}} {{details.competitors[1].last_name.charAt(0)}}</div> -->
          <img class="logo" src="../assets/logos/Jets.png" style="background-color: white;">
      </div>
    </div>

    <div class="row align-items-center scores">
      <div class="col align-self-center shadow p-1 mb-5 rounded">
        <div style="height: 100%;" class="ticker">
          <Ticker :player="details.competitors[1]" 
                  :details="details"
                  type='score'
                  fontSize="22" 
                  colour="red"/>
        </div>
      </div>
      <div class="col align-self-center shadow p-1 mb-5 rounded">
        <div style="height: 100%;" class="ticker">
          <Ticker :player="details.competitors[0]" 
                  :details="details"
                  type='score'
                  fontSize="22" 
                  colour="black"/>
        </div>
      </div>
    </div>

    <div class="row align-items-center scores">
      <div class="col align-self-center shadow p-1 mb-5rounded ends">
        <img class="logo" src="../assets/adds/belle_property.png" style="background-color: white; width: 40%;">
      </div>
    </div>

    <div class="row align-items-center scores">
      <div class="col align-self-center shadow p-1 mb-5 rounded">
        <Ticker :details="details"
                type="ends"
                player="ends" 
                fontSize="18" 
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
    height:25vh;
    /*width: 100vh;*/
}

.txt {
  font-family: bigText;
  color: white;
  font-size: 12vh;
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
  width: 70%;
  display: block;
  margin-left: auto;
  margin-right: auto;
}


</style>
