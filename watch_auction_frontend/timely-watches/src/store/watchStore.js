// Utilities
import { defineStore } from "pinia";

export const useWatchStore = defineStore("watch", {
  state: () => ({
    watch: null,
  }),
  actions: {
    setWatch(watch) {
      this.watch = watch;
    },
    incrementCurrentPrice(amount) {
      this.watch.CurrentPrice += amount;
    },
    incrementCurrentBid(amount) {
      this.watch.CurrentBid += amount;
    },
    convertCurrentBid() {
      this.watch.CurrentBid = this.watch.CurrentPrice
    },
    removeWatch() {
      this.watch = ''
    }
  },
  getters: {
    getCurrentPrice() {
      return this.watch.CurrentPrice;
    },
    getWatch() {
      return this.watch
    },
    getCurrentBid() {
      return this.watch.CurrentBid
    },
    getWatchImages() {
      return this.watch.ImageList
    },
    getAuctionId() {
      return this.watch.auctionID
    }
  },
  persist: {
    enabled: true,
  },
});
