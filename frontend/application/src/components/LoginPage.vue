<template>
    <div class="login">
        <nav style="text-align: left;">

            <router-link to="/"><button style="margin-right: 16px; font-size: medium;"
                    class="btn btn-lg"><strong>Home</strong></button></router-link> |
            <router-link to="/about"><button style="margin-right: 16px; font-size: medium;"
                    class="btn btn-lg"><strong>About</strong></button></router-link> |
            <router-link to="/register_page"><button style="margin-right: 16px; font-size: medium;"
                    class="btn btn-lg"><strong>SignUp</strong></button></router-link>
        </nav>

        <body class="login_body_class">

            <body class="container">
                <br />
                <h3 class="form text-center mt-2 mb-4"><strong>Login</strong></h3>
                <div class="container">
                    <p id="error_txt" class="alert alert-danger" role="alert" v-if="error_txt">{{ error_txt }}</p>
                    <p id="success_msg" class="alert alert-success" role="alert" v-if="success_msg">{{ success_msg }}</p>
                </div>
                <form @submit.prevent="loginAuth">
                    <div class="form-group">
                        <label>Email
                            <input v-model="email" id="email" type="text" class="form-control form-control-lg" required />
                        </label>
                    </div>
                    <div class="form-group">
                        <label>Password
                            <input v-model="password" id="password" type="password" class="form-control form-control-lg"
                                required />
                        </label>
                    </div>
                    <div class="form-group">
                        <label>Role
                            <select v-model="role" class="form-control form-control-lg" required>
                                <option value="manager">Manager</option>
                                <option value="customer" selected>Customer</option>
                                <option value="admin" selected>Admin</option>
                            </select>
                        </label>
                    </div>
                    <button id="" class="btn btn-dark btn-lg btn-block">Log in</button>
                    <p>New User? <router-link to="/register">Create a new account now</router-link>
                    </p>
                </form>
            </body>
        </body>
    </div>
</template>

<script>
const baseURL = "http://127.0.0.1:5000";
export default {
    name: "LoginPage",
    data() {
        return {
            email: "",
            password: "",
            role: "",
            auth_token: "",
            is_auth: "",
            error_txt: "",
            success_msg: "",
        };
    },
    beforeMount() {
        sessionStorage.clear();
    },
    methods: {
        async loginAuth() {

            const requestBody = {
                email: this.email,
                password: this.password,
            };

            const authRequestOptions = {
                method: "POST",
                headers: {
                    "Content-Type": "application/json;charset=utf-8",
                },
                body: JSON.stringify(requestBody),
            };


            await fetch(`${baseURL}/login?include_auth_token`, authRequestOptions)
                .then(async (response) => {
                    if (!response.ok) {
                        throw Error(response.statusText);
                    }
                    const myResp = await response.json();
                    if (myResp) {
                        this.auth_token = myResp.response.user.authentication_token;
                        sessionStorage.setItem("authentication-token", this.auth_token);
                        sessionStorage.setItem("email", this.email);
                        this.loginUser();
                    } else {
                        throw Error("Authentication failed. Data not received.");
                    }
                }).catch((error) => {
                    this.error_txt = error;
                    console.log("Login failed. Error: ", error);
                })
        },

        async loginUser() {

            const requestBody = {
                email: this.email,
                password: this.password,
                role: this.role,
            };

            const requestOptions = {
                method: "POST",
                headers: {
                    "Content-Type": "application/json;charset=utf-8",
                    "Authentication-Token": this.auth_token,
                },
                body: JSON.stringify(requestBody),
            };

            try {
                if (this.auth_token) {
                    await fetch(`${baseURL}/login_page`, requestOptions)
                        .then(async (response) => {
                            if (!response.ok) {
                                throw Error(response.statusText);
                            }
                            const myResp = await response.json();
                            if (myResp) {
                                if (myResp.resp == "not ok") {
                                    throw Error(myResp.msg);
                                } else if (myResp.resp == "ok") {
                                    // console.log("Well and good");
                                    const user_data = myResp.stuff;
                                    console.log(user_data);
                                    sessionStorage.setItem("username", user_data["username"]);
                                    sessionStorage.setItem("role", user_data["role"]);
                                    if (user_data["role"] == "customer") {
                                        this.$router.push({ path: `/user/dashboard` });
                                    } else if (user_data["role"] == "admin") {
                                        this.$router.push({ path: `/admin/dashboard` });
                                    } else {
                                        this.$router.push({ path: `/manager/${user_data["username"]}/dashboard` });
                                    }
                                    this.success_msg = myResp.msg;
                                } else {
                                    throw Error(myResp.msg);
                                }
                            } else {
                                throw Error("something went wrong (data not received)");
                            }
                        })
                        .catch((error) => {
                            this.error_txt = error;
                            console.log("Login failed. Error: ", error);
                        });
                } else {
                    this.$router.go();
                    // this.$router.push({ path: '/login_page' })
                    throw Error("authentication failed");
                }
            } catch (error) {
                this.error_txt = error;
                console.log("Log in failed. Error: ", error);
            }
        }

    }
}
</script>

<style lang="stylus" scoped>
.login
  max-width: 400px
  margin: 0 auto
  padding: 20px
  border-radius: 8px
  background-color: #fff
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1)

  nav
    display: flex
    justify-content: flex-end
    margin-bottom: 20px

    .btn
      font-size: 16px
      font-weight: bold
      color: #007bff
      background-color: transparent
      border: none
      cursor: pointer
      margin-left: 10px

      &:hover
        text-decoration: underline

  .form-group
    margin-bottom: 20px

    label
      display: block
      font-weight: bold
      color: #555
      margin-bottom: 5px

    input, select
      width: 100%
      padding: 12px
      font-size: 16px
      border: 1px solid #ccc
      border-radius: 4px
      transition: border-color 0.3s ease
      box-sizing: border-box // Add this line to prevent box-sizing issues

      &:focus
        border-color: #007bff
        outline: none

    .alert
      margin-top: 10px
      font-size: 16px
      color: #dc3545

  h3.form
    text-align: center
    margin-top: 10px
    margin-bottom: 20px
    color: #007bff

  #submit
    width: 100%
    font-size: 18px
    padding: 12px
    background-color: #007bff
    color: #fff
    border: none
    border-radius: 4px
    cursor: pointer
    transition: background-color 0.3s ease

    &:hover
      background-color: #0056b3

/* Additional global styles */

body
  font-family: 'Helvetica Neue', sans-serif
  background-color: #f9f9f9
  color: #333

.container
  max-width: 800px
  margin: 0 auto
  padding: 20px

</style>