import Vue from "vue";
import Router from "vue-router";

import Home from "./views/Home.vue";

import RegisterView from "./views/Register.vue";
import LoginView from "./views/Login.vue";
import AdminDashboardView from "./views/AdminDashboard.vue";
import TheatreView from "./views/Theatre.vue";
import ShowView from "./views/Show.vue";
import CustomerDashboardView from "./views/CustomerDashboard.vue";
import SearchView from "./views/Search.vue";
import CheckoutView from "./views/Checkout.vue";

Vue.use(Router);

export default new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/",
      name: "home",
      component: Home
    },
    {
      path: "/about",
      name: "about",
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () =>
        import(/* webpackChunkName: "about" */ "./views/About.vue")
    },
    {
      path: "/login_page",
      name: "login",
      component: LoginView
    },
    {
      path: "/register_page",
      name: "register",
      component: RegisterView
    },
    {
      path: "/admin/dashboard",
      name: "admin_dashboard",
      component: AdminDashboardView
    },
    {
      path: "/theatre/:id",
      name: "theatre",
      component: TheatreView
    },
    {
      path: "/show",
      name: "show",
      component: ShowView
    },
    {
      path: "/user/dashboard",
      name: "customer_dashboard",
      component: CustomerDashboardView
    },
    {
      path: "/search",
      name: "search",
      component: SearchView
    },
    {
      path: "/checkout",
      name: "checkout",
      component: CheckoutView
    }
  ]
});
