<template>
    <div :class="['admin-dashboard', { 'dark-mode': darkMode }]">
        <!-- Sidebar -->
        <aside class="sidebar">
            <div class="logo">
                <img src="./../assets/logo.png" />
            </div>
            <ul class="nav">
                <!-- Add other navigation links here as needed -->
                <li v-if="role === 'admin'">
                    <router-link to="/theatre/0"><button class="nav-btn">Add Theatre</button></router-link> |
                    <button class="nav-btn" @click="logoutUser">Logout</button>
                </li>
                <li v-if="role === 'manager'">
                    <button class="nav-btn" @click="addShow">Add Show</button> |
                    <button class="nav-btn" @click="logoutUser">Logout</button>
                </li>
                <li>
                    <button class="nav-btn" @click="toggleDarkMode">
                        {{ darkMode ? "Light Mode" : "Dark Mode" }}
                    </button>
                </li>
            </ul>
        </aside>

        <!-- Main content -->
        <main class="main-content">
            <h2 class="section-title">Hi {{ username }}, welcome to your CookMyShow dashboard</h2>
            <div class="container">
                <p id="error_txt" class="alert alert-danger" role="alert" v-if="error_txt">{{ error_txt }}</p>
                <p id="success_msg" class="alert alert-success" role="alert" v-if="success_msg">{{ success_msg }}</p>
            </div>
            <h3 class="section-subtitle">Unmanaged Theatres</h3>
            <div class="theatres-list">
                <ul>
                    <!-- List of unmanaged theatres -->
                    <li v-for="theatre in unmanagedTheatres" :key="theatre.id">
                        {{ theatre.name }} ({{ theatre.capacity }})
                        <span class="theatre-details">{{ theatre.address }}</span>
                        <ul>
                            <!-- Shows hosted in each managed theatre -->
                            <li v-for="show in theatreShows[theatre.id]" :key="show.id">
                                {{ show.name }} - {{ show.time }}
                            </li>
                        </ul>
                    </li>
                </ul>
            </div>

            <h3 class="section-subtitle">Managed Theatres</h3>
            <div class="theatres-list">
                <ul>
                    <!-- List of managed theatres -->
                    <li v-for="theatre in managedTheatres" :key="theatre.id">
                        {{ theatre.name }} ({{ theatre.capacity }})
                        <span class="thatre-details">{{ theatre.address }}</span>
                        <ul>
                            <!-- Shows hosted in each managed theatre -->
                            <li v-for="show in theatreShows[theatre.id]" :key="show.id">
                                {{ show.name }} - {{ show.time }}
                            </li>
                        </ul>
                    </li>
                </ul>
            </div>
        </main>
    </div>
</template>
  
