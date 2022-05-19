<template>
  <div id="nav">
    <router-link class="link" to="/">Home</router-link>
    <router-link class="link" to="/budget">Budget</router-link>
    <router-link class="link" to="/about">About</router-link>
  </div>
  <router-view/>
</template>

<style >
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background-color: #3d3d3d;
  height: 100%;
}

.offcanvas-body {
 display: flex;
 flex-direction: column;
 gap: 1rem;
}

#websiteTitle{
  width: 100%;
  height: 50px; 
  color: white;
  background-color: #2a2a2a;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
