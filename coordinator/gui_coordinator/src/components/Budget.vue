<template>
  <div class="hello">
    <h1>{{ msg }}</h1>

  <div class="flex-container">
    <div class="flex-child-spend">
      <h2>KL Spending</h2>
      <h1>{{getSpending}}</h1>
    </div>
    <div class="flex-child-spend ">
      <h2>Mitch Spending</h2>
      <h1>{{getSpending}}</h1>
    </div>
  </div>

    <div class="flex-container">
      <div class="flex-child magenta">
       <div class="flex-container">
        <form>
          <h2>Income - ${{totalIncome}}</h2>
          <table>
           <thead>
            <tr>
             <th>Name</th>
             <th>Cost</th>
             <th>Details</th>
            </tr>
           </thead>
             <tbody id="wages">
              <tr v-for="wage in state.wage" :key="wage.name">
               <td ><div style="flex: 1;"><input type="" name="Name" v-model="wage.name"></div></td>
               <td ><div style="flex: 1;"><input type="" name="Name" v-model="wage.cost"></div></td>
               <td ><div style="flex: 1;"><input type="" name="Name" v-model="wage.details"></div></td>
              </tr>
             </tbody>
          </table>
        </form>
       </div>
      </div>

      <div class="flex-child yellow">
       <div class="flex-container">
        <form>
        <h2>Bills - ${{totalBill}}</h2>
        <table>
         <thead>
          <tr>
           <th>Bill</th>
           <th>Cost</th>
           <th>Details</th>
          </tr>
         </thead>
         <tbody id="bills">
          <tr v-for="bill in state.bills" :key="bill.name">
           <td ><div style="flex: 1;"><input type="" name="Name" v-model="bill.name"></div></td>
           <td ><div style="flex: 1;"><input type="" name="Name" v-model="bill.cost"></div></td>
           <td ><div style="flex: 1;"><input type="" name="Name" v-model="bill.details"></div></td>
          </tr>
         </tbody>
        </table>
        </form>
      </div>
     </div>

      <div class="flex-child green">
       <div class="flex-container">
        <form>
        <h2>Savings - ${{totalSavings}}</h2>
        <table>
         <thead>
          <tr>
           <th>Savings</th>
           <th>Cost</th>
           <th>Details</th>
          </tr>
         </thead>
         <tbody id="savings">
          <tr v-for="saving in state.saving" :key="saving.name">
           <td ><div style="flex: 1;"><input type="" name="Name" v-model="saving.name"></div></td>
           <td ><div style="flex: 1;"><input type="" name="Name" v-model="saving.cost"></div></td>
           <td ><div style="flex: 1;"><input type="" name="Name" v-model="saving.details"></div></td>
          </tr>
         </tbody>
        </table>
        </form>
       </div>
      </div>


    </div>
    <button v-on:click="post" style="margin-top: 20px; width: 75%; height: 50px;">Save</button>

  </div>
</template>

<script>
import { reactive, onMounted } from "vue";

export default {
  name: 'Budget',

  props: {
    msg: String
  },

  setup() {
    const state = reactive({
      bills: null,
      saving: null,
      wage: null
    });

    var path = ""
    if (process.env.NODE_ENV == 'development'){
      path = 'http://127.0.0.1:8000/budget'
    }else{
      path = window.location.toString();
    }

    onMounted(async () => {
        fetch(path+'/get_bills')
        .then((response) => {
          if (response.ok) {
            return response.json();
          }
        })
        .then((data) => {
          state.bills = data;
        });

        const savings_response = await fetch(path+'/get_savings');
        state.saving = await savings_response.json();

        const wages_response = await fetch(path+'/get_wages');
        state.wage = await wages_response.json();
      });

    return {
      path,
      state
    };
  },
  data(){
    return{
    }
  },
  created () {
  },
  mounted () {
  },

  computed: {
    totalBill() {
      var spendings = 0
      for (const id in this.state.bills){
        spendings += parseInt(this.state.bills[id].cost)
      }
      return spendings
    },
    totalIncome() {
      var income = 0
      for (const id in this.state.wage){
        income += parseInt(this.state.wage[id].cost)
      }
      return income
    },
    totalSavings() {
      var savings = 0
      for (const id in this.state.saving){
        savings += parseInt(this.state.saving[id].cost)
      }
      return savings
    },
    getSpending() {
      var spendings = (this.totalIncome - this.totalBill - this.totalSavings)
      return spendings / 2
    },
  },

  methods:{
    post() {
      (async () => {
      const rawResponse = await fetch(this.path+'/save', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        mode: 'no-cors',
        body: JSON.stringify(this.state)
      })
      const content = await rawResponse.json();
      console.log(content);
      })();
    },
  },
}
</script>

<style scoped>

.flex-container {
  display: flex;
  justify-content: space-around;
}

.flex-child-spend {
  background-color: #b8fcbb;
  flex-grow: 1;
  border: 2px solid grey;
  margin: 5px;
  margin-top: 50px;
  margin-bottom: 80px;
  padding-bottom: 10px;
}

.flex-child {
  background-color: #e6dfcc;
  flex-grow: 1;
  border: 2px solid grey;
  margin: 2px;
}

input {
  width: 90%;
}

h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
