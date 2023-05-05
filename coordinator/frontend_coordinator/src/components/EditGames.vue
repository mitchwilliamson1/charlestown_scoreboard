<template>
  <div class="edit">
    <div v-if="gameOptions">
    <div class="card p-2 pt-0 shadow">

        <form class="row">
          <div class="col-6">
            <label class="form-label">Game Name</label>
            <input class="form-control" v-model="details.name">
          </div>
          <div class="col-6">
            <label class="form-label">Rink</label>
            <!-- fix this: needs to v-model the whole object to start with not just the number 1 -->
            <select class="form-select" v-model="details.rink">
              <option v-for="rink in gameOptions['rink']" :value="rink">{{rink.rink}}</option>
            </select>
          </div>
          <div class="col-3">
            <label class="form-label">Type</label>
            <select class="form-select" v-model="details.type">
              <option v-for="game in gameOptions['type']" :value="game.type_id">{{game.type}}</option>
            </select>
          </div>
          <div class="col-3">
            <label class="form-label">Winner</label>
            <select class="form-select" v-model="details.winner">
              <option v-for="game in details['competitors']" :value="game">{{game.first_name}}</option>
            </select>
          </div>
          <div class="col-3">
            <label class="form-label">{{details['competitors'][0]['first_name']}}'s Score</label>
            <select class="form-select" v-model="details['competitors'][0]['score']">
              <option v-for="n, index in 100" :value="index">{{index}}</option>
            </select>
          </div>
          <div class="col-3">
            <label class="form-label">{{details['competitors'][1]['first_name']}}'s Score</label>
            <select class="form-select" v-model="details['competitors'][1]['score']">
              <option v-for="n, index in 100" :value="index">{{index}}</option>
            </select>
          </div>
          <!-- <div class="col-6">
            <label class="form-label">Gender</label>
            <select class="form-select" v-model="details.gender">
              <option v-for="game in gameOptions['gender']" :value="game.gender_id">{{game.gender}}</option>
            </select>
          </div>
          <div class="col-6">
            <label  class="form-label">Round</label>
            <select class="form-select" v-model="details.round">
              <option v-for="game in gameOptions['round']" :value="game.round_id">{{game.round}}</option>
            </select>
          </div>
          <div class="col-6">
            <label class="form-label">Level</label>
            <select class="form-select" v-model="details.level">
              <option v-for="game in gameOptions['level']" :value="game.level_id">{{game.level}}</option>
            </select>
          </div>
          <div class="col-6">
            <label class="form-label">Grade</label>
            <select class="form-select" v-model="details.grade">
              <option v-for="game in gameOptions['grade']" :value="game.grade_id">{{game.grade}}</option>
            </select>
          </div> -->
          <div class="row p-3">
            <div class="col-6">
              <button type="submit" @click="updateGame" class="btn btn-primary">Update</button>
            </div>
            <div class="col-6">
              <button type="submit" @click="finishGame" class="btn btn-primary">Finsih Game</button>
            </div>
          </div>
        </form>
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
    path = 'http://127.0.0.1:8000/games'

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
