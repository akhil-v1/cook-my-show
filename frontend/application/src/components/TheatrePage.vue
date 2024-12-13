<template>
  <div :class="['theatre-page', { 'dark-mode': darkMode }]">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="user-details">
        <p><strong>{{ username }}</strong></p>
        <p>Your role: {{ role }}</p>
      </div>
      <ul class="nav">
        <li v-if="isAdmin">
          <router-link to="/admin/dashboard" style="color:white; text-decoration: none;">Dashboard</router-link> |
          <button class="nav-btn" @click="logout">Logout</button>
        </li>
        <li v-else>
          <router-link :to="'/' + this.role + '/' + this.username + '/dashboard'"
            style="color:white; text-decoration: none;">Dashboard</router-link> |
          <button class="nav-btn" @click="logout">Logout</button>
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
      <h2>Theatre Details</h2>

      <div v-if="theatre" class="theatre-details">
        <div class="field">
          <label>Name:</label>
          <input v-model="theatre.name" :disabled="!isAdmin" placeholder="Enter Theatre name" />
        </div>
        <div class="field">
          <label>Address:</label>
          <input v-model="theatre.address" :disabled="!isAdmin" />
        </div>
        <div class="field">
          <label>Capacity:</label>
          <input v-model="theatre.capacity" :disabled="!isAdmin" type="number" />
        </div>
        <div class="field">
          <label>Manager
            <select v-model="theatre.manager" :disabled="!isAdmin">
              <option v-for="manager in manager_list" :key="manager.id" :value="manager.id">{{
                manager.username }}
              </option>
            </select>
          </label>
        </div>
        <div class="field">
          <label>Shows:</label>
          <ul>
            <li v-for="show in theatre.shows" :key="show.id">{{ show.title }}</li>
          </ul>
        </div>
        <div v-if="isAdmin" class="btn-container">
          <button class="btn" @click="submit">Submit</button>
          <button class="btn btn-cancel" @click="cancel">Cancel</button>
          <button class="btn" @click="remove">Remove</button>
        </div>
      </div>
      <div v-else>
        Loading...
      </div>
    </main>
  </div>
</template>

<script>
const baseURL = "http://127.0.0.1:5000"
export default {
  name: "TheatrePage",
  data() {
    return {
      username: "", // Replace this with the actual username
      role: "", // Replace this with the actual user's role (admin, manager, or customer)
      auth_token: "",
      theatre: null,
      manager_list: [],
      theatre_id: "",
      darkMode: false,
      isEditable: false,
      error_txt: "",
      success_msg: "",
    };
  },
  async created() {
    this.username = sessionStorage.getItem("username");
    this.auth_token = sessionStorage.getItem("authentication-token");
    this.role = sessionStorage.getItem("role");
    this.theatre_id = this.$route.path.split("/")[2];

    const firstRequestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json;charset=utf-8",
        "Authentication-Token": this.auth_token,
      }
    };
    console.log(firstRequestOptions);
    await fetch(`${baseURL}/theatre/${this.theatre_id}`, firstRequestOptions)
      .then(async (response) => {
        if (!response.ok) {
          throw Error(response.statusText);
        }
        const myResp = await response.json();
        console.log(myResp);
        if (myResp) {
          if (myResp.resp === "ok") {
            this.theatre = myResp.stuff.theatre_data;
            this.manager_list = myResp.stuff.manager_list;
            this.success_msg = myResp.msg;
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
      });

  },
  computed: {
    isAdmin() {
      return this.role === "admin";
    },
  },
  methods: {
    logout() {
      // Implement your logout functionality here
    },
    async submit() {
      // Implement the submit functionality here
      // Save the changes made to the theatre details
      const requestBody = {
        name: this.theatre.name,
        address: this.theatre.address,
        capacity: this.theatre.capacity,
        manager: this.theatre.manager
      };

      const updateTheatreRequestOptions = {
        method: "POST",
        headers: {
          "Content-Type": "application/json;charset=utf-8",
          "Authentication-Token": this.auth_token,
        },
        body: JSON.stringify(requestBody),
      };

      await fetch(`${baseURL}/theatre/${this.theatre_id}`, updateTheatreRequestOptions)
        .then(async (response) => {
          if (!response.ok) {
            throw Error(response.statusText);
          }
          const myResp = await response.json();
          if (myResp) {
            if (myResp.resp == "ok") {
              this.success_msg = myResp.msg;
              this.$router.push({ path: `/admin/dashboard` });
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
      // Reset the changes made to the theatre details
      // this.isEditable = false;
      this.$router.push({ path: `/admin/dashboard` });
    },
    async remove() {
      const removeRequestOptions = {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json;charset=utf-8",
          "Authentication-Token": this.auth_token,
        }
      };

      await fetch(`${baseURL}/theatre/${this.theatre_id}`, removeRequestOptions)
        .then(async (response) => {
          if (!response.ok) {
            throw Error(response.statusText);
          }
          const myResp = await response.json();
          if (myResp) {
            if (myResp.resp == "ok") {
              this.$router.push({ path: `/admin/dashboard` });
              this.success_msg = myResp.msg;
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
        });
    },
    toggleDarkMode() {
      this.darkMode = !this.darkMode;
    },
  },
};
</script>

<style lang="stylus" scoped>
/* Add your custom styles here */

.theatre-page {
  display: flex;
  height:100%;
}

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
      margin: 5px 0;
      color: white;
      font-size: medium;
    }
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

.main-content {
  flex: 1;
  padding: 20px;

  h2 {
    text-align: left;
  }

  .theatre-details {
    .field {
      display: flex;
      align-items: center;
      margin-bottom: 10px;

      label {
        width: 100px;
        margin-right: 10px;
        text-align: left;
      }

      input,
      ul {
        flex: 1;
        padding: 5px;
        border: 1px solid #ccc;
        border-radius: 5px;
        font-size: 16px;
        text-align: left;
      }

      ul {
        margin: 0;
        padding-left: 20px;

        li {
          margin: 10px;
        }
      }
    }

    .btn-container {
      margin-top: 20px;

      .btn {
        background-color: #007bff;
        color: #fff;
        border: none;
        padding: 10px 20px;
        cursor: pointer;
        border-radius: 5px;
        font-size: 16px;
        margin-right: 10px;

        &.btn-cancel {
          background-color: #dc3545;
        }
      }
    }
  }
}

.dark-mode {

  .theatre-page {
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

    .theatre-details {
      input {
        background-color: #444;
        color: #fff;
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
