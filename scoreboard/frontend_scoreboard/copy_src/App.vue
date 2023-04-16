<template>
  <div class="routeContainer">

    <!-- <router-link to="/"> Scoreboard </router-link> -->
    <!-- <router-link to="/sponsor"> Sponsor </router-link> -->
    <!-- <router-link to="/weather"> Weather </router-link> -->

    <router-view v-slot='{ Component }'>
      <transition 
        enter-active-class="animate__animated animate__fadeInLeft"
        leave-active-class="animate__animated animate__fadeOutLeft"
        name="slide"
        mode="out-in"
        >
        <component :is="Component"/>
      </transition>
    </router-view>

  </div>
</template>

<script>

export default {
  name: 'App',
  components: {
  }
}
</script>
<style type="text/css">
.routeContainer {
  background-color: #2b2b2b;
  }

a {
  font-weight: 40%;
  color: grey;
  text-decoration: none;
  margin-right: 1em;
  }

a:hover,
a:router-link-active {
  border-bottom: 2px solid yellow;
}

</style>
