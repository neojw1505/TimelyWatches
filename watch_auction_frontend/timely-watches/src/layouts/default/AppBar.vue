<!-- eslint-disable no-mixed-spaces-and-tabs -->
<!-- eslint-disable no-multiple-template-root -->
<template>
  <div>
    <v-navigation-drawer v-model="drawer" temporary color="amber-lighten-4">
      <v-list-item
        prepend-avatar="https://randomuser.me/api/portraits/men/78.jpg"
        :title="getUserName()"
      ></v-list-item>

      <v-divider></v-divider>

      <v-list density="compact" nav>
        <router-link class="router-link" to="/home">
          <v-list-item
            prepend-icon="mdi-home"
            title="All Auctions"
            value="home"
            @click="removeWatchStore"
          >
          </v-list-item>
        </router-link>

        <router-link class="router-link" to="/home/bids">
          <v-list-item
            prepend-icon="mdi-cash-multiple"
            title="My Bids"
            value="bids"
            @click="removeWatchStore"
          ></v-list-item>
        </router-link>

        <router-link class="router-link" to="/home/account">
          <v-list-item
            prepend-icon="mdi-account"
            title="Account"
            value="account"
            @click="removeWatchStore"
          ></v-list-item>
        </router-link>

        <router-link class="router-link" to="/">
          <v-list-item
            prepend-icon="mdi-door"
            title="Logout"
            value="logout"
            @click="removeUserStore"
          ></v-list-item>
        </router-link>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar :elevation="2" :height="100" color="amber-lighten-5">
      <v-btn
        @click.stop="drawer = !drawer"
        density="compact"
        icon="mdi-menu"
      ></v-btn>
      <v-app-bar-title class="topbar">
        <h4 class="header">
          <svg-icon type="mdi" :path="path1"></svg-icon>
          Timely Watches
        </h4>
      </v-app-bar-title>
      <v-badge v-if="notifications.length > 0" :content="notifications.length">
        <v-menu :location="start">
          <template v-slot:activator="{ props }">
            <v-btn
              density="compact"
              v-bind="props"
              icon="mdi-bell-outline"
            ></v-btn>
          </template>

          <V-list>
            <v-list-item v-for="(alert, idx) in notifications" :key="idx">
              <v-list-item-subtitle>
                {{ alert }}
              </v-list-item-subtitle>
            </v-list-item>
          </V-list>
        </v-menu>
      </v-badge>

      <v-btn v-else density="compact" icon="mdi-bell-outline"></v-btn>
    </v-app-bar>
  </div>
</template>

<script>
import { useUserStore } from "@/store/userStore";
import { useWatchStore } from "@/store/watchStore";
import { useNotificationStore } from "@/store/notification";
import axios from "axios";

export default {
  data() {
    return {
      drawer: null,
      notifications: ["Hi There"],
      userStore: "",
      watchStore: "",
      reactiveCounter: this.$RC
    };
  },
  computed: {
    getUserName() {
      return this.userStore.getUserName;
    },
    getUserID() {
      return this.userStore.getUserId;
    },
    getNotifications() {
      return useNotificationStore().getTopNotifications
    }
  },
  methods: {
    removeUserStore() {
      this.userStore.removeUser();
      this.userStore.logout();
    },
    removeWatchStore() {
      this.watchStore.removeWatch;
      console.log(this.watchStore.getWatch);
    },
  },
  watch: {
    async getNotifications(newVal) {
      if (newVal) {
        try {
        console.log(111)
        const userID = this.userStore.getUserId();
        const notificationResponse = await axios.get(
          `http://127.0.0.1:8000/notification/${userID}`
        );
        const notificationData = notificationResponse.data.data.notifications;
        for (let i = 0; i < notificationData.length; i++) {
          if (notificationData[i].notification_type == "outbid") {
            this.notifications.push(
              `You have been outbidded at Auction ID: ${notificationData[i].auction_id}`
            );
          } else if (
            notificationData[i].notification_type == "winandpayremind"
          ) {
            this.notifications
              .push(`Congratulations on winning auction ID: ${notificationData[i].auction_id}. 
          Do log into Timely Watches and pay for the item within 1 hour. Or else, you may lose your item and the item will be offered to the second highest bidder.`);
          } else if (
            notificationData[i].notification_type == "rollbackandpayremind"
          ) {
            this.notifications
              .push(`Congratulations on winning auction ID: ${notificationData[i].auction_id}. 
          As the highest bidder has given up the offer, the item will be offered to you! Do log into Timely Watches and pay for the item within 1 hour.
          Or else, you may lose your item and the item will be offered to the second highest bidder..`);
          } else if (
            notificationData[i].notification_type == "schedulesuccess"
          ) {
            this.notifications.push(
              `You have scheduled a timeslot for auction ID: ${notificationData[i].auction_id}.`
            );
          }
        }
      this.notifications = this.notifications.slice(-5)
      } catch (error) {
        console.error(error);
      }
      }
    }
  },
  created() {
    const userStore = useUserStore();
    const watchStore = useWatchStore;
    this.userStore = userStore;
    this.watchStore = watchStore;
    console.log(this.reactiveCounter)
  },
  async mounted() {
    const notificationStore = useNotificationStore();

    console.log(this.notifications);
    console.log(notificationStore.getTopNotifications);
    if (!notificationStore.getTopNotifications) {
      try {
        const userID = this.userStore.getUserId();
        const notificationResponse = await axios.get(
          `http://127.0.0.1:8000/notification/${userID}`
        );
        const notificationData = notificationResponse.data.data.notifications;
        for (let i = 0; i < notificationData.length; i++) {
          if (notificationData[i].notification_type == "outbid") {
            this.notifications.push(
              `You have been outbidded at Auction ID: ${notificationData[i].auction_id}`
            );
          } else if (
            notificationData[i].notification_type == "winandpayremind"
          ) {
            this.notifications
              .push(`Congratulations on winning auction ID: ${notificationData[i].auction_id}. 
          Do log into Timely Watches and pay for the item within 1 hour. Or else, you may lose your item and the item will be offered to the second highest bidder.`);
          } else if (
            notificationData[i].notification_type == "rollbackandpayremind"
          ) {
            this.notifications
              .push(`Congratulations on winning auction ID: ${notificationData[i].auction_id}. 
          As the highest bidder has given up the offer, the item will be offered to you! Do log into Timely Watches and pay for the item within 1 hour.
          Or else, you may lose your item and the item will be offered to the second highest bidder..`);
          } else if (
            notificationData[i].notification_type == "schedulesuccess"
          ) {
            this.notifications.push(
              `You have scheduled a timeslot for auction ID: ${notificationData[i].auction_id}.`
            );
          }
        }
      this.notifications = this.notifications.slice(-5)
      } catch (error) {
        console.error(error);
      }
    }
    else {
      this.notifications = notificationStore.getTopNotifications
    }
  },
};
</script>


<style scoped>
.topbar {
  display: flex;
  justify-content: center;
  align-items: center;
}

@font-face {
  font-family: Riviera Nights;
  src: url(@/styles/rivieraNights/RivieraNights-Black.otf);
}

.header {
  font-family: Riviera Nights, sans-serif;
}

.router-link {
  text-decoration: none;
  color: black;
}
</style>