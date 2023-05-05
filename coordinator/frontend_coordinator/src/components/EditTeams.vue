<template>
  <div class="edit">
    <div class="card p-2 pt-0 shadow">

      <form class="row">
        <div class="">
          <label class="form-label">Name</label>
          <input type="text" class="form-control" v-model="team.team_name">
        </div>
        <div class="">
          <label class="form-label">Address</label>
          <input type="text" class="form-control" v-model="team.address">
        </div>
        <div class="">
          <label class="form-label">Contact</label>
          <input type="text" class="form-control" v-model="team.contact_details">
        </div>
        <div class="">
            <label class="form-label w-100">Logo</label>
          <div class="row border rounded p-1">
            <div class="col">{{team.logo}}</div>
            <input type="file" ref="file" @change="onChange($event)" class="col">
          </div>
        </div>
      </form>
      <div class="col-12">
        <button @click="updateTeam(team)" class="btn btn-primary">Update</button>
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
    path = 'http://127.0.0.1:8000/'

    function onChange(event) {
      createTeam.logo = event.target.files[0]
    }

    function updateTeam(team) {
      let data = new FormData();
      data.append('file', createTeam.logo);
      data.append('team', JSON.stringify(team));

      console.log("name:")
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
