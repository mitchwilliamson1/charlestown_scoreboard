<template>
  <div class="edit">
    <form class="row g-3">
      <div class="col-md-6">
        <label for="inputEmail4" class="form-label">Rink</label>
        <input type="text" class="form-control" id="inputEmail4" v-model="masterboard.rink">
      </div>
      <div class="col-md-6">
        <label for="inputPassword4" class="form-label">Ip Address</label>
        <input type="text" class="form-control" id="inputPassword4" v-model="masterboard.ip">
      </div>
    </form>
    <br>
    <div>Show Rinks</div>
    {{state.ips}}
    <div v-for="ip, i in state.ips" class="form-check form-check-inline">
        <input class="form-check-input" type="checkbox" id="inlineCheckbox1" v-model="ip.show">
        <label class="form-check-label" for="inlineCheckbox1">{{ip.ip}}</label>
    </div>

    <div class="col-12">
      <button @click="updateRink" type="submit" class="btn btn-primary">Update</button>
    </div>
    

  </div>
</template>

<script>
import { reactive, onMounted } from "vue";
import axios from 'axios'

export default {
  name: 'EditMasterboards',
  props: {
    masterboard: Object,
    rinks: Object,
  },

  setup(props) {
    const state = reactive({
      ips: [],
    });

    const addRemoveIp = e => {
      console.log("!!!!!!!!!!", e)
      // if (e.target.value === 'Jhon') sayHello()
    }

    var path = ""
    if (process.env.NODE_ENV == 'development'){
      path = 'http://127.0.0.1:8000/games'
    }else{
      path = window.location.toString();
    }

    onMounted(async () => {
      // getMasterboard()
      getIpList()
    });
    function getIpList() {
      var blah = props.masterboard.rink_ips.map(( e ) => {
        return e.rink_id
      });
      state.ips = props.rinks.map(( e ) => {
        e.show = blah.includes(e.rink_id)
        return e
      });
    }

    function getMasterboard() {
      axios.get(path+'/get_masterboard', 
        { params: { rink: props.masterboard.ip } })
      .then(function (response) {
        if (response.status == 200){
          state.ips = ['127.0.0.1:8080', '127.0.0.2:885']
          state.ips = response.data
        }
      })
      .catch(function (error) {
        console.log("ERROR ", error);
      })
      .then(function () {

      });
    }

    return {
      path,
      addRemoveIp,
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
    updateRink() {
      (async () => {
      const rawResponse = await fetch(this.path+'/update_rink', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        mode: 'no-cors',
        body: JSON.stringify(this.rinks)
      })
      const content = await rawResponse.json();
      console.log(content);
      })();
    },
    addRemove(ip){
      console.log(ip)
      this.state.ips.push(ip)
    },
    addIP(){
      this.state.ips.push("")
    },
    removeIP(key){
      this.state.ips.splice(key, 1)
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
