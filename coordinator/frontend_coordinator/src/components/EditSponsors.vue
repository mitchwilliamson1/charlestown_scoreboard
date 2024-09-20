<template>
  <div class="edit">
    <div class="card p-2 pt-0 shadow">
      <div class="container">
        <form class="row">
          <div class="">
            <label class="form-label">Name</label>
            <input type="text" class="form-control" v-model="sponsor.sponsor">
          </div>
          <div class="">
            <label class="form-label w-100">Logo</label>
            <div class="row border rounded p-1">
              <input type="file" @change="onChange($event)">
            </div>
          </div>
        </form>
      </div>

      <div class="col-12">
        <button @click="updateSponsor(sponsor)" class="btn btn-primary">Update</button>
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
    sponsor: Object,
  },

  setup(props, context) {
    const state = reactive({
      someData: null,
    });

    const createSponsor = reactive({
        name:null,
        logo:null,
      });

    var path = 'http://127.0.0.1:8000/'

    function onChange(event) {
      createSponsor.logo = event.target.files[0]
    }

    function updateSponsor() {
      let data = new FormData();
      console.log("SPON OBJ: ", props.sponsor)
      data.append('file', createSponsor.logo);
      data.append('sponsor_name', JSON.stringify(props.sponsor));

      axios.post(path+'games/update_sponsor',
      data,
      {headers: {
        'Content-Type': 'multipart/form-data'
        }
      })
      .then(function (response) {
        console.log(response);
        context.emit("reLoadSponsors")
        // getSponsors()
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
      createSponsor,
      onChange,
      updateSponsor
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
