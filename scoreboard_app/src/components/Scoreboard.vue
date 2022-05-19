<template>
  <div class="teamAndTime">
    <img class="logo" src="../assets/tigers.jpg">
    <div class="timer">
      <Counter/>
    </div>
    <img  class="logo" src="../assets/lowlands.jpg">
  </div>

  <div class="scores">
    <div class="ticker">
      <Ticker msg="Team Name" />
    </div>
    <div class="ticker">
      <Ticker msg="Team Name" />
    </div>
  </div>

</template>

<script>
import Ticker from './Ticker.vue'
import Counter from './Counter.vue'


export default {
  name: 'Board',
  components: {
    Ticker,
    Counter
  }
}
</script>
<style scoped type="text/css">
.teamAndTime{
  display: flex;
  align-items: center;
  justify-content: center;;
  background-color: #262626;
  padding: 50px;
}
.scores{
  display: flex;
  align-items: center;
  flex-wrap: nowrap;
  justify-content: space-around;
  background-color: #262626;
  padding-bottom: 50px;
}
/*.ticker{
  border-style: dashed;
  height: 100%;
  border-color: white;
}*/
.timer{
  width: 40%;
  height: 300px;
}

.logo{
  height: 250px;
}


flex-grow: 4;
</style>
