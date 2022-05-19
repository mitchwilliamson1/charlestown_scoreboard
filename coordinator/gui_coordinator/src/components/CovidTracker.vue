<template>
  <div id="camera">
    <div>
      <video ref="video" id="video" width="100%" height="100%" autoplay/>
    </div>
    <div>
      <input type="file" accept="image/*" capture="camera" />
    </div>
    <canvas ref="canvas" id="canvas" width="100%" height="100%"/>>
  </div>
</template>
 Run code snippetHide resultsExpand snippet

<script>

export default {
  name: 'Camera',
  data() {
    return {
      video: {},
      canvas: {},
      captures: []
    }
  },
//   mounted() {
//     this.video = this.$refs.video;
//     if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
//         navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
//              video.srcObject = stream;
//                 video.play();
//                 video.onplay = function () {
//                 };
//                 this.video.play();
//         });
//     }
// },
//   methods: {
//     capture() {
//         this.canvas = this.$refs.canvas;
//         var context = this.canvas.getContext("2d").drawImage(this.video, 0, 0, 640, 480);
//         this.captures.push(canvas.toDataURL("image/webp"));
//     }
// }
}
</script>
 Run code snippetHide resultsExpand snippet





<style>
    #camera {
        text-align: center;
        color: #2c3e50;
    }
    #video {
        background-color: #000000;
    }
    #canvas {
        display: none;
    }
    li {
        display: inline;
        padding: 5px;
    }
</style>
 Run code snippetHide resultsExpand snippet