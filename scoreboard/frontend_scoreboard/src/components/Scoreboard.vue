<template>
  <div v-if="this.details" class="container-fluid h-100 w-100 p-0" style="background-color: black;">
    <div class="container-fluid w-100 d-flex flex-column" style="height: 100vh">
      <div class="row align-items-center" style="height: 25%;">
        <div class="col p-0 h-100">
          <div v-if="coordinator_running" class="h-100" >
            <img v-if="p1.competitor_display == 'Logo'" class="logo"  :src="'http://'+coordinator+'/players/get_logo/'+p1Logo">
            <div v-else-if="p1.competitor_display == 'First Initial'" class="txt">{{p1.first_name.charAt(0)}}</div>
            <div v-else-if="p1.competitor_display == 'Fist and Last Initial'" class="txt">{{p1.first_name.charAt(0)}}{{p1.last_name.charAt(0)}}</div>
            <img v-else="p1.competitor_display == 'Default'" class="logo" :src="'http://127.0.0.1:8081/charls.jpeg'"> 
          </div>
          <div v-else class="h-100">
            <div v-if="p1.competitor_display == 'first name'" class="txt">{{p1.first_name.charAt(0)}}</div>
            <div v-else-if="p1.competitor_display == 'Fist and Last Initial'" class="txt">{{p1.first_name.charAt(0)}}{{p1.last_name.charAt(0)}}</div>
            <img v-else="p1.competitor_display == 'Default'" class="logo" :src="'http://127.0.0.1:8081/charls.jpeg'">

          </div>
        </div>
        <div class="col p-0 h-100">
          <div v-if="coordinator_running" class="h-100" >
            <img v-if="p2.competitor_display == 'Logo'" class="logo"  :src="'http://'+coordinator+'/players/get_logo/'+p2Logo">
            <div v-else-if="p2.competitor_display == 'First Initial'" class="txt">{{p2.first_name.charAt(0)}}</div>
            <div v-else-if="p2.competitor_display == 'Fist and Last Initial'" class="txt">{{p2.first_name.charAt(0)}}{{p2.last_name.charAt(0)}}</div>
            <img v-else="p2.competitor_display == 'Default'"  class="logo" :src="'http://127.0.0.1:8081/away.jpeg'">
          </div>
          <div v-else class="h-100">
            <div v-if="p2.competitor_display == 'First Initial'" class="txt">{{p2.first_name.charAt(0)}}</div>
            <div v-else-if="p2.competitor_display == 'Fist and Last Initial'" class="txt">{{p2.first_name.charAt(0)}}{{p2.last_name.charAt(0)}}</div>
            <img v-else="p2.competitor_display == 'Default'" class="logo" :src="'http://127.0.0.1:8081/away.jpeg'">
          </div>
        </div>
      </div>

      <div class="row align-items-center" style="min-height: 25%; padding-bottom: 30px;">
        <div class="col p-0 align-self-center">
          <Ticker :player="details.competitors[0]" 
                    :details="details"
                    fontSize="21" 
                    colour="red"/>
        </div>
        <div class="col p-0">
          <Ticker :player="details.competitors[1]" 
                    :details="details"
                    fontSize="21" 
                    colour="black"/>
        </div>
      </div>

      <div v-if="!isMobile()" class="flex-fill">
        <div class="h-100 align-self-center">
          <!-- <div class="h-100" style="background: red" /> -->
          <div :style="getBackgroundImage" class="add"/>
        </div>
      </div>

      <div class="row align-items-center overflow-hidden" style="height: 25%;">
        <div class="col">
          <Ticker :details="details"
                  :endsProp="ends"
                  player="ends" 
                  fontSize="21" 
                  fontColour="white" 
                  colour="black"/>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import Ticker from './Ticker.vue'
import axios from 'axios'
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
    getBackgroundImage() {
      return 'background-image:url(http://127.0.0.1:8081/'+this.detail.sponsor+');'
    },
    p1() {
      return this.detail.competitors[0]
    },
    p2() {
      return this.detail.competitors[1]
    },
    details() {
      return this.detail
    },
    coordinator_running() {
      return this.detail.coordinator_running
    },
    coordinator() {
      return this.detail.coordinator
    },
    p1Logo() {
      return this.detail.competitors[0].logo
    },
    logo() {
      return this.coordinator+'/players/get_logo/'+this.p1Logo
    },
    p2Logo() {
      return this.detail.competitors[1].logo
    },
    ends() {
      return this.detail.ends
    }
  },
  methods: {
    isMobile() {
     if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
       return true
     } else {
       return false
     }
   }
    // updateGame() {
    //   this.game = this details
    // },
  },

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
  font-size: 16vh;
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
  /*background-color: white;*/
  position: relative;
  /*height: 100%;*/
  display: block;
  margin-left: auto;
  margin-right: auto;

  background-size:contain;
  background-repeat: no-repeat;
  background-position: center center;
  height: 100%;

}


</style>
