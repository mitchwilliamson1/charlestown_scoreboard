<template>
  <div class="home">
    <div class="row">

      <div class="col">
        <div class="bg-secondary p-3 text-white" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight" aria-controls="offcanvasRight">Create New Club</div>

      <div class="offcanvas offcanvas-end w-50" tabindex="-1" id="offcanvasRight" aria-labelledby="offcanvasRightLabel">
        <div class="offcanvas-header">
          <h5 id="offcanvasRightLabel">Create Club</h5>
          <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">
          <div class="">
          <div class="row p-1">
            <div class="col-4">Name</div>
            <input class="col" v-model="createClub.name" type="text">
          </div>
          <div class="row p-1">
            <div class="col-4">Logo</div>
            <input type="file" ref="file" @change="onChange($event)" class="col">
          </div>
          <div class="row p-1">
            <div class="col-4">Address</div>
            <input class="col" v-model="createClub.address" type="text">
          </div>
          <div class="row p-1">
            <div class="col-4">Contact</div>
            <input class="col" v-model="createClub.contact_details" type="text">
          </div>
          </div>

          <div class="">
            <button type="button" @click="createClubButton(createClub)" data-bs-dismiss="offcanvas" class="btn btn-success">Create Club</button>
          </div>
        </div>
      </div>

        <div class="row">
          <div v-if="state.clubs" class="col-12">
            <h3 class="p-3">Current Clubs</h3>
            <current-clubs :clubs="state.clubs"/>
          </div>
        </div>
        
      </div>
    </div>
    
  </div>
</template>

<script>
import { reactive, onMounted, ref} from "vue";
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
    }
  },
  setup() {
    const state = reactive({
      players: null,
      clubs: null,
    });

  const createClub = reactive({
        name:null,
        logo:null,
        address: null,
        contact: null,
      });

    function onChange(event) {
      createClub.logo = event.target.files[0]
    }

    var path = ""
    path = 'http://127.0.0.1:8000/'
    
    onMounted(async () => { 
      getPlayers()
      getClubs()
    });
    function createClubButton(club) {
      let data = new FormData();
      data.append('file', club.logo);
      data.append('club', JSON.stringify(club));

      axios.post(path+'players/create_club',
      data,
      {headers: {
        'Content-Type': 'multipart/form-data'
        }
      })
      .then(function (response) {
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
      createClub,
      getPlayers,
      createClubButton,
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