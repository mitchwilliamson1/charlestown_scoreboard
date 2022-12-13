<template>
  <div class="edit">
    <form class="row g-3">
      <div class="col-md-6">
        <label for="inputEmail4" class="form-label">Rink</label>
        <input type="text" class="form-control" id="inputEmail4" v-model="rinks.rink" >
      </div>
      <div class="col-md-6">
        <label for="inputPassword4" class="form-label">Ip Address</label>
        <input type="text" class="form-control" id="inputPassword4"  v-model="rinks.ip">
      </div>
    </form>
      <div class="col-12">
        <button @click="updateRink" type="submit" class="btn btn-primary">Update</button>
      </div>

  </div>
</template>

<script>
import { reactive, onMounted } from "vue";

export default {
  name: 'EditGames',
  props: {
    rinks: Object,
  },

  setup() {
    const state = reactive({
      someData: null,
    });

    var path = ""
    if (process.env.NODE_ENV == 'development'){
      path = 'http://127.0.0.1:8000/games'
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
