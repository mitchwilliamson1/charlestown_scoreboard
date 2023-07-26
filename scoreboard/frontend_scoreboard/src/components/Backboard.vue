<template>
  <div v-if="state.game" class="h-100 w-100">
    <BPL v-if="state.game.competition == 'BPL'" class="h-100" :detail="state.game"/>
    <Scoreboard v-else class="h-100" :detail="state.game"/>
  </div>
</template>

<script>
import { reactive, onMounted } from "vue";
import axios from 'axios'
import Scoreboard from './Scoreboard.vue'
import BPL from './BPL.vue'
 

export default {
  name: 'Backboard',
  components: {
    Scoreboard,
    BPL,
  },
  data(){
    return{
      path: "",
    }
  },
  setup() {
    const state = reactive({
      game: null,
    });

    var path = ""
    if (process.env.NODE_ENV == 'development'){
      path = 'http://127.0.0.1:8081/'
    }else{
      path = window.location.toString();
    }

    onMounted(async () => {
      getGame()
    })

    function getGame() {
      axios.get(path+'get_game')
      .then(function (response) {
        if (response.status == 200){
          state.game = response.data[0]
        }
      })
      .catch(function (error) {
        console.log("ERROR ", error);
      })
      .then(function () {
        setTimeout(getGame, 1000)
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

</style>
