<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <v-container>
    <v-tabs v-model="tab" align-tabs="center" color="amber-lighten-2">
      <v-tab v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</v-tab>
    </v-tabs>
      <v-row align="center" justify="center">
        <v-col v-for="(watch, index) in watches[tab]" :key="index" cols="4">
          <WatchCard
            v-if="watch"
            :referenceNo="index"
            :watch="watch"
          />
        </v-col>
      </v-row>
    </v-container>
</template>

<script setup>
  import WatchCard from '@/components/WatchCard.vue'
</script>

<script>
import axios from 'axios'
import { useUserStore } from '@/store/userStore'
import { useNotificationStore } from '@/store/notification'


  export default {
    data() {
      return {
        categories: ['Rolex', 'Patek Philippe', 'Audemars Piguet'],
        tab: null,
        auctionData: null,
        watches: {
      'Rolex': {
       
      },
      'Patek Philippe': {
       
      },
      'Audemars Piguet': {
        
      }
    }, 
    userStore: '',
      }
    },
    computed: {
    watchLength() {
      return this.watches[this.tab] ? this.watches[this.tab].length : 0
    },
  },
  methods: {
    async getAndSetNotification() {
            const userID = useUserStore().getUserId()
            console.log(userID)
            const notificationResponse = await axios.get(`http://127.0.0.1:8000/notification/${userID}`)
            const notificationData = notificationResponse.data.data.notifications
            const notificationList = []
                for (let i = 0; i < notificationData.length; i++) {
                    if (notificationData[i].notification_type == 'outbid') {
                        notificationList.push(`You have been outbidded at Auction ID: ${notificationData[i].auction_id}`)
                    }
                    else if (notificationData[i].notification_type == 'winandpayremind') {
                        notificationList.push(`Congratulations on winning auction ID: ${notificationData[i].auction_id}. 
                        Do log into Timely Watches and pay for the item within 1 hour. Or else, you may lose your item and the item will be offered to the second highest bidder.`)
                    }
                    else if (notificationData[i].notification_type == 'rollbackandpayremind') {
                        notificationList.push(`Congratulations on winning auction ID: ${notificationData[i].auction_id}. 
                        As the highest bidder has given up the offer, the item will be offered to you! Do log into Timely Watches and pay for the item within 1 hour.
                        Or else, you may lose your item and the item will be offered to the second highest bidder..`)
                    }
                    else if (notificationData[i].notification_type == 'schedulesuccess') {
                        notificationList.push(`You have scheduled a timeslot for auction ID: ${notificationData[i].auction_id}.`)
                    }
                }
            console.log(notificationList)
            const notificationStore = useNotificationStore()
            notificationStore.setNotifications(notificationList)
        }
  },

   async mounted() {
      try {
        this.getAndSetNotification()
        const userResponse = await axios.get(`http://127.0.0.1:8000/user/${this.userStore.getUser().email}`)
        const userData = userResponse.data.data
        const userID = userData.id
        this.userStore.setUserId(userID)
        console.log(userID)
      } catch (error) {
        console.error('Error getting user:', error.message);
        throw error; // Re-throw the error to propagate it further
      }

      this.tab = this.categories[0]; // Initialize tab to the first category
      try {
        const response = await axios.get('http://127.0.0.1:8000/auction')
        this.auctionData = response.data.data.auctions;
        for (let i = 0; i < this.auctionData.length; i++) {
        const currentBid = this.auctionData[i].current_price > this.auctionData[i].start_price ? this.auctionData[i].current_price  : 'No bids made';
        const currentPrice = Number.isInteger(currentBid) ? this.auctionData[i].current_price + 500 : this.auctionData[i].current_price;
        if (this.auctionData[i].watch_brand == 'Rolex') {
          this.watches['Rolex'][this.auctionData[i].watch_ref] = {
            'auctionID' : this.auctionData[i].auction_id,
            'title' : this.auctionData[i].auction_item,
            'manufactureYear' : this.auctionData[i].manufacture_year,
            'StartDate' : this.auctionData[i].start_time,
            'EndDate' : this.auctionData[i].end_time,
            'MinBid' : this.auctionData[i].start_price,
            'CurrentPrice' : currentPrice,
            'CurrentBid' : currentBid,
            'WatchBoxPresent' : this.auctionData[i].watch_box_present,
            'WatchPapersPresent' : this.auctionData[i].watch_papers_present,
            'Condition' : this.auctionData[i].watch_condition,
            'AuctionWinner' : this.auctionData[i].auction_winner_id,
            'AuctionStatus' : this.auctionData[i].auction_status,
            'ImageList' : [this.auctionData[i].watch_image1, this.auctionData[i].watch_image2, this.auctionData[i].watch_image3],
            'imageURL' : this.auctionData[i].watch_image1 
          }
        }
        else if (this.auctionData[i].watch_brand == 'Patek Philippe') {
          this.watches['Patek Philippe'][this.auctionData[i].watch_ref] = {
            'auctionID' : this.auctionData[i].auction_id,
            'title' : this.auctionData[i].auction_item,
            'manufactureYear' : this.auctionData[i].manufacture_year,
            'StartDate' : this.auctionData[i].start_time,
            'EndDate' : this.auctionData[i].end_time,
            'MinBid' : this.auctionData[i].start_price,
            'CurrentPrice' : currentPrice,
            'CurrentBid' : currentBid,
            'WatchBoxPresent' : this.auctionData[i].watch_box_present,
            'WatchPapersPresent' : this.auctionData[i].watch_papers_present,
            'Condition' : this.auctionData[i].watch_condition,
            'AuctionWinner' : this.auctionData[i].auction_winner_id,
            'AuctionStatus' : this.auctionData[i].auction_status,
            'ImageList' : [this.auctionData[i].watch_image1, this.auctionData[i].watch_image2, this.auctionData[i].watch_image3],
            'imageURL' : this.auctionData[i].watch_image1 
          }
        }
        else {
          this.watches['Audemars Piguet'][this.auctionData[i].watch_ref] = {
            'auctionID' : this.auctionData[i].auction_id,
            'title' : this.auctionData[i].auction_item,
            'manufactureYear' : this.auctionData[i].manufacture_year,
            'StartDate' : this.auctionData[i].start_time,
            'EndDate' : this.auctionData[i].end_time,
            'MinBid' : this.auctionData[i].start_price,
            'CurrentPrice' : currentPrice,
            'CurrentBid' : currentBid,
            'WatchBoxPresent' : this.auctionData[i].watch_box_present,
            'WatchPapersPresent' : this.auctionData[i].watch_papers_present,
            'Condition' : this.auctionData[i].watch_condition,
            'AuctionWinner' : this.auctionData[i].auction_winner_id,
            'AuctionStatus' : this.auctionData[i].auction_status,
            'ImageList' : [this.auctionData[i].watch_image1, this.auctionData[i].watch_image2, this.auctionData[i].watch_image3],
            'imageURL' : this.auctionData[i].watch_image1 
          }
        }
    }
      }
      catch (error) {
        console.error('Error fetching auction data', error.message, error.status)
      }
      
    },
    created() {
      const userStore = useUserStore()
      this.userStore= userStore
    }
}
</script>

