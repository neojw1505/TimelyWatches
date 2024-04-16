import { defineStore } from "pinia";

export const useNotificationStore = defineStore("notification", {
  state: () => ({
    notifications: [],
  }),
  actions: {
    setNotifications(notificationList) {
      this.notifications = notificationList;
    },
  },
  getters: {
    getNotifications() {
      return this.notifications;
    },
    getTopNotifications() {
        return this.notifications.slice(-5)
    }
  },
  persist: {
    enabled: true,
  },
});