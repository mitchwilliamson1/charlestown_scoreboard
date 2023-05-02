<template>
  <div>
    <div class="count text-align-center h-100" :style="addstyle"> 
      <div v-if="typeof ends !== 'undefined'">58</div>
      <div v-if="typeof score !== 'undefined'">57</div>
    </div>
<!-- <button v-if="typeof ends !== 'undefined'" @click="endsUp(ends)">Increase</button>
      <button v-if="typeof ends !== 'undefined'" @click="endsDown(ends)">Decrease</button> -->
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
    colour: String,
    fontSize: String,
    fontColour: String,
  },
  data() {
    return {
      playerId: this.player.first_name,
    }
  },
  computed: {
    score() {
      return this.player.score
    },
    ends() {
      return this.endsProp
    },
    addstyle() {
      return "font-size:"+this.fontSize+"vh; color:"+this.fontColour+";"
    }
  },
  methods: {
    scoreUp() {
      if(typeof this.score !== "undefined") {
        this.player.score++
        axios.post('http://127.0.0.1:8081/add_score', {
        update: {score: parseInt(this.score), player_id: this.player.player_id, game_id:this.details.game_id}
        })
        .then(function (response) {
          console.log(response);
        })
        .catch(function (error) {
          console.log(error);
        });
      }
    },
    endsUp() {
      console.log("GAME ID", this.details.game_id)
      this.ends++
      axios.post('http://127.0.0.1:8081/add_ends', {
      update: {ends: parseInt(this.ends), game_id:this.details.game_id}
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
  line-height: 0.9;
}
</style>




