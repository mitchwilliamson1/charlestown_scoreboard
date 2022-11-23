<template>
  <div v-if="state" class="coordinator">
    <div class="container">
      <div class="bg-secondary p-3 text-white" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight" aria-controls="offcanvasRight">Make Game</div>

      <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasRight" aria-labelledby="offcanvasRightLabel">
        <div class="offcanvas-header">
          <h5 id="offcanvasRightLabel">New Game</h5>
          <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">
          <div class="row">
            <div class="col-4">Name</div>
            <input v-model="createGame.name" class="form-control col" type="text" name="">
          </div>
          <div class="row" v-for="item, key in state.init">
              <div class="col-4">{{capitalise(key)}}</div>
              <select v-model="createGame[key]" class="form-select col">
                <option v-for="type in item" :value="type">{{type[key]}}</option>
              </select>
          </div>

          <div class="row">
            <div v-if="createGame['type']" v-for="teamNumber in 2" class="col">
              <div class="">Team {{teamNumber}}</div>
                <select v-model="createGame.teams[teamNumber]" class="form-select">
                  <option v-for="team in state.teams" :value="team">{{team.team_name}}</option>
                </select>            
              <div class="col" v-for="number in parseInt(createGame['type']['players']/2)">
                <div v-if="createGame.teams[teamNumber]">
                  <div class="">Player {{number}}</div>
                  <select v-model="createGame.players[teamNumber +'.'+number]" class="form-select">
                    <option v-for="player in selectPlayers(createGame.teams[teamNumber].team_id)" :value="player">{{player.first_name}} {{player.last_name}}</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
          <div class="col p-5">
            <button type="button" @click="create" class="btn btn-success">Create Game</button>
          </div>
        </div>
      </div>

      <div class="row p-3">
        <div class="col-12">
          <h3>Current Games</h3>
          <current-games :games="state.games" :gameOptions="state.init"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, onMounted } from "vue";
import CurrentGames from '../components/CurrentGames.vue'
import axios from 'axios'
import { DateTime } from "luxon";


export default {
  name: 'coordinator',
  components: {
    CurrentGames
  },
  data(){
    return{
      rinks: 12,
      createGame: {
        'name': null,
        'type': null,
        'round': {},
        'grade': {},
        'level': {},
        'rink': {},
        'teams': {},
        'players': {},
      }
    }
  },
  mounted () {
    
  },
  setup() {
    const state = reactive({
      games: null,
      players: null,
      teams: null,
      init: null,
    });

    var path = ""
    if (process.env.NODE_ENV == 'development'){
      path = 'http://127.0.0.1:8000/'
    }else{
      path = window.location.toString();
    }
    
    onMounted(async () => { 
      getGames()
      getPlayers()
      getTeams()
      initialise()
    });
    function initialise() {
      axios.get(path+'games/init')
      .then(function (response) {
        if (response.status == 200){
          state.init = response.data
        }
      })
      .catch(function (error) {
        console.log("ERROR ", error);
      })
      .then(function () {
        // always executed
      });
    }
    function getGames() {
      axios.get(path+'games/get_games')
      .then(function (response) {
        if (response.status == 200){
          state.games = response.data
        }
      })
      .catch(function (error) {
        console.log("ERROR ", error);
      })
      .then(function () {
        // always executed
      });
    }
    function getTeams() {
      axios.get(path+'players/get_teams')
      .then(function (response) {
        if (response.status == 200){
          state.teams = response.data
        }
      })
      .catch(function (error) {
        // handle error
        console.log("ERROR ", error);
      })
      .then(function () {
        // always executed
      });
    }
    function getPlayers() {
      axios.get(path+'players/get_players')
      .then(function (response) {
        if (response.status == 200){
          state.players = response.data
        }
      })
      .catch(function (error) {
        // handle error
        console.log("ERROR ", error);
      })
      .then(function () {
        // always executed
      });
    }

    return {
      path,
      state,
      getGames,
      getPlayers
    };
  },
  created () {
  },
  computed: {

  },
  methods:{
    capitalise(key) {
      return key.charAt(0).toUpperCase() + key.slice(1);
    },
    selectPlayers(teamName){
      console.log(teamName)
      console.log(this.state.players.filter(i => i.team == teamName))
      return this.state.players.filter(i => i.team == teamName)
    },
    create() {
      this.createGame.start_time = DateTime.utc().toISO()
      axios.post(this.path+'games/create_game', {
      create_game: this.createGame,
      })
      .then(function (response) {
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
      this.getGames()
      axios.post('http://127.0.0.1:8081/create_game', {
      create_game: this.createGame,
      })
      .then(function (response) {
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
      this.getGames()
      
    },

  },
}
</script>

<style scoped type="text/css">

</style>