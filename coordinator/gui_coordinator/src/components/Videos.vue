<template>
  <div class="hello">
      <video :id="x" 
        :ref="this.videoUrl" 
        :src="this.videoUrl" 
        width="640" 
        height="480" 
        type="video/mp4" 
        autoplay
        preload="none" 
        controls >
        Your browser does not support the video tag.
      </video> 

  </div>
</template>

<script>

export default {
  name: 'Videos',
  props: {
    videoUrl: String
  },
  data() {
    return {
    }
  },
  methods: {

  },
}
</script>

<style scoped>

</style>
