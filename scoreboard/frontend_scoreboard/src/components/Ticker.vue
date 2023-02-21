<template>
  <div style="text-align: center;">
    <div class="container">
      <div class="row align-items-center">
        <div class="col align-self-center count " :style="addstyle"> 
          <div v-if="type == 'ends'">{{ends}}</div>
          <div v-if="type == 'score'">{{score}}</div>
        </div>
      </div>
    </div>
    <button v-if="type == 'ends'" @click="endsUp">Increase</button>
    <button v-if="type == 'ends'" @click="endsDown">Decrease</button>
    <button v-if="type == 'score'" @click="scoreUp">Increase</button>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Ticker',
  props: {
    player: Object,
    details: Object,
    type: String,
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
      return this.details.ends
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
      this.details.ends++
      console.log(this.details.ends)
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
    endsDown() {
      this.details.ends--
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




