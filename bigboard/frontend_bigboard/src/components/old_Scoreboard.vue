<template>
  <div v-if="this.details" class="container-fluid h-100 w-100 p-0" style="background-color: white;">
    <div class="container-fluid h-100 w-100">
      <div class="row align-items-center" style="height: 45%;">
        <div class="col-4 h-100">
          <img class="logo" :src="P1Url">
        </div>
        <div class="col-4">
          <Ticker :player="details.ends" 
                    :details="details"
                    fontSize="30" 
                    fontColour="white"/>
        </div>
        <div class="col-4 h-100">
          <img class="logo" :src="P2Url">
        </div>
      </div>

      <div class="row justify-content-between overflow-hidden" style="height:55%; width: 100%;">
        <div class="col align-self-center w-50">
          <Ticker :player="details.competitors[0].score" 
                    :details="details"
                    fontSize="45" 
                    colour="red"/>
        </div>
        <div class="col"></div>
        <div class="col align-self-center w-50">
          <Ticker :player="details.competitors[1].score"
                    :details="details"
                    fontSize="45" 
                    colour="black"/>
        </div>
      </div>

    </div>
  </div>

</template>

<script>
import Ticker from './Ticker.vue'
import { reactive, onMounted } from "vue";
import axios from 'axios'

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
    P1Url() {
      return 'http://'+this.detail.coordinator_ip+'/players/get_logo/'+this.detail.competitors[0].logo
    },
    P2Url() {
      return 'http://'+this.detail.coordinator_ip+'/players/get_logo/'+this.detail.competitors[1].logo
    },
    details() {
      return this.detail
    },
    ends() {
      return this.detail.ends
    }
  },
  methods: {
    newsrc1() {
      return "http://127.0.0.1:8083/charls.jpeg"
    },
    newsrc1() {
      return "http://127.0.0.1:8083/away.jpeg"
    },
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
