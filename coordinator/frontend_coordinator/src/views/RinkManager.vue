<template>
  <div class="home">
    <div class="row">

      <div class="col">
        <div class="bg-secondary p-3 text-white" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight" aria-controls="offcanvasRight">New Board</div>

      <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasRight" aria-labelledby="offcanvasRightLabel">
        <div class="offcanvas-header">
          <h5 id="offcanvasRightLabel">New Rink</h5>
          <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">
          
          <div class="row">
            <div class="col-4">Rink Name</div>
            <input class="col" v-model="createRink.rink" type="text">
          </div>
          <div class="row">
            <div class="col-4">IP Address</div>
            <input class="col" v-model="createRink.ip" type="text">
          </div>

          <div class="">
            <button @click="createRinkButton(this.createRink)" class="btn btn-success">Create Rink</button>
          </div>

          <div class="row">
            <div class="col-4">Masterboard Name</div>
            <input class="col" v-model="createMasterboard.masterboard" type="text">
          </div>
          <div class="row">
            <div class="col-4">IP Address</div>
            <input class="col" v-model="createMasterboard.ip" type="text">
          </div>

          <div class="">
            <button @click="createMasterboardButton(this.createMasterboard)" class="btn btn-success">Create Masterboard</button>
          </div>
        </div>
      </div>

        <div class="row">
          <div v-if="state.rinks" class="col-12">
            <current-rinks :rinks="state.rinks" :masterboards="state.masterboards"/>
          </div>
        </div>
  
      </div>
    </div>
    
  </div>
</template>

<script>
import { reactive, onMounted } from "vue";
import CurrentRinks from '../components/CurrentRinks.vue'
import axios from 'axios'
import { DateTime } from "luxon";

export default {
  name: 'PlayersView',
  components: {
    CurrentRinks,
  },
  data() {
    return {
      createRink: {
        'rink':null,
        'ip':null,
      },
      createMasterboard: {
        'masterboard':null,
        'ip':null,
      }
    }
  },
  setup() {
    const state = reactive({
      rinks: null,
      masterboards: null,
    });

    var path = ""
    if (process.env.NODE_ENV == 'development'){
      path = 'http://127.0.0.1:8000/'
    }else{
      path = window.location.toString();
    }
    
    onMounted(async () => { 
      getRinks()
      getMasterboards()
    });
    function createRinkButton(rink) {
      axios.post(path+'games/create_rink', {
      create_rink: rink,
      })
      .then(function (response) {
        console.log(response);
        getRinks()
      })
      .catch(function (error) {
        console.log(error);
      });
    }
    function createMasterboardButton(masterboard) {
      axios.post(path+'games/create_masterboard', {
      create_masterboard: masterboard,
      })
      .then(function (response) {
        console.log(response);
        getMasterboards()
      })
      .catch(function (error) {
        console.log(error);
      });
    }
    function getRinks() {
      axios.get(path+'games/get_rinks')
      .then(function (response) {
        if (response.status == 200){
          console.log("RESPONSE ", response.data);
          state.rinks = response.data
        }
      })
      .catch(function (error) {
        // handle error
        console.log("ERROR ", error);
      })
      .then(function () {
        // always executed
      });
    }
    function getMasterboards() {
      axios.get(path+'games/get_masterboards')
      .then(function (response) {
        if (response.status == 200){
          console.log("RESPONSE ", response.data);
          state.masterboards = response.data
        }
      })
      .catch(function (error) {
        // handle error
        console.log("ERROR ", error);
      })
      .then(function () {
        // always executed
      });
    }

    return {
      path,
      state,
      getRinks,
      createRinkButton,
      createMasterboardButton,
    };
  },
  methods: {

  }
}
</script>
<style type="text/css" scoped>

</style>