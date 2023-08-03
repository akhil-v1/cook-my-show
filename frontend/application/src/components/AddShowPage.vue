<template>
  <div :class="['shows-page', { 'dark-mode': darkMode }]">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="user-details">
        <p><strong>{{ username }}</strong></p>
        <p>Your role: {{ role }}</p>
      </div>
      <ul class="nav">
        <li>
          <router-link :to="'/manager/' + this.username + '/dashboard'"
            style="color:white;text-decoration: none;">Dashboard</router-link> |
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
      <h2>{{ isEditable ? 'Create New Show' : 'Update Show' }}</h2>
      <div class="show-details">
        <div class="field">
          <label>Title:</label>
          <input v-model="shows.title" :disabled="!isManager" />
        </div>
        <div class="field">
          <label>Duration:</label>
          <input v-model="shows.duration" :disabled="!isManager" type="text" />
        </div>
        <div class="field">
          <label>Tags:</label>
          <input v-model="shows.tags" :disabled="!isManager" type="text" />
        </div>
        <div class="field" v-if="isManager">
          <label>Theatres:</label>
          <ul>
            <li v-for="(theatre, idx) in managedTheatres" :key="theatre.id">
              <input type="checkbox" v-model="theatre.selected" />
              {{ theatre.name }}
              <div v-if="theatre.selected">
                <label>Price:</label>
                <input v-model="theatre.price" :disabled="!isManager" type="number" step="0.01" />
                <label>Time:</label>
                <input v-model="theatre.time" :disabled="!isManager" type="datetime-local" />
                <label>Available Seats:</label>
                <input v-model="theatre.seats" :disabled="!isManager" type="number" />
              </div>
              <!-- <input type="checkbox" v-model="shows.theatre.id" :value="theatre.id" /> {{ theatre.name }}
              <label>Price:</label>
              <input v-model="shows.theatre.price" :disabled="!isManager" type="number" step="0.01" />
              <label>Time:</label>
              <input v-model="shows.theatre.time" :disabled="!isManager" type="time" />
              <label>Available Seats:</label>
              <input v-model="shows.theatre.seats" :disabled="!isManager" type="number" /> -->
            </li>
          </ul>
        </div>
        <div v-if="isManager" class="btn-container">
          <button class="btn" @click="submit">Submit</button>
          <button class="btn btn-cancel" @click="cancel">Cancel</button>
        </div>
      </div>
    </main>
  </div>
</template>
  
