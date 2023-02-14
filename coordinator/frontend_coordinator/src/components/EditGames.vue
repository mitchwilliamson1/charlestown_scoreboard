<template>
  <div class="edit">
    {{details}}
    <div v-if="gameOptions">
      <form class="row">
        <div class="col-6">
          <label for="inputEmail4" class="form-label">Game Name</label>
          <input class="form-control" id="inputEmail4" v-model="details[0].name">
        </div>
        <div class="col-6">
          <label for="inputAddress2" class="form-label">Type</label>
          <select class="form-select" v-model="details[0].type">
            <option v-for="game in gameOptions['type']" :value="game.type_id">{{game.type}}</option>
          </select>
        </div>
        <div class="col-6">
          <label for="inputAddress2" class="form-label">Gender</label>
          <select class="form-select" v-model="details[0].gender">
            <option v-for="game in gameOptions['gender']" :value="game.gender_id">{{game.gender}}</option>
          </select>
        </div>
        <div class="col-6">
          <label for="inputAddress2" class="form-label">Round</label>
          <select class="form-select" v-model="details[0].round">
            <option v-for="game in gameOptions['round']" :value="game.round_id">{{game.round}}</option>
          </select>
        </div>
        <div class="col-6">
          <label for="inputAddress2" class="form-label">Rink</label>
          <select class="form-select" v-model="details[0].rink">
            <option v-for="game in gameOptions['rink']" :value="game">{{game.rink}}</option>
          </select>
        </div>
        <div class="col-6">
          <label for="inputAddress2" class="form-label">Level</label>
          <select class="form-select" v-model="details[0].level">
            <option v-for="game in gameOptions['level']" :value="game.level_id">{{game.level}}</option>
          </select>
        </div>
        <div class="col-6">
          <label for="inputAddress2" class="form-label">Grade</label>
          <select class="form-select" v-model="details[0].grade">
            <option v-for="game in gameOptions['grade']" :value="game.grade_id">{{game.grade}}</option>
          </select>
        </div>
        <div class="col-6">
          <label for="inputAddress2" class="form-label">Winner</label>
          <select class="form-select" v-model="details[0].winner">
            <option v-for="game in details[0]['competitors']" :value="game">{{game.first_name}}</option>
          </select>
        </div>
      </form>
      <div class="row p-3">
        <div class="col-6">
          <button type="submit" @click="updateGame" class="btn btn-primary">Update</button>
        </div>
        <div class="col-6">
          <button type="submit" @click="finishGame" class="btn btn-primary">Finsih Game</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import { reactive, onMounted } from "vue";

export default {
  name: 'EditGames',
  props: {
    details: Object,
    gameOptions: Object,
  },

  setup() {
    const state = reactive({
      someData: null,
    });

    var path = ""
    if (process.env.NODE_ENV == 'development'){
      path = 'http://127.0.0.1:8000/games'
    }else{
      path = window.location.toString();
    }

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
    filterDict(teamName) {
      return this.state.players.filter(i => i.team == teamName)
    },
    capitalise(key) {
      return key.charAt(0).toUpperCase() + key.slice(1);
    },
    updateGame() {
      (async () => {
      const rawResponse = await fetch(this.path+'/update_game', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        mode: 'no-cors',
        body: JSON.stringify(this.details)
      })
      const content = await rawResponse.json();
      console.log(content);
      })();
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
