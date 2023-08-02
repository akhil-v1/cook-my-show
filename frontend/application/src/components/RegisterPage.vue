<template>
  <div class="register">
    <nav style="text-align: left;">
      <router-link to="/"><button style="margin-right: 16px; font-size: medium;"
          class="btn btn-lg"><strong>Home</strong></button></router-link> |
      <router-link to="/About"><button style="margin-right: 16px; font-size: medium;"
          class="btn btn-lg"><strong>About</strong></button></router-link> |
      <router-link to="/login_page"><button style="margin-right: 16px; font-size: medium;"
          class="btn btn-lg"><strong>Login</strong></button></router-link>
    </nav>
    <p id="error_txt" class="alert alert-danger" role="alert" v-if="error_txt">{{ error_txt }}</p>
    <p id="success_msg" class="alert alert-success" role="alert" v-if="success_msg">{{ success_msg }}</p>

    <body class="container">
      <form @submit.prevent="registerUser">
        <h3 class="form text-center mt-2 mb-4"><strong>Create new account</strong></h3>
        <div class="form-group">
          <label>Username
            <input id="username" type="text" v-model="username" class="form-control form-control-lg"
              placeholder="Username" required autocomplete="off" />
          </label>
        </div>
        <div class="form-group">
          <label>Email address
            <input id="email" type="email" v-model="email" class="form-control form-control-lg" placeholder="Email"
              required autocomplete="off" />
          </label>
        </div>
        <div class="form-group">
          <label>Password
            <input id="password" type="password" v-model="password" class="form-control form-control-lg"
              placeholder="Password" required autocomplete="off" />
          </label>
        </div>
        <div class="form-group">
          <label>Password Confirm
            <input id="password_confirm" type="password" v-model="password_confirm" class="form-control form-control-lg"
              placeholder="Confirm Password" required autocomplete="off" />
          </label>
        </div>
        <div class="form-group">
          <label>Role
            <select v-model="role" class="form-control form-control-lg" required>
              <option value="" disabled selected> Select your role</option>
              <option id="manager_drop_down" value="manager">Manager</option>
              <option id="customer_drop_down" value="customer">Customer</option>
            </select>
          </label>
        </div>
        <button id="submit" class="btn btn-dark btn-lg btn-block">Sign Up</button>
      </form>
    </body>
  </div>
</template>

<script>
const baseURL = "http://127.0.0.1:5000"
export default {
  name: "RegisterPage",
  data() {
    return {
      username: "",
      email: "",
      password: "",
      password_confirm: "",
      role: "",
      error_txt: "",
      success_msg: "",
    };
  },
  beforeMount() {
    sessionStorage.clear();
  },
  methods: {
    async registerUser() {

      const requestBody = {
        username: this.username,
        email: this.email,
        password: this.password,
        role: this.role
      };

      const requestOptions = {
        method: "POST",
        headers: {
          "Content-Type": "application/json;charset=utf-8",
        },
        body: JSON.stringify(requestBody),
      };

      try {

        if (this.password == this.password_confirm) {
          await fetch(`${baseURL}/register_page`, requestOptions)
            .then(async (response) => {
              if (!response.ok) {
                throw Error(response.statusText)
              }
              const myResp = await response.json();
              if (myResp) {
                if (myResp.resp == "ok") {
                  this.success_msg = myResp.msg;
                  this.$router.go();
                } else {
                  throw Error(myResp.msg);
                }
              } else {
                throw Error("Something went wrong. Invalid data received.");
              }
            })
            .catch((error) => {
              this.error_txt = error;
              console.log("Registration failed. Error: ", error);
            });
        } else {
          throw Error("Passwords do not match.");
        }

      } catch (error) {
        this.error_txt = error;
        console.log("Registration failed. Error: ", error);
      }
    }
  },
  watch: {
    username(newValue, oldValue) {
      console.log(`Value changed from ${oldValue} to ${newValue}`)
    }
  }

};
</script>

<style lang="stylus" scoped>
.register {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.register nav {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
}

.register .btn {
  font-size: 16px;
  font-weight: bold;
  color: #007bff;
  background-color: transparent;
  border: none;
  cursor: pointer;
  margin-left: 10px;
}

.register .btn:hover {
  text-decoration: underline;
}

.register .form-group {
  margin-bottom: 20px;
}

.register .form-group label {
  display: block;
  font-weight: bold;
  color: #555;
  margin-bottom: 5px;
}

.register input,
.register select {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  transition: border-color 0.3s ease;
}

.register input:focus,
.register select:focus {
  border-color: #007bff;
  outline: none;
}

.register .alert {
  margin-top: 10px;
  font-size: 16px;
  color: #dc3545;
}

.register h3.form {
  text-align: center;
  margin-top: 10px;
  margin-bottom: 20px;
  color: #007bff;
}

.register #submit {
  width: 100%;
  font-size: 18px;
  padding: 12px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.register #submit:hover {
  background-color: #0056b3;
}

/* Additional global styles */

body {
  font-family: 'Helvetica Neue', sans-serif;
  background-color: #f9f9f9;
  color: #333;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

</style>
