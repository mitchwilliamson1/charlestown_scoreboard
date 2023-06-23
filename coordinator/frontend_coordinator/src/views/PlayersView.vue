<template>
  <div class="home">
    <div class="row">
      <div class="col">
        <div class="bg-secondary p-3 text-white" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight" aria-controls="offcanvasRight">New Player</div>

      <div class="offcanvas offcanvas-end w-50" tabindex="-1" id="offcanvasRight" aria-labelledby="offcanvasRightLabel">
        <div class="offcanvas-header">
          <h5 id="offcanvasRightLabel">New Player</h5>
          <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">

          <div class="row">
            <div class="col-4">Club</div>
              <select class="col" v-model="createPlayer.club">
                <option v-for="club in state.clubs" :value="club.club_id">{{club.club_name}}</option>
              </select>
          </div>
          
          <div class="row p-1">
            <div class="col-4">First Name</div>
            <input class="col" v-model="createPlayer.first_name" type="text">
          </div>
          <div class="row p-1">
            <div class="col-4">Last Name</div>
            <input class="col" v-model="createPlayer.last_name" type="text">
          </div>
          <div class="row p-1">
            <div class="col-4">Bowls Number</div>
            <input class="col" v-model="createPlayer.bowls_number" type="text">
          </div>
          <div class="row p-1">
            <div class="col-4">Grade</div>
            <select class="col" v-model="createPlayer.grade" type="text">
              <option v-for="num in 7" :value="num">{{num}}</option>
              <option :value="'None'">None</option>
            </select>
          </div>

          <div class="">
            <button type="button" @click="createPlayerButton(this.createPlayer)" class="btn btn-success">Create Player</button>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col-12">
          <h3 class="p-3">Current Players</h3>
          <current-players :players="state.players" :clubs="state.clubs"/>
        </div>
      </div>
        
      </div>
    </div>
    
  </div>
</template>

<script>
import { reactive, onMounted } from "vue";
import CurrentPlayers from '../components/CurrentPlayers.vue'
import CurrentClubs from '../components/CurrentClubs.vue'
import axios from 'axios'
import { DateTime } from "luxon";

export default {
  name: 'PlayersView',
  components: {
    CurrentPlayers,
    CurrentClubs,
  },
  data() {
    return {
      createPlayer: {
        'club':null,
        'first_name':null,
        'last_name': null,
        'address': null,
        'email':null,
      },
      createClub: {
        'name':null,
        'logo':null,
        'address': null,
        'contact': null,
      }
    }
  },
  setup() {
    const state = reactive({
      players: null,
      clubs: null,
    });

    var path = ""
    path = 'http://127.0.0.1:8000/'
    
    onMounted(async () => { 
      getPlayers()
      getClubs()
    });
    function createClubButton(club) {
      axios.post(path+'players/create_club', {
      create_club: club,
      })
      .then(function (response) {
        console.log(response);
        getClubs()
      })
      .catch(function (error) {
        console.log(error);
      });
    }
    function createPlayerButton(player) {
      axios.post(path+'players/create_player', {
      create_player: player,
      })
      .then(function (response) {
        console.log(response);
        getPlayers()
      })
      .catch(function (error) {
        console.log(error);
      });
    }
    function getPlayers() {
      axios.get(path+'players/get_players')
      .then(function (response) {
        if (response.status == 200){
          console.log("RESPONSE ", response.data);
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
    function getClubs() {
      axios.get(path+'players/get_clubs')
      .then(function (response) {
        if (response.status == 200){
          console.log("RESPONSE ", response.data);
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

    return {
      path,
      state,
      getPlayers,
      createClubButton,
      createPlayerButton,
    };
  },
  methods: {

  }
}
</script>
<style type="text/css" scoped>

</style>