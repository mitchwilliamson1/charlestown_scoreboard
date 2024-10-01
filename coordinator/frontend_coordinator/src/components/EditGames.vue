<template>
  <div class="edit">
    <div v-if="gameOptions && details">
    <div class="card p-2 pt-0 shadow">
        <form>
          <div class="row">
            <div class="col-3">
              <label class="form-label">Winner</label>
              <select class="form-select" v-model="details.winner">
                <option value="1">Team 1</option>
                <option value="2">Team 2</option>
              </select>
            </div>
            <div class="col-3" v-for="player, index in details['competitors']">
              <label class="form-label">Team {{n}} Score</label>
              <select class="form-select" v-model="player.score">
                <option v-for="n, index in 100" :value="index">{{index}}</option>
              </select>
            </div>

            <div class="col-3">
              <label class="form-label">Rink</label>
              <select class="form-select" v-model="details.rink">
                <option v-for="rink in gameOptions['rink']" :value="rink">{{rink.rink}}</option>
              </select>
            </div>

            <div class="col-3">
            </div>

            <div class="col-3" v-for="player, index in details['competitors']">
              <label class="form-label">Team {{n}} Score</label>
              <select class="form-select" v-model="player.display">
                <option v-for="display in gameOptions['display']" :value="display">{{display.display}}</option>
              </select>
            </div>

            <div class="col-3">
              <label class="form-label">Sponsor</label>
              <select class="form-select" v-model="details.sponsor">
                <option v-for="sponsor in gameOptions['sponsor']" :value="sponsor">{{sponsor.sponsor}}</option>
              </select>
            </div>
          </div>

          <div class="row p-3">
            <div class="col-6">
              <button type="submit" @click="updateGame" class="btn btn-primary">Update</button>
            </div>
            <div class="col-6">
              <button type="submit" @click="finishGame" class="btn btn-primary">Finish Game</button>
            </div>
          </div>

        </form>
      </div>
    </div>

  </div>
</template>

<script>
import { reactive, onMounted } from "vue";
import axios from 'axios'

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

    var path = 'http://127.0.0.1:8000/games'

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
      axios.post(this.path+'/update_game', {
      update_game: this.details,
      })
      .then( (response) => {
        console.log(response);
        this.$emit('reload')
      })
      .catch( (error) => {
        console.log(error);
      });
    },
    finishGame() {
      axios.post(this.path+'/finish_game', {
      finish_game: this.details,
      })
      .then( (response) => {
        console.log(response);
        this.$emit('reload')
      })
      .catch( (error) => {
        console.log(error);
      });
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
