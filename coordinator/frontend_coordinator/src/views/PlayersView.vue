<template>
  <div class="home">
    <div class="row">
      <div class="col">
        <div class="bg-secondary p-3 text-white" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight" aria-controls="offcanvasRight">New Player</div>

      <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasRight" aria-labelledby="offcanvasRightLabel">
        <div class="offcanvas-header">
          <h5 id="offcanvasRightLabel">New Player</h5>
          <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">

          <div class="row">
            <div class="col-4">Team</div>
              <select class="col" v-model="createPlayer.team">
                <option v-for="team in state.teams" :value="team.team_id">{{team.team_name}}</option>
              </select>
          </div>
          
          <div class="row">
            <div class="col-4">First Name</div>
            <input class="col" v-model="createPlayer.first_name" type="text">
          </div>
          <div class="row">
            <div class="col-4">Last Name</div>
            <input class="col" v-model="createPlayer.last_name" type="text">
          </div>
          <div class="row">
            <div class="col-4">Address</div>
            <input class="col" v-model="createPlayer.address" type="text">
          </div>
          <div class="row">
            <div class="col-4">Email</div>
            <input class="col" v-model="createPlayer.email" type="text">
          </div>

          <div class="">
            <button type="button" @click="createPlayerButton(this.createPlayer)" class="btn btn-success">Create Player</button>
          </div>
        </div>
      </div>



        <div class="row">
          <div class="col-12">
            <div>Current Players</div>
            <current-players :players="state.players" :teams="state.teams"/>
          </div>
        </div>
        
      </div>
    </div>
    
  </div>
</template>

<script>
import { reactive, onMounted } from "vue";
import CurrentPlayers from '../components/CurrentPlayers.vue'
import CurrentTeams from '../components/CurrentTeams.vue'
import axios from 'axios'
import { DateTime } from "luxon";

export default {
  name: 'PlayersView',
  components: {
    CurrentPlayers,
    CurrentTeams,
  },
  data() {
    return {
      createPlayer: {
        'team':null,
        'first_name':null,
        'last_name': null,
        'address': null,
        'email':null,
      },
      createTeam: {
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
      teams: null,
    });

    var path = ""
    path = 'http://127.0.0.1:8000/'
    
    onMounted(async () => { 
      getPlayers()
      getTeams()
    });
    function createTeamButton(team) {
      axios.post(path+'players/create_team', {
      create_team: team,
      })
      .then(function (response) {
        console.log(response);
        getTeams()
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
    function getTeams() {
      axios.get(path+'players/get_teams')
      .then(function (response) {
        if (response.status == 200){
          console.log("RESPONSE ", response.data);
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

    return {
      path,
      state,
      getPlayers,
      createTeamButton,
      createPlayerButton,
    };
  },
  methods: {

  }
}
</script>
<style type="text/css" scoped>

</style>