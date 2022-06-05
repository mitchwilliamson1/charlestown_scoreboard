<template>
  <div class="home">

<h2>Login Form</h2>

    <form v-if="!form.show" @submit.prevent="submit">
      <div class="container">
<!--         <label for="uname"><b>Username</b></label>
        <input type="text" placeholder="Enter Username" name="uname" required > -->

        <label for="psw"><b>Password</b></label>
        <input type="password" placeholder="Enter Password" v-model="pass" name="psw" required>
            
        <button type="submit">Submit</button>
      </div>
    </form>

    <Budget v-if="form.show" msg="Welcome to the Budget App"/>

  </div>
</template>

<script>
// @ is an alias to /src
import Budget from '../components/Budget.vue'

export default {
  name: 'BudgetView',
  components: {
    Budget
  },
  data() {
    return {
      form: {
        pass: null,
        show: false,
        user: null,
      }
    }
  },
  methods: {
    async submit() {

      var path = ""
        if (process.env.NODE_ENV == 'development'){
          path = 'http://127.0.0.1:3000/budget'
        }else{
          path = window.location.toString();
        }

      fetch(path+'/', {
        method:'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        // mode: 'no-cors',
        body: JSON.stringify({"pass":this.pass})
      })
      .then(res => res.json())
      .then(res => {
         console.log("Correct Password: ", res.pass);
         this.form.show = res.pass
      })
      .catch(e => {
        console.error(JSON.stringify(e.message));
      });

    }
  }
}
</script>
<style type="text/css" scoped>
body {font-family: Arial, Helvetica, sans-serif;}
form {border: 3px solid #f1f1f1;}

input[type=text], input[type=password] {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  display: inline-block;
  border: 1px solid #ccc;
  box-sizing: border-box;
}

button {
  background-color: #04AA6D;
  color: white;
  padding: 14px 20px;
  margin: 8px 0;
  border: none;
  cursor: pointer;
  width: 100%;
}

button:hover {
  opacity: 0.8;
}

.cancelbtn {
  width: auto;
  padding: 10px 18px;
  background-color: #f44336;
}

.imgcontainer {
  text-align: center;
  margin: 24px 0 12px 0;
}

img.avatar {
  width: 40%;
  border-radius: 50%;
}

.container {
  padding: 16px;
}

span.psw {
  float: right;
  padding-top: 16px;
}


/* Change styles for span and cancel button on extra small screens */
@media screen and (max-width: 300px) {
  span.psw {
     display: block;
     float: none;
  }
  .cancelbtn {
     width: 100%;
  }
}
</style>