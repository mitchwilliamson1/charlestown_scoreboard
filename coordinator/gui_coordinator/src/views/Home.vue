<template>
  <div class="home">
    <img style="-webkit-filter: grayscale(1);" alt="Vue logo" src="../assets/family.jpg">
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: 'Home',
  components: {
  }
}
</script>

<style scoped type="text/css">
  img {
    width: 80%;
    filter: gray; /* IE6-9 */
    -webkit-filter: grayscale(1); /* Google Chrome, Safari 6+ & Opera 15+ */
    filter: grayscale(1); /* Microsoft Edge and Firefox 35+ */
}

/* Disable grayscale on hover */
img:hover {
    -webkit-filter: grayscale(0);
    filter: none;
}
</style>