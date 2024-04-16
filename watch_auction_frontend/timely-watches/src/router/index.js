// Composables
import { createRouter, createWebHistory } from "vue-router";
import { useUserStore } from "@/store/userStore";

import Login from "@/views/Login.vue";
import Schedule from "@/views/Schedule.vue"
import AdminDefault from "@/layouts/admin/AdminDefault.vue";
import AdminLanding from "@/views/seller/AdminHome.vue"
import AdminSchedule from "@/views/seller/AdminSchedule.vue"
import CreateListing from "@/views/seller/CreateListing.vue";
import AdminAccount from "@/views/Account.vue"
import Listing from "@/views/seller/Listing.vue"
import AuctionList from "@/views/seller/ListOfAuctions.vue";
import HomeDefault from "@/layouts/default/Default.vue";
import AuctionHome from "@/views/AuctionHome.vue"
import Bids from "@/views/BidsView.vue";
import AuctionDetails from "@/views/AuctionDetails.vue";
import AccountUpdate from "@/views/Account.vue";
import Checkout from "@/views/Checkout.vue";
import Success from "@/views/Success.vue";
import Cancel from "@/views/Cancel.vue";

const routes = [
  {
    path: "",
    name: "Login",
    component: Login,
    meta: { requiresAuth: false },
  },
  {
    path: "/schedule/:id",
    name: "Schedule",
    component: Schedule,
    meta: { requiresAuth: true },
  },
  {
    path: "/admin",
    component: AdminDefault,
    redirect: "/admin/landing",
    children: [
      {
        path: "landing",
        name: "Landing",
        component: AdminLanding,
        meta: { requiresAuth: true },
      },
      {
        path: "adminschedule",
        name: "AdminSchedule",
        component: AdminSchedule,
        meta: { requiresAuth: true },
      },
      {
        path: "create",
        name: "Create",
        component: CreateListing,
        meta: { requiresAuth: true },
      },
      {
        path: "account",
        name: "AdminAccount",
        component: AdminAccount,
        meta: { requiresAuth: true },
      },
      {
        path: "listing",
        name: "Listing",
        component: Listing,
        meta: { requiresAuth: true },
      },
      {
        path: "auctionlist",
        name: "AuctionList",
        component: AuctionList,
        meta: { requiresAuth: true },
      },
    ],
  },

  {
    path: "/home",
    component: HomeDefault,
    children: [
      {
        path: "", // Empty path for the Home route
        name: "Home",
        component: AuctionHome,
        meta: { requiresAuth: true },
      },
      {
        path: "bids",
        name: "Bids",
        component: Bids,
        meta: { requiresAuth: true },
      },
      {
        path: ":id",
        name: "AuctionDetails",
        component: AuctionDetails,
        meta: {
          auth: true,
          requiresAuth: true,
        },
      },
      {
        path: "account", // Removed the leading slash
        name: "Account",
        component: AccountUpdate,
        meta: { requiresAuth: true },
      },
    ],
  },
  {
    path: "/checkout/:id",
    name: "Checkout",
    component: Checkout,
    meta: { requiresAuth: true },
  },
  {
    path: "/Success",
    name: "Success",
    component: Success, // Fixed the casing of the file name
    meta: { requiresAuth: true },
  },
  {
    path: "/Cancel",
    name: "Cancel",
    component: Cancel,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

// eslint-disable-next-line no-unused-vars
router.beforeEach((to, from, next) => {
  const userStore = useUserStore();
  if (
    to.matched.some((record) => record.meta.requiresAuth) &&
    !userStore.$state.isLoggedIn
  ) {
    next({
      path: "/",
      // save the location we were at to come back later
      query: { redirect: to.fullPath },
    });
  } else {
    // Continue navigation
    next();
  }
});

export default router;
