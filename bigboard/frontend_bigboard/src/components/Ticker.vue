<template>
  <div>
    <!-- <div class="bg-light"> {{player}}</div> -->
    <div class="count text-align-center h-100" :style="addstyle"> 
      <div v-if="typeof ends !== 'undefined'">{{ends}}</div>
      <div v-if="typeof score !== 'undefined'">{{score}}</div>
      <div v-if="typeof sets !== 'undefined'">{{sets}}</div>
      <!-- <div v-if="typeof sets !== 'undefined'">1&#189;</div> -->
    </div>
    <div class="text-align-center">
      <button v-if="isMobile() && (typeof ends !== 'undefined')" @click="endsUp(ends)">Increase</button>
      <button v-if="isMobile() && (typeof ends !== 'undefined')" @click="endsDown(ends)">Decrease</button>
      <button v-if="isMobile() && (typeof score !== 'undefined')" @click="scoreUp(score)">Increase</button>
      <button v-if="isMobile() && (typeof score !== 'undefined')" @click="scoreDown(score)">Decrease</button>
      <button v-if="isMobile() && (typeof sets !== 'undefined')" @click="setsUp(sets)">Increase</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Ticker',
  props: {
    player: Object,
    details: Object,
    endsProp: Number,
    setsProp: Number,
    colour: String,
    fontSize: String,
    fontColour: String,
  },
  data() {
    return {
    }
  },
  computed: {
    score() {
      return this.player.score
    },
    ends() {
      return this.endsProp
    },
    sets() {
      return this.setsProp
    },
    addstyle() {
      return "font-size:"+this.fontSize+"vh; color:"+this.fontColour+";"
    }
  },
  methods: {
    isMobile() {
     if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
       return true
     } else {
       return false
     }
   },
    scoreUp(score) {
      score++
      console.log(score)
      axios.post('http://127.0.0.1:8081/add_score', {
      update: {score: parseInt(score), player:this.player}
      })
      .then(function (response) {
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
    },
    scoreDown(score) {
      score--
      axios.post('http://127.0.0.1:8081/add_score', {
      update: {score: parseInt(score), player:this.player}
      })
      .then(function (response) {
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
    },
    endsUp(ends) {
      ends++
      console.log(ends)
      axios.post('http://127.0.0.1:8081/add_ends', {
      update: {ends: parseInt(ends), game_id:this.details.game_id}
      })
      .then(function (response) {
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
    },
    endsDown(ends) {
      ends--
      axios.post('http://127.0.0.1:8081/add_ends', {
      update: {ends: parseInt(ends), game_id:this.details.game_id}
      })
      .then(function (response) {
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
    },
    setsUp(sets) {
      var newSets = Number(sets) 
      newSets+=0.5
      var js = {"player_id": this.player}
      axios.post('http://127.0.0.1:8081/add_sets', {
      update: {sets: newSets, player:js}
      })
      .then(function (response) {
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
    },
  },
}
</script>
<style scoped type="text/css">
@font-face {
  font-family: clock-look;
  src: url(../assets/fonts/ebrima-bold.ttf);
}

.count {
  font-family: clock-look;
  color: yellow;
  text-align: center;
  stroke: solid;
  background-color: black;
  line-height: 0.8;
}
</style>




