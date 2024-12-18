<template>
  <div class="h-100 w-100" style="background-color: black;">
    <div class="container p-0 h-100 w-100">
      <div class="row h-50 w-100 m-0 p-0">
        <template v-for="board in state.scoreboards">
          <div class="col  w-100 h-100 m-1">
            <Scoreboard class="" :detail="board"/>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, onMounted } from "vue";
import axios from 'axios'
import Scoreboard from './Scoreboard.vue'


export default {
  name: 'Backboard',
  components: {
    Scoreboard,
  },
  data(){
    return{
      path: "",
    }
  },
  setup() {
    const state = reactive({
      scoreboards: null,
    });

    var path = ""
    if (process.env.NODE_ENV == 'development'){
      path = 'http://127.0.0.1:8083/'
    }else{
      path = window.location.toString();
    }

    onMounted(async () => {
      getScoreboards()
    })

    function getScoreboards() {
      axios.get(path+'get_scoreboards')
      .then(function (response) {
        if (response.status == 200){
          state.scoreboards = response.data
        }
      })
      .catch(function (error) {
        console.log("ERROR ", error);
      })
      .then(function () {
        setTimeout(getScoreboards, 1000)
      });
    }

    return {
      path,
      state
    };
  },
  methods:{
    addRow() {
      (async () => {
      const Response = await fetch(this.path+'/add_row', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        mode: 'no-cors',
      })
      const addContent = await Response.json();
      console.log(addContent);
      })();
    },
    tabSelect(id) {
      for (const tab in this.selected){
        console.log(tab, id)
        if (id == tab){
          this.selected[tab] = true
        } else {
          this.selected[tab] = false
        }
      }
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
  },
}
</script>
<style scoped type="text/css">
.container {
  max-width: 100%;
  /*margin: 0%;*/
}
.row {
  max-width: 100%;
  /*margin: 0%;*/
}
</style>
