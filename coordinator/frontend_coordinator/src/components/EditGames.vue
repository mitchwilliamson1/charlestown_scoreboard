<template>
  <div class="edit">
    <div class="row" v-for="item, key in details[0]">
      <div class="col-4">{{capitalise(key)}}</div>
      <select class="form-select col">
        <option v-for="type in item" :value="type">{{item}}</option>
      </select>
    </div>

  </div>
</template>

<script>
import { reactive, onMounted } from "vue";

export default {
  name: 'EditGames',
  props: {
    details: Object,
    gameOptions: Object,
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
    filterDict(teamName) {
      return this.state.players.filter(i => i.team == teamName)
    },
    capitalise(key) {
      return key.charAt(0).toUpperCase() + key.slice(1);
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
