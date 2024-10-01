<template>
  <div class="edit">
    <div class="card p-2 pt-0 shadow">
      <div class="container">

        <form class="row">
          <div class="p-0 m-0">
            <label class="form-label">Name</label>
            <input type="text" class="form-control" v-model="club.club_name">
          </div>
          <div class="p-0 m-0">
            <label class="form-label">Address</label>
            <input type="text" class="form-control" v-model="club.address">
          </div>
          <div class="p-0 m-0">
            <label class="form-label">Contact</label>
            <input type="text" class="form-control" v-model="club.contact_details">
          </div>
          <div class="p-0 m-0">
            <label class="form-label w-100">Logo</label>
            <div class="col">{{club.logo}}</div>
              <input type="file" ref="file" @change="onChange($event)" class="">
          </div>
        </form>
      </div>
      <div class="col-12">
        <button @click="updateClub()" class="btn btn-primary">Update</button>
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
    club: Object,
  },

  setup(props, context) {
    const state = reactive({
      someData: null,
    });

    const createClub = reactive({
        name:null,
        logo:null,
        address: null,
        contact: null,
      });

    var path = 'http://127.0.0.1:8000/'

    function onChange(event) {
      createClub.logo = event.target.files[0]
    }

    function updateClub() {
      let data = new FormData();
      data.append('file', createClub.logo);
      data.append('club', JSON.stringify(props.club));

      axios.post(path+'players/update_club',
      data,
      {headers: {
        'Content-Type': 'multipart/form-data'
        }
      })
      .then(function (response) {
        console.log("THEN: ", response)
        if (response.data == "No File Uploaded"){
          alert(response.data)
        } else {
          console.log(response);
          context.emit("reLoadClubs")
        }
      })
      .catch(function (error) {
        console.log("ERROR", error);
      });
    }
    
    onMounted(async () => { 
    });

    return {
      path,
      state,
      createClub,
      onChange,
      updateClub
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
