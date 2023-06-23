<template>
  <div v-if="game && gameOptions" class="currentGames">
    <div class="container">
      <div class="row">
        <div class="col-2 fw-bold">Game</div>
        <div class="col-4 fw-bold">Team 1</div>
        <div class="col-4 fw-bold">Team 2</div>
        <div class="col-2 fw-bold">Rink</div>
      </div>
      <div >
        <div class="row shadow p-2 mb-1 bg-body rounded"
          data-bs-toggle="collapse" 
          :data-bs-target="'#collapse'+game.game_id" 
          aria-expanded="false" 
          aria-controls="collapseOne">
          <div class="col-2">{{gameType(game)}}</div>
          <div :class="winner(n, game.winner)" class="col-4" v-for="n, index in 2">
            <div v-for="player in game.competitors">
              <div class="p-1" v-if="player.is_skipper && player.team == n " >Skipper: {{player.first_name[0]}}.{{player.last_name}} - Score: {{player.score}}</div>
            </div>
          </div>

          <div class="col-2">{{game.rink.rink}}</div>
        </div>
        <div class="row p-2">
          <div class="col collapse"
            :id="'collapse'+game.game_id"
            data-parent="#accordion">
            <edit-games @reload="$emit('reload')" :details="game" :gameOptions="gameOptions"/>
          </div>
          
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, onMounted } from "vue";
import EditGames from '../components/EditGames.vue'
import axios from 'axios'

export default {
  name: 'CurrentGames',
  components: {
    EditGames
  },
  props: {
    game: Object,
    gameOptions: Object,
  },

  setup() {
    const state = reactive({
      myGames: Object,
    });

    var path = ""
    path = 'http://127.0.0.1:8000/budget'

    onMounted(async () => {});

    return {
      path,
      state
    };
  },
  data(){
    return{
      isActive: false,
    }
  },
  created () {
  },
  mounted () {
  },

  computed: {
    
  },

  methods:{
    gameType(game){
      var gender = this.gameOptions.gender.filter(i => i.gender_id == game.gender)[0].gender
      var competition = this.gameOptions.competition.filter(i => i.competition_id == game.competition)[0].competition
      var game = this.gameOptions.game_type.filter(i => i.game_type_id == game.game_type)[0].game_type
      return gender +" "+ competition +" " + game
    },
    winner(team, winner) {
      if (team == winner){
        return {
          rounded:true,
          border: true,
          'border-success': true
        }
      }
    },
  },
}
</script>

<style scoped>

.flex-container {
  display: flex;
  justify-content: space-around;
}

.flex-child-spend {
  background-color: #b8fcbb;
  flex-grow: 1;
  border: 2px solid grey;
  margin: 5px;
  margin-top: 50px;
  margin-bottom: 80px;
  padding-bottom: 10px;
}

.flex-child {
  background-color: #e6dfcc;
  flex-grow: 1;
  border: 2px solid grey;
  margin: 2px;
}

input {
  width: 90%;
}

h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