<script>
const baseURL = "http://127.0.0.1:5000"
export default {
  name: "ShowPage",
  data() {
    return {
      username: "", // Replace this with the actual username
      role: "", // Replace this with the actual user's role (admin, manager, or customer)
      auth_token: "",
      shows: {
        title: "",
        duration: 0,
        tags: "",
      },
      managedTheatres: [],
      isEditable: true,
      darkMode: false,
      error_txt: "",
      success_msg: "",
    };
  },
  computed: {
    isManager() {
      return this.role === "manager";
    },
  },
  async created() {
    this.role = sessionStorage.getItem("role");
    this.username = sessionStorage.getItem("username");
    this.auth_token = sessionStorage.getItem("authentication-token");
    const firstRequestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json;charset=utf-8",
        "Authentication-Token": this.auth_token,
      }
    };

    await fetch(`${baseURL}/manager/${this.username}/show/add_new`, firstRequestOptions)
      .then(async (response) => {
        if (!response.ok) {
          throw Error(response.statusText);
        }
        const myResp = await response.json();
        if (myResp) {
          if (myResp.resp == "ok") {
            this.managedTheatres = myResp.stuff;
            this.success_msg = myResp.msg;

            this.managedTheatres.forEach((theatre) => {
              theatre.selected = false;
              theatre.price = "";
              theatre.time = "";
              theatre.seats = "";
            });
          } else {
            throw Error(myResp.msg);
          }
        } else {
          throw Error("Invalid data received");
        }
      })
      .catch((error) => {
        this.error_txt = error;
        console.log("Request failed. Error: ", error);
      })
  },
  watch: {
    theatre() {
      theatre.selected = !theatre.selected;
    }
  },
  methods: {
    // toggleTheatre(theatre) {
    //   theatre.selected = !theatre.selected;
    // },
    async submit() {
      // Implement the submit functionality here
      // Save the changes made to the show details
      // this.isEditable = false;
      const selectedTheatres = this.managedTheatres.filter((theatre) => theatre.selected);
      const requestBody = {
        title: this.shows.title,
        duration: this.shows.duration,
        tags: this.shows.tags,
        theatres: selectedTheatres.map((theatre) => {
          return {
            id: theatre.id,
            price: theatre.price,
            time: new Date(theatre.time),
            seats: theatre.seats,
          };
        }),
      };

      const addShowRequestOptions = {
        method: "POST",
        headers: {
          "Content-Type": "application/json;charset=utf-8",
          "Authentication-Token": this.auth_token,
        },
        body: JSON.stringify(requestBody),
      };

      await fetch(`${baseURL}/manager/${this.username}/show/add_new`, addShowRequestOptions)
        .then(async (response) => {
          if (!response.ok) {
            throw Error(response.statusText);
          }
          const myResp = await response.json();
          if (myResp) {
            if (myResp.resp == "ok") {
              this.success_msg = myResp.msg;
              this.$router.push({ path: `/manager/${this.username}/dashboard` });
            } else {
              throw Error(myResp.msg);
            }
          } else {
            throw Error("Invalid data received.");
          }
        })
        .catch((error) => {
          this.error_txt = error;
          console.log("Request failed. Error: ", error);
        })
    },
    cancel() {
      // Implement the cancel functionality here
      // Reset the changes made to the show details
      this.$router.push({ path: `/manager/${this.username}/dashboard` });
      // this.isEditable = false;
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
.shows-page{
    display: flex;
    height: 100%;
}
  /* Sidebar styles */
  .sidebar {
    width: 250px;
    padding: 20px;
    background-color: #333;
    color: #fff;
    display: flex;
    flex-direction: column;
  
    .user-details {
  
      strong {
        font-size: xx-large;
        color: yellow;
      }
  
      p {
        font-size: medium;
        margin: 5px 0;
        color: white;
      }
    }
  
    .nav {
      list-style: none;
      padding: 0;
  

  
      a,
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
    flex:1;
    padding: 20px;
  
    h2 {
      text-align: left;
    }
  
    .show-details {
      .field {
        display: flex;
        align-items: center;
        margin-bottom: 10px;
  
        label {
          width: 100px;
          text-align: left;
          margin-right: 10px;
        }
  
        input {
          width: 100%;
          padding: 10px;
          font-size: 16px;
          border: 1px solid #ccc;
          border-radius: 5px;
          background-color: #fff;
        }
      }
  
      .rating-stars {
        font-size: 24px;
        span {
          cursor: pointer;
          margin-right: 5px;
        }
  
        .rated {
          color: #ffc107;
        }
      }
  
      ul {
        list-style: none;
        margin-top: 10px;
        padding-left: 20px;
  
        li {
          font-size: 16px;
          margin-bottom: 5px;
  
          input {
            margin-right: 5px;
          }
        }
      }
    }
  
    .btn-container {
      margin-top: 20px;
  
      .btn {
        background-color: #007bff;
        color: #fff;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
        margin-right: 10px;
  
        &:hover {
          background-color: #0056b3;
        }
      }
  
      .btn-cancel {
        background-color: #ccc;
        &:hover {
          background-color: #999;
        }
      }
    }
  }
  
  /* Dark mode styles */
  .dark-mode {

    .shows-page {
        background-color: #333;
        color: #f5f5f5; /* Bright text color for dark background */
      }
  
    .sidebar {
      background-color: #222;
    }
  
    .main-content {

        h2 {
            color: #00ff00;
          }
  
      .show-details {
        input {
          background-color: #444;
          color: #f5f5f5;
        }
      }
  
      .btn-container {
        .btn,
        .btn-cancel {
          background-color: #007bff;
        }
        .btn-cancel {
          background-color: #ccc;
          &:hover {
            background-color: #999;
          }
        }
      }
    }
  }
  </style>
  
  