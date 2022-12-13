<template>
  <div class="hello">
  <div class="container">
    <div class="row">
      <div class="col fw-bold">Team</div>
      <div class="col fw-bold">First Name</div>
      <div class="col fw-bold">Last Name</div>
      <div class="col fw-bold">Address</div>
      <div class="col fw-bold">E-mail</div>
    </div>
    <div v-for="player, i in players" :key="i">
      <div class="row shadow p-2 mb-1 bg-body rounded"
        data-bs-toggle="collapse" 
        :data-bs-target="'#collapse'+i" 
        aria-expanded="false" 
        aria-controls="collapseOne">
      <div class="col">{{teamName(player.team)}}</div>
      <div class="col">{{player.first_name}}</div>
      <div class="col">{{player.last_name}}</div>
      <div class="col">{{player.address}}</div>
      <div class="col">{{player.email}}</div>
      </div>
      <div class="row p-2">
        <div class="col collapse"
          :id="'collapse'+i"
          data-parent="#accordion">
          <edit-player :teams="teams" :player="player"/>
        </div>
        
      </div>
    </div>
  </div>
  </div>
</template>

<script>
import { reactive, onMounted } from "vue";
import EditPlayer from '../components/EditPlayer.vue'


export default {
  name: 'CurrentPlayers',
  components: {
    EditPlayer
  },
  props: {
    players: Object,
    teams: Object,
  },

  setup() {
    const state = reactive({
      someData: null,
    });

    var path = ""
    if (process.env.NODE_ENV == 'development'){
      path = 'http://127.0.0.1:8000/budget'
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
    teamName(playerTeam){
      console.log("!!!!!!!!", playerTeam)
      console.log(this.teams.filter(i => i.team_id == playerTeam))
      var team = this.teams.filter(i => i.team_id == playerTeam)
      return team[0]['team_name']
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
