<template>
  <div class="home">
    <div class="row">

      <div class="col">
        <div class="bg-secondary p-3 text-white" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight" aria-controls="offcanvasRight">New Team</div>

      <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasRight" aria-labelledby="offcanvasRightLabel">
        <div class="offcanvas-header">
          <h5 id="offcanvasRightLabel">New Team</h5>
          <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">
          
          <div class="row">
            <div class="col-4">Name</div>
            <input class="col" v-model="createTeam.name" type="text">
          </div>
          <div class="row">
            <div class="col-4">Logo</div>
            <!-- <input class="col" v-model="createTeam.logo" type="text"> -->
            <!-- <input type="file" ref="file" v-on:change="handleFileUpload()"  class="col"> -->
            <input type="file" ref="file" @change="onChange($event)" class="col">
          </div>
          <div class="row">
            <div class="col-4">Address</div>
            <input class="col" v-model="createTeam.address" type="text">
          </div>
          <div class="row">
            <div class="col-4">Contact</div>
            <input class="col" v-model="createTeam.contact" type="text">
          </div>

          <div class="">
            <button type="button" @click="createTeamButton(createTeam)" class="btn btn-success">Create Team</button>
          </div>
        </div>
      </div>

        <div class="row">
          <div v-if="state.teams" class="col-12">
            <div>Current Teams</div>
            <current-teams :teams="state.teams"/>
          </div>
        </div>
        
      </div>
    </div>
    
  </div>
</template>

<script>
import { reactive, onMounted, ref} from "vue";
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
    }
  },
  setup() {
    const state = reactive({
      players: null,
      teams: null,
      
    });

  const createTeam = reactive({
        name:null,
        logo:null,
        address: null,
        contact: null,
      });

    // const handleFileUpload = async() => {
    //    // debugger;
    //    console.log("selected file",file.value.files)
    //    console.log("IMG: ", file.value.file)
    //    state.createTeam.logo = file.value.files[0].value
    //     //Upload to server
    // }

    function onChange(event) {
      createTeam.logo = event.target.files[0]
    }

    var path = ""
    if (process.env.NODE_ENV == 'development'){
      path = 'http://127.0.0.1:8000/'
    }else{
      path = window.location.toString();
    }
    
    onMounted(async () => { 
      getPlayers()
      getTeams()
    });
    function createTeamButton(team) {
      let data = new FormData();
      data.append('file', team.logo);
      data.append('team', JSON.stringify(team));

      console.log("name: ", JSON.stringify(team))

      axios.post(path+'players/create_team',
      data,
      {headers: {
        'Content-Type': 'multipart/form-data'
        }
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
      createTeam,
      getPlayers,
      createTeamButton,
      createPlayerButton,
      onChange,
      
    };
  },
  methods: {

  }
}
</script>
<style type="text/css" scoped>

</style>