<template>
  <div class="home">
    <div class="row">

      <div class="col">
        <div class="bg-secondary p-3 text-white" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight" aria-controls="offcanvasRight">New Rink</div>

      <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasRight" aria-labelledby="offcanvasRightLabel">
        <div class="offcanvas-header">
          <h5 id="offcanvasRightLabel">New Rink</h5>
          <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">
          
          <div class="row">
            <div class="col-4">Name</div>
            <input class="col" v-model="createTeam.name" type="text">
          </div>
          <div class="row">
            <div class="col-4">Logo</div>
            <input class="col" v-model="createTeam.logo" type="text">
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
            <button @click="createTeamButton(this.createTeam)" class="btn btn-success">Create Rink</button>
          </div>
        </div>
      </div>

        <div class="row">
          <div v-if="state.rinks" class="col-12">
            <current-rinks :rinks="state.rinks" :masterboards="state.masterboards"/>
          </div>
        </div>
  
      </div>
    </div>
    
  </div>
</template>

<script>
import { reactive, onMounted } from "vue";
import CurrentRinks from '../components/CurrentRinks.vue'
import axios from 'axios'
import { DateTime } from "luxon";

export default {
  name: 'PlayersView',
  components: {
    CurrentRinks,
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
      rinks: null,
      masterboards: null,
    });

    var path = ""
    if (process.env.NODE_ENV == 'development'){
      path = 'http://127.0.0.1:8000/'
    }else{
      path = window.location.toString();
    }
    
    onMounted(async () => { 
      getRinks()
      getMasterboards()
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
    function getRinks() {
      axios.get(path+'games/get_rinks')
      .then(function (response) {
        if (response.status == 200){
          console.log("RESPONSE ", response.data);
          state.rinks = response.data
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
    function getMasterboards() {
      axios.get(path+'games/get_masterboards')
      .then(function (response) {
        if (response.status == 200){
          console.log("RESPONSE ", response.data);
          state.masterboards = response.data
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
      getRinks,
      createTeamButton,
    };
  },
  methods: {

  }
}
</script>
<style type="text/css" scoped>

</style>