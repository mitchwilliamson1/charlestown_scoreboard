<template>
  <div class="home">
    <div class="row">

      <div class="col">
        <div class="bg-secondary p-3 text-white" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight" aria-controls="offcanvasRight">Create New Club</div>

      <div class="offcanvas offcanvas-end w-50" tabindex="-1" id="offcanvasRight" aria-labelledby="offcanvasRightLabel">
        <div class="offcanvas-header">
          <h5 id="offcanvasRightLabel">Create Sponsor</h5>
          <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">
          <div class="">
          <div class="row p-1">
            <div class="col-4">Name</div>
            <input class="col" v-model="createSponsor.name" type="text">
          </div>
          <div class="row p-1">
            <div class="col-4">Logo</div>
            <input type="file" ref="file" @change="onChange($event)" class="col">
          </div>
          </div>
          <div class="">
            <button type="button" @click="createSponsorButton(createSponsor)" data-bs-dismiss="offcanvas" class="btn btn-success">Create Sponsor</button>
          </div>
        </div>
      </div>

        <div class="row">
          <div v-if="state.sponsors" class="col-12">
            <h3 class="p-3">Current Sponsors</h3>
            <current-sponsors :sponsors="state.sponsors"/>
          </div>
        </div>
        
      </div>
    </div>
    
  </div>
</template>

<script>
import { reactive, onMounted, ref} from "vue";
import CurrentSponsors from '../components/CurrentSponsors.vue'
import axios from 'axios'
import { DateTime } from "luxon";

export default {
  name: 'SponsorsView',
  components: {
    CurrentSponsors,
  },
  data() {
    return {

    }
  },
  setup() {
    const state = reactive({
      players: null,
      sponsors: null,
    });

  const createSponsor = reactive({
        name:null,
        logo:null,
      });

    function onChange(event) {
      createSponsor.logo = event.target.files[0]
    }

    var path = ""
    path = 'http://127.0.0.1:8000/'
    
    onMounted(async () => { 
      getSponsors()
    });
    function createSponsorButton(sponsor) {
      let data = new FormData();
      data.append('file', sponsor.logo);
      data.append('sponsor', JSON.stringify(sponsor));

      axios.post(path+'games/create_sponsor',
      data,
      {headers: {
        'Content-Type': 'multipart/form-data'
        }
      })
      .then(function (response) {
        getClubs()
      })
      .catch(function (error) {
        console.log(error);
      });
    }
    function getSponsors() {
      axios.get(path+'games/get_sponsors')
      .then(function (response) {
        if (response.status == 200){
          console.log("RESPONSE ", response.data);
          state.sponsors = response.data
        }
      })
      .catch(function (error) {
        // handle error
        console.log("ERROR ", error);
      })
      .then(function () {
        // always executed
      });
    }

    return {
      path,
      state,
      createSponsor,
      createSponsorButton,
      onChange,
      
    };
  },
  methods: {

  }
}
</script>
<style type="text/css" scoped>

</style>