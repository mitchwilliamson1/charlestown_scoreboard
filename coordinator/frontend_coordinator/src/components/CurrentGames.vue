<template>
  <div v-if="game && gameOptions" class="currentGames">
    <div class="container">
      <div class="row shadow p-1 m-0 bg-body rounded"
        data-bs-toggle="collapse" 
        :data-bs-target="'#collapse'+game.game_id" 
        aria-expanded="false" 
        aria-controls="collapseOne">
        <div class="col-2">{{gameType(game)}}</div>
        <div :class="winner(game.winner, competitor.player_id)" class="col-3" v-for="competitor, index in game.competitors">
            <div class="p-0 m-0" >{{competitor.first_name[0]}}.{{competitor.last_name}}</div>
            <div>Score: {{competitor.score}}</div>
        </div>
        <div class="col-2">{{game.sponsor.sponsor}}</div>
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
      return game.competition.competition
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
