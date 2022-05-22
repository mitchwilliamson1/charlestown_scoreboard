<template>

  <div class="container">
  <div class="row teamAndTime">
    <div class="col-4 shadow p-1 mb-5 rounded">
      <div style="display: flex; align-items: center; height: 100%;">
        <img class="logo" src="../assets/tigers.jpg">
      </div>
    </div>
    <div class="col-4 shadow p-1 mb-5 rounded">
      <div style="height: 100%" class="ends">
        <!-- <div class="viewport"> -->
          <Ticker msg="ENDS" colour="black"/>
        <!-- </div> -->
      </div>
    </div>
    <div class="col-4 shadow p-1 mb-5 rounded">
      <div style="display: flex; align-items: center; height: 100%">
        <img  class="logo" src="../assets/lowlands.jpg">
      </div>
    </div>
  </div>

  <div class="row scores">
    <div class="col-6 shadow p-1 mb-5 rounded">
      <div style="height: 100%;" class="ticker">
        <div class="viewport">
          <Ticker msg="Team Name" colour="red"/>
        </div>
      </div>
    </div>
    <div class="col-6 shadow p-1 mb-5 rounded">
      <div style="height: 100%;" class="ticker">
        <div class="viewport">
          <Ticker msg="Team Name" colour="blue"/>
        </div>
      </div>
    </div>
  </div>
</div>

</template>

<script>
import Ticker from './Ticker.vue'


export default {
  name: 'Board',
  components: {
    Ticker,
  }
}
</script>

<style scoped type="text/css">
.row {
    background-color: #363535;
    height:50vh;
}

img {
  width: 100%;
}

.scores{
  display: flex;
  align-items: center;
  flex-wrap: nowrap;
  justify-content: space-around;
}

</style>
