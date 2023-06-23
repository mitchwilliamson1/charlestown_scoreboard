<template>
  <div class="edit">
    <div class="card p-2 pt-0 shadow">
    <form class="row g-3">
      <div class="col-md-4">
        <label for="inputEmail4" class="form-label">First Name</label>
        <input class="form-control" id="inputEmail4" v-model="player.first_name">
      </div>
      <div class="col-md-4">
        <label class="form-label">Last Name</label>
        <input class="form-control" id="inputPassword4" v-model="player.last_name">
      </div>
      <div class="col-4">
        <label  class="form-label">Club</label>
        <select class="form-select" v-model="player.club">
          <option v-for="club in clubs" :value="club.club_id">{{club.club_name}}</option>
        </select>
      </div>
      <div class="col-6">
        <label class="form-label">Bowls Number</label>
        <input type="text" class="form-control" id="inputAddress" v-model="player.bowls_number">
      </div>
      <div class="col-6">
        <label class="form-label">Grade</label>
        <select class="form-control" v-model="player.grade" type="text">
          <option v-for="num in 7" :value="num">{{num}}</option>
          <option :value="'None'">None</option>
        </select>
      </div>
    <div class="col-12">
      <button type="submit" @click="updatePlayer" class="btn btn-primary">Update</button>
    </div>
    </form>
    </div>

  </div>
</template>

<script>
import { reactive, onMounted } from "vue";

export default {
  name: 'EditGames',
  props: {
    player: Object,
    clubs: Object,
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
    clubName(playerClub){
      var club = this.clubs.filter(i => i.club_id == playerClub)
      return club[0]['club_name']
    },
    updatePlayer() {
      (async () => {
      const rawResponse = await fetch(this.path+'/update_player', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        mode: 'no-cors',
        body: JSON.stringify(this.player)
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
