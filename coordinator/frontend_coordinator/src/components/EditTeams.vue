<template>
  <div class="edit">
    <form class="row g-3">
      <div class="col-md-6">
        <label for="inputEmail4" class="form-label">Name</label>
        <input type="text" class="form-control" id="inputEmail4" v-model="team.team_name">
      </div>
      <div class="col-md-6">
        <label for="inputPassword4" class="form-label">Address</label>
        <input type="text" class="form-control" id="inputPassword4" v-model="team.address">
      </div>
      <div class="col-md-6">
        <label for="inputPassword4" class="form-label">Contact</label>
        <input type="text" class="form-control" id="inputPassword4" v-model="team.contact_details">
      </div>
      <div class="col-md-6">
        <label for="inputPassword4" class="form-label w-100">Logo</label>
        <input type="file" ref="file" @change="onChange($event)" class="col">
        <img class="logo" :src="'http://127.0.0.1:8000/players/get_logo/'+team.logo" >
      </div>
    </form>
      <div class="col-12">
        <button @click="updateTeam(team)" class="btn btn-primary">Update</button>
      </div>

  </div>
</template>

<script>
import { reactive, onMounted } from "vue";
import axios from 'axios'


export default {
  name: 'EditGames',
  props: {
    team: Object,
  },

  setup() {
    const state = reactive({
      someData: null,
    });

    const createTeam = reactive({
        name:null,
        logo:null,
        address: null,
        contact: null,
      });

    var path = ""
    if (process.env.NODE_ENV == 'development'){
      path = 'http://127.0.0.1:8000/'
    }else{
      path = window.location.toString();
    }

    function onChange(event) {
      createTeam.logo = event.target.files[0]
    }

    function updateTeam(team) {
      let data = new FormData();
      data.append('file', team.logo);
      data.append('team', JSON.stringify(team));

      console.log("name: ", JSON.stringify(team))

      axios.post(path+'players/update_team',
      data,
      {headers: {
        'Content-Type': 'multipart/form-data'
        }
      })
      .then(function (response) {
        console.log(response);
        getTeams()
      })
      .catch(function (error) {
        console.log(error);
      });
    }
    
    onMounted(async () => { 
    });

    return {
      path,
      state,
      createTeam,
      onChange,
      updateTeam
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

.logo {
  width: 40%;
  display: block;
  margin-left: auto;
  margin-right: auto;
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
