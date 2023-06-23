<template>
  <div v-if="getGames" class="coordinator">
    <div class="container">
      <div class="bg-secondary p-3 text-white" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight" aria-controls="offcanvasRight">Create New Game</div>

      <div class="offcanvas offcanvas-end w-50" tabindex="-1" id="offcanvasRight" aria-labelledby="offcanvasRightLabel">
        <div class="offcanvas-header">
          <h5 id="offcanvasRightLabel">New Game</h5>
          <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">
          <div class="row p-1" v-for="item, key in state.init">
              <div class="col-4">{{capitalise(key)}}</div>
              <select v-model="createGame[key]" class="form-select col">
                <option v-for="type in item" :value="type">{{type[key]}}</option>
              </select>
          </div>

          <div class="row">
            <div v-if="createGame['game_type']" v-for="clubNumber in 2" class="col">
              <div class="">Club {{clubNumber}}</div>
                <select v-model="createGame.clubs[clubNumber]" class="form-select">
                  <option v-for="club in state.clubs" :value="club">{{club.club_name}}</option>
                </select>            
              <div class="col" v-for="number in parseInt(createGame['game_type']['players']/2)">
                <div v-if="createGame.clubs[clubNumber]">
                  <div class="">Player {{number}}</div>
                  <select v-model="createGame.competitors[clubNumber][number]" class="form-select">
                    <option v-for="player in selectPlayers(createGame.clubs[clubNumber].club_id)" :value="player">{{player.first_name}} {{player.last_name}} - BA No: {{player.bowls_number}}</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
          <div class="col p-5">
            <button type="button" @click="create(this.createGame)" class="btn btn-success">Create Game</button>
          </div>
        </div>
      </div>
      <div class="row p-3">
        <div class="col-12">
          <h3 class="p-3">Current Games</h3>
          <current-games v-for="game in state.games" @reload="getGames" :game="game" :gameOptions="state.init"/>
        </div>
      </div>

      <div class="row p-3">
        <div class="col-12">
          <h3 class="p-3">Finished Games</h3>
          <current-games v-for="game in state.finishedGames" @reload="getGames" :game="game" :gameOptions="state.init"/>
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
        'game_type': null,
        'round': {},
        'grade': {},
        'level': {},
        'display': {},
        'rink': {},
        'clubs': {},
        'competitors': {'1':{}, '2':{}},
      }
    }
  },
  mounted () {
    
  },
  setup() {
    const state = reactive({
      games: null,
      finishedGames: null,
      players: null,
      clubs: null,
      init: null,
    });

    var path = ""
    path = 'http://127.0.0.1:8000/'
    
    onMounted(async () => { 
      getGames()
      getFinishedGames()
      getPlayers()
      getClubs()
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
    function create(createGame) {
      createGame.start_time = DateTime.utc().toISO()
      axios.post(path+'games/create_game', {
      create_game: createGame,
      })
      .then(function (response) {
        console.log("GET GAMES: ", response);
        getGames()
      })
      .catch(function (error) {
        console.log("ERROR: ", error);
      });
      
    }
    function getFinishedGames() {
      axios.get(path+'games/get_finished_games')
      .then(function (response) {
        if (response.status == 200){
          state.finishedGames = response.data
        }
      })
      .catch(function (error) {
        console.log("ERROR ", error);
      })
      .then(function () {
        // always executed
      });
    }
    function getClubs() {
      axios.get(path+'players/get_clubs')
      .then(function (response) {
        if (response.status == 200){
          state.clubs = response.data
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
      create,
      getFinishedGames,
      getPlayers
    };
  },
  created () {
  },
  computed: {

  },
  methods:{
    playerObj(number, player) {
      console.log('Number: ', number)
      return {number:player}
    },
    capitalise(key) {
      key = key.replace("_", " ")
      return key.charAt(0).toUpperCase() + key.slice(1);
    },
    selectPlayers(clubName){
      return this.state.players.filter(i => i.club == clubName)
    },

  },
}
</script>

<style scoped type="text/css">

</style>