<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <button v-on:click="post" style="margin-top: 20px; width: 75%; height: 50px;">CLIIIIIICK!!</button>
  </div>
</template>

<script>
export default {
  name: 'ToDo',
  props: {
    msg: String
  },
    methods:{
    post() {
      (async () => {
      const rawResponse = await fetch('http://127.0.0.1:8000/budget/save', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        },
        mode: 'no-cors',
        body: JSON.stringify({ x: 5, y: 6 })
      });
      const content = await rawResponse.json();
      console.log(content);
      })();
    },
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
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
