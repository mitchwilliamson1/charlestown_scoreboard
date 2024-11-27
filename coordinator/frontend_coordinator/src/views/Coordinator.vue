<template>
  <div v-if="getGames && state.init" class="coordinator">
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
            <div class="row" v-if="key != 'display' && key != 'create_game'">
              <div class="col-4">{{capitalise(key)}}</div>
              <select v-model="state.init.create_game[0][key]" 
                      class="form-select col" :class="state.formatGame[key]">
                <option v-for="type in item" :value="type">{{type[key]}}</option>
              </select>
            </div>
          </div>
          <div class="row p-2">
            <div v-for="key, team in state.init.create_game[0].clubs" class="col">
              Club {{team}}: <strong>{{state.init.create_game[0].clubs[team].club_name}}</strong>
              <div class="col">
                <input @click="showClubList(team)"
                    v-model="clubSearch[team]"
                    class="form-control" 
                    :class="state.formatGame['clubs'][team]['club_name']">
                <div class="club">
                  <ul :id="'clubList'+team" class="hidden">
                    <li :id="club.club_id"
                        :class="'clubListItem'+team"
                        @click="hideClubList(team, club)"
                        v-for="club in state.clubs">
                      {{ club.club_name }}
                    </li>
                  </ul>
                </div>
              </div>

              <div v-if="state.players && state.init">
                <div class="">Player: <strong>{{state.init.create_game[0].competitors[team].first_name}}
                  {{state.init.create_game[0].competitors[team].last_name}}</strong>
                </div>
                  <input @click="showPlayerList(team)" 
                      v-model="playerSearch[team]"
                      class="form-control"
                      :class="state.formatGame['competitors'][team]['first_name']">
                  <div class="player">
                    <ul :id="'playerList'+team" class="hidden">
                      <li :id="player.player_id"
                          :class="'playerListItem'+team"
                          @click="hidePlayerList(team, player)"
                          v-for="player in selectPlayers(state.init.create_game[0].clubs[team].club_id, team)">
                        {{player.first_name}} {{player.last_name}}
                      </li>
                    </ul>
                  </div>

                <div >Display</div>
                  <select v-model="state.init.create_game[0].competitors[team].display"
                        class="form-select"
                        :class="state.formatGame['competitors'][team]['display']">
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
          <div class="container">
            <div class="row">
              <div class="col-2 fw-bold">Game</div>
              <div class="col-3 fw-bold">Team 1</div>
              <div class="col-3 fw-bold">Team 2</div>
              <div class="col-2 fw-bold">Sponsor</div>
              <div class="col-2 fw-bold">Rink</div>
            </div>
          </div>
          <current-games v-for="game in state.games" @reload="getGames" :game="game" :gameOptions="state.init"/>
        </div>
      </div>

<!--       <div class="row p-3">
        <div class="col-12">
          <h3 class="p-3">Finished Games</h3>
          <div class="container">
            <div class="row">
              <div class="col-2 fw-bold">Game</div>
              <div class="col-3 fw-bold">Team 1</div>
              <div class="col-3 fw-bold">Team 2</div>
              <div class="col-2 fw-bold">Sponsor</div>
              <div class="col-2 fw-bold">Rink</div>
            </div>
          </div>
          <current-games v-for="game in state.finishedGames" @reload="getGames" :game="game" :gameOptions="state.init"/>
        </div>
      </div> -->
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
      clubInput:null,
      isHidden: true,
      active:false,
      playerSearch: {1:"", 2:""},
      clubSearch: {1:"", 2:""},
    }
  },
  setup(props, context) {
    const state = reactive({
      games: null,
      finishedGames: null,
      players: null,
      clubs: null,
      init: null,
      formatGame: {
        'competition': {},
        'rink': {},
        'sponsor': {},
        'clubs': {
          1:'',
          2:'',
        },
        'competitors':{
          1:{},
          2:{}
        },
        'displays':{
          1:{},
          2:{}
        },
      }
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
      axios.post(path+'games/create_game', {
      create_game: state.init.create_game[0],
      })
      .then(function (response) {
        console.log("CREATED GAME: ", response);
        getGames()
      })
      .catch(function (error) {
        console.log("ERRORRR: ", error.response.data)
        state.formatGame = error.response.data
        console.log(error);
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
      getPlayers,
    };
  },
  mounted () {
  },
  created () {
  },
  watch: {
    clubSearch: {
      handler: function (val) {
        this.hideClubs(val)
      },
      deep: true,
    },
    playerSearch: {
      handler: function (val) {
        this.hidePlayers(val)
      },
      deep: true,
    },
  },
  computed: {

  },
  methods:{
    hideClubs(val){
      if(this.state.clubs){
        for (let i = 1; i <= 2; i++) {
          const listItems = document.querySelectorAll('.clubListItem'+i);
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
    hidePlayers(val){
      if(this.state.clubs){
        for (let i = 1; i <= 2; i++) {
          console.log(val[i])
          const listItems = document.querySelectorAll('.playerListItem'+i);
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
    showClubList(id){
      const listItem = document.getElementById('clubList'+id);
      if (listItem.classList.contains('hidden')){
        listItem.classList.remove('hidden');
      }else{
        listItem.classList.add('hidden');
      }
    },
    showPlayerList(id){
      const listItem = document.getElementById('playerList'+id);
      if (listItem.classList.contains('hidden')){
        listItem.classList.remove('hidden');
      }else{
        listItem.classList.add('hidden');
      }
    },
    hideClubList(id, clubDeets){
      this.state.init.create_game[0].clubs[id] = clubDeets
      this.showClubList(id)
    },
    hidePlayerList(id, playerDeets){
      this.showPlayerList(id)
      playerDeets['display'] = {"display": "Default", "display_id": 1}
      this.state.init.create_game[0].competitors[id] = playerDeets
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
  overflow: hidden;
  margin: 20px auto;
  /*padding: 20px;*/
  background-color: #fff;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.player {
  max-width: 600px;
  max-height: 400px;
  overflow: scroll;
  overflow: hidden;
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
.clubListItem1 {
  padding: 10px;
  margin: 5px 0;
  background-color: #f9f9f9;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.clubListItem1:hover {
  background-color: #e9e9e9;
}
.clubListItem2 {
  padding: 10px;
  margin: 5px 0;
  background-color: #f9f9f9;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.clubListItem2:hover {
  background-color: #e9e9e9;
}
.playerListItem1 {
  padding: 10px;
  margin: 5px 0;
  background-color: #f9f9f9;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.playerListItem1:hover {
  background-color: #e9e9e9;
}
.playerListItem2 {
  padding: 10px;
  margin: 5px 0;
  background-color: #f9f9f9;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.playerListItem2:hover {
  background-color: #e9e9e9;
}
.hidden {
  display: none;
}
</style>