<template>
  <div class="p-3">
    <div class="row">
      <div class="col-2 border-end border-2 bg-light text-dark p-3">
        <div class="container" id="nav">
          <div class="row p-3">
            <router-link class="link" to="/">Games</router-link>
          </div>
          <div class="row p-3">
            <router-link class="link" to="/players">Players</router-link>
          </div>
          <div class="row p-3">
            <router-link class="link" to="/teams">Teams</router-link>
          </div>
          <div class="row p-3">
            <router-link class="link" to="/rinkmanager">Manage Rinks </router-link>
          </div>
          <div class="row p-3">
            <router-link class="link" to="/about">About </router-link>
          </div>
        </div>
      </div>
      <div class="col">
        <div>
          <router-view/>
        </div>
      </div>
    </div>
  </div>
</template>

<style >
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 100%;
  padding: 0;
}
</style>
