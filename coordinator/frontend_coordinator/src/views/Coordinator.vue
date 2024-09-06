<template>
  <div v-if="getGames" class="coordinator">
    <div class="container">
      <div class="bg-secondary p-3 text-white" 
        type="button" 
        data-bs-toggle="offcanvas" 
        data-bs-target="#offcanvasRight" 
        aria-controls="offcanvasRight">
          Create New Game
        </div>

      <div class="offcanvas offcanvas-end w-50" 
        tabindex="-1" 
        id="offcanvasRight" 
        aria-labelledby="offcanvasRightLabel">
        <div class="offcanvas-header">
          <h5 id="offcanvasRightLabel">New Game</h5>
          <button type="button" 
            class="btn-close text-reset" 
            data-bs-dismiss="offcanvas" 
            aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">

          <div class="row p-1" v-for="item, key in state.init">
            <div class="row" v-if="key != 'display'">
              <div class="col-4">{{capitalise(key)}}</div>
              <select v-model="createGame[key]" class="form-select col">
                <option v-for="type in item" :value="type">{{type[key]}}</option>
              </select>
            </div>
          </div>

          <div class="row">
            <div v-for="team in 2" class="col">
              <div class="col">Club {{team}}
                <input :id="'club'+team" @click="list('clubList'+team)" v-model="createGame['clubs'][team]" type="text" name="">
                <div class="club">
                  <ul :id="'clubList'+team">
                    <li :id="club.club_id"
                        :class="'listItem'+team"
                        @click="list('clubList'+team)"
                        v-for="club in state.clubs">
                      {{ club.club_name }}
                    </li>
                  </ul>
                </div>
              </div>

                <div v-if="createGame.clubs[team] && display[team]">
                  <div class="">Player </div>
                  <select v-model="createGame.competitors[team]['player']" class="form-select">
                      <option :value="player" v-for="player in selectPlayers(createGame.clubs[team].club_id, team)">{{player.first_name}} {{player.last_name}} - BA No: {{player.bowls_number}}</option>
                  </select>
              <div>Display</div>
                
                <select v-model="createGame.competitors[team]['player'].display" class="form-select">
                  <option v-for="display in state.init.display" :value="display">{{display.display}}</option>
                </select>
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
      display: {1:{}, 2:{}},
      rinks: 12,
      clubInput:null,
      isHidden: true,
      active:false,
      createGame: {
        'name': {},
        'competition': {},
        'display': {},
        'rink': {},
        'clubs': {},
        'sponsor': {},
        'competitors': {'1':{'player':{}}, '2':{'player':{}}},
      }
    }
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
      initialise()
      getGames()
      getFinishedGames()
      getPlayers()
      getClubs()
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
  mounted () {
    
  },
  created () {
  },
  watch: {
    createGame: {
      handler: function (val, oldVal) {
        this.selectClubs(val.clubs)
      },
      deep: true,
    },
  },
  computed: {
    clubInput(){
      return this.createGame.clubs
    }
  },
  methods:{
    selectClubs(val){
      if(this.state.clubs){
        for (let i = 1; i <= 2; i++) {
          console.log(i)
          const listItems = document.querySelectorAll('.listItem'+i);
          listItems.forEach(function (item) {
            const text = item.innerText.toLowerCase();
            if (text.includes(val[i])) {
                item.classList.remove('hidden');
            } else {
                item.classList.add('hidden');
            }
        });
        }
      }
    },
    list(id){
      const listItem = document.getElementById(id);
      if (listItem.classList.contains('hidden')){
        listItem.classList.remove('hidden');
      }else{
        listItem.classList.add('hidden');
      }

      // this.isHidden = !this.isHidden
    },
    select(num){
      this.isHidden = !this.isHidden
    },
    playerObj(number, player) {
      console.log('Number: ', number)
      return {number:player}
    },
    capitalise(key) {
      key = key.replace("_", " ")
      return key.charAt(0).toUpperCase() + key.slice(1);
    },
    selectPlayers(clubName, team){
      var players = this.state.players.filter(i => i.club == clubName)
      return players
    },

  },
}
</script>

<style scoped type="text/css">
.club {
  max-width: 600px;
  max-height: 400px;
  overflow: scroll;
  margin: 20px auto;
  /*padding: 20px;*/
  background-color: #fff;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

#filterInput {
  margin-bottom: 20px;
  padding: 10px;
  width: calc(100% - 20px);
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
} 
.listItem1 {
  padding: 10px;
  margin: 5px 0;
  background-color: #f9f9f9;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.listItem1:hover {
  background-color: #e9e9e9;
}
.listItem2 {
  padding: 10px;
  margin: 5px 0;
  background-color: #f9f9f9;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.listItem2:hover {
  background-color: #e9e9e9;
}
.hidden {
  display: none;
}
</style>