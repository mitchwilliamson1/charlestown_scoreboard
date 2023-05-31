<template>
  <div class="currentGames">
    <div class="container">
      <div class="row">
        <div class="col fw-bold">Game</div>
        <div class="col fw-bold">Players</div>
        <div class="col fw-bold">Rink</div>
      </div>
      <div v-for="game, i in games" :key="i">
        <div class="row shadow p-2 mb-1 bg-body rounded"
          data-bs-toggle="collapse" 
          :data-bs-target="'#collapse'+game.game_id" 
          aria-expanded="false" 
          aria-controls="collapseOne">
          <div class="col">{{game.name}}</div>
          <div class="col">
            <div class='row'>
              <div class="col" :class="winner(player.first_name, game.winner)" v-for="player in game.competitors">{{player.first_name}} - {{player.score}}</div>
            </div>
          </div>
          <div class="col">{{game.rink.rink}}</div>
        </div>
        <div class="row p-2">
          <div class="col collapse"
            :id="'collapse'+game.game_id"
            data-parent="#accordion">
            <edit-games :details="game" :gameOptions="gameOptions"/>
          </div>
          
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, onMounted } from "vue";
import EditGames from '../components/EditGames.vue'


export default {
  name: 'CurrentGames',
  components: {
    EditGames
  },
  props: {
    games: Object,
    teams: Object,
    gameOptions: Object,
  },

  setup() {
    const state = reactive({
      someData: null,
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
    winner(name, winner) {
      if (name == winner){
        return {
          rounded:true,
          border: true,
          'border-success': true
        }
      }
    },
    post() {
      (async () => {
      const rawResponse = await fetch(this.path+'/save', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        mode: 'no-cors',
        body: JSON.stringify(this.state)
      })
      const content = await rawResponse.json();
      console.log(content);
      })();
    },
    edit(game) {
      console.log(game)
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