<script>
const baseURL = "http://127.0.0.1:5000"
export default {
    name: "AdminDashboardPage",
    data() {
        return {
            role: "", // Replace this with the actual user's role
            username: "", // Replace this with the actual username
            auth_token: "",
            unmanagedTheatres: [],
            mangedTheatres: [],
            theatreShows: [],
            error_txt: "",
            success_msg: "",
            darkMode: false,
        };
    },

    async created() {
        this.auth_token = sessionStorage.getItem("authentication-token");
        this.username = sessionStorage.getItem("username");
        this.role = sessionStorage.getItem("role");

        const requestOptions = {
            methods: "GET",
            headers: {
                "Content-Type": "application/json;charset=utf-8",
                "Authentication-Token": `${this.auth_token}`,
            }
        };

        try {

            await fetch(`${baseURL}/admin/dashboard`, requestOptions)
                .then(async (response) => {
                    if (!response.ok) {
                        throw Error(response.statusText);
                    }
                    const myResp = await response.json();
                    if (myResp) {
                        if (myResp.resp == "ok") {
                            this.success_msg = myResp.msg;
                            this.unmanagedTheatres = myResp.stuff.theatres;
                            this.theatreShows = myResp.stuff.theatreShows;
                            console.log("Finished");
                        } else {
                            throw Error(myResp.msg);
                        }
                    } else {
                        throw Error("Invalid data received.");
                    }
                })
                .catch((error) => {
                    throw Error(error);
                })

        } catch (error) {
            this.logoutUser();
            this.error_txt = error;
            console.log("Failed to load Dashboard. Error: ", error);
        }
    },
    methods: {
        // async addTheatre() {
        //     // Implement add theatre functionality for admin role here
        //     const requestOptions = {
        //         method: "POST",
        //         headers: {
        //             "Content-Type": "application/json;charset=utf-8",
        //             "Authentication-Token": this.auth_token,
        //         }
        //     };

        //     await fetch(`${baseURL}/theatre/0`, requestOptions)
        //         .then(async (response) => {
        //             if (!response.ok) {
        //                 throw Error(response.statusText);
        //             }
        //             const myResp = await respnse.json();
        //             if (myResp) {
        //                 if (myResp.resp == "ok") {
        //                     this.$router.push({ path: `/theatre/0`, params: { theatre_id: 0 } })
        //                     this.success_msg = myResp.msg;
        //                 } else {
        //                     throw Error(myresp.msg);
        //                 }
        //             } else {
        //                 throw Error("Invalid data received.");
        //             }
        //         })
        //         .catch((error) => {
        //             this.error_txt = error;
        //             console.log("Request failed. Error: ", error);
        //         })

        // },
        addShow() {
            // Implement add show functionality for manager role here
        },
        toggleDarkMode() {
            this.darkMode = !this.darkMode;
        },
        async logoutUser() {
            // Implement your logout functionality here
            const logoutRequestOptions = {
                method: "POST",
                headers: {
                    "Content-Type": "application/json;charset=utf-8",
                    "Authentication-Token": this.auth_token
                },
            };

            await fetch(`${baseURL}/logout_page`, logoutRequestOptions)
                .then(async (response) => {
                    if (!response.ok) {
                        throw Error(response.statusText);
                    }
                    const myResp = await response.json();
                    if (myResp) {
                        if (myResp.resp == "ok") {
                            this.success_msg = myResp.msg;
                            this.logoutAuth(logoutRequestOptions);
                            sessionStorage.clear();
                            console.log("Logging out");
                            this.$router.push({ path: `/login_page` })
                        } else {
                            throw Error(myResp.msg);
                        }
                    } else {
                        throw Error("Something went wrong. Invalid data received.");
                    }
                })
                .catch((error) => {
                    this.error_txt = error;
                    console.log("Logout failed. Error: ", error);
                })

        },
        async logoutAuth(reqoptions) {
            await fetch(`${baseURL}/logout`, reqoptions)
                .then(async (response) => {
                    if (!response.ok) {
                        throw Error(response.statusText);
                    }
                    const myResp = await response.json();
                    console.log("Logging out auth");
                })
                .catch((error) => {
                    this.error_txt = error;
                    console.log("Logout failed. Error: ", error);
                })
        },
    },
};
</script>
  
<style lang="stylus" scoped>
  /* Dashboard styles */
  .admin-dashboard {
    display: flex;
    background-color: #f5f5f5;
    color: #333; /* Default text color */
  }
  
  .dark-mode {
    background-color: #000;
    color: #fff; /* Bright text color for dark background */
    
    .main-content{
        background-color: #000;
        .section-title {
            color: #00ff00;
        }
    
        .section-subtitle{
            color: yellow;
        }
    
        .theatres-list{
            ul{
                li{
                    color: white;
                    ul{
                        li{
                           color: white; 
                        }
                    }
                }
            }
        }
    }

    }
  
  /* Sidebar styles */
  .sidebar {
    width: 300px;
    padding: 20px;
    background-color: #333;
    color: #fff;
    heihgt: 100%;
  
    .logo {
      /* Add logo styles here */
      margin-bottom: 20px;
    }
  
    .nav {
      list-style: none;
      padding: 0;
  
      .nav-btn {
        background-color: transparent;
        color: #fff;
        border: none;
        cursor: pointer;
        font-size: 16px;
        margin-bottom: 10px;
  
        &:hover {
          text-decoration: underline;
        }
      }
    }
  }
  
  /* Main content styles */
  .main-content {
    flex: 1;
    height: 100%;
    padding: 20px;
  
    .section-title {
      font-size: 24px;
      margin-bottom: 10px;
      text-align: left; /* Align the title to the left */
    }
  
    .section-subtitle {
      font-size: 20px;
      margin-bottom: 10px;
      color: #007bff;
      text-align: left; /* Align the subtitle to the left */
    }
  
    .theatres-list {
      ul {
        list-style: none;
        padding: 0;
        margin: 0;
        text-align: left; /* Align the list items to the left */
  
        li {
          font-size: 18px;
          margin-bottom: 5px;
          padding-left: 10px;
  
          ul {
            list-style: none;
            margin-top: 5px;
            padding-left: 20px;
  
            li {
              font-size: 16px;
            }
          }
        }
      }
    }
  }
  </style>
  