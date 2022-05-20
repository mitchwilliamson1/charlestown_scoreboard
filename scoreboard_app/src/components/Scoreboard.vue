<template>
  <div class="teamAndTime">
    <img class="logo" src="../assets/tigers.jpg">

    <div style="width: 25%;" class="ends">
      <div class="viewport">
        <Ticker msg="ENDS"/>
      </div>
    </div>

    <img  class="logo" src="../assets/lowlands.jpg">
  </div>

  <div class="scores">
    <div class="ticker">
      <div class="viewport">
        <Ticker msg="Team Name" />
      </div>
    </div>
    <div class="ticker">
      <div class="viewport">
        <Ticker msg="Team Name" />
      </div>
    </div>
  </div>

</template>

<script>
import Ticker from './Ticker.vue'
import Ends from './Ends.vue'

// import Counter from './Counter.vue'


export default {
  name: 'Board',
  components: {
    Ticker,
    Ends,
    // Counter
  }
}
</script>
<style scoped type="text/css">
.teamAndTime{
  display: flex;
  align-items: flex-end;
  justify-content: center;;
  background-color: #262626;
  padding-bottom: 150px;
}
.viewport {
  padding: 10px;
/*  border-style: dashed;
  border-color: white;*/
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
.ends{
  width: 40%;
  height: 300px;
}

.logo{
  height: 250px;
}


flex-grow: 4;
</style>
