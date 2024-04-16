<template>

    <v-container>
        <v-row dense>
            <v-col cols="12">
                <v-card elevation="4" v-for="bid in highestBids" :key="bid" :color="bid.bid_amount < bid.current_price ? 'red-lighten-4' : 'brown-lighten-4'">
                    <div class="d-flex justify-space-between">
                        <div>
                            <v-card-title class="text-h5">Auction Name : {{ bid.auction_item }} {{ bid.watch_ref }} </v-card-title>
            
                            <v-card-title >Auction ID : {{ bid.auction_id }} </v-card-title>

                            <v-card-subtitle>Your Current Bid Amount : $SGD {{ bid.bid_amount }}</v-card-subtitle>

                            <v-card-actions>
                                <v-btn @click="selectBid(bid)" class="ms-2 mr-2" size="small" variant="outlined">
                                    Enter bid
                                </v-btn>
                            </v-card-actions>

                            <v-card-actions>
                                <v-btn @click="goCheckout(bid)" class="ms-2 mr-2" color="success" size="small" 
                                variant="outlined" elevation="3" rounded :disabled="isCheckoutEnabled(bid)">
                                    Checkout
                                </v-btn>
                            </v-card-actions>
                        </div>

                        <v-avatar class="ma-3" rounded="0" size="125">
                            <v-img
                            :src="bid.watch_image2"
                            ></v-img>
                        </v-avatar>
                    </div>

                </v-card>
            </v-col>
        </v-row>
    </v-container>


</template>

<script>
import { useWatchStore } from '@/store/watchStore'
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/userStore'
import { useNotificationStore } from '@/store/notification'
import axios from 'axios'




export default {
    setup() {
        const highestBids = ref([])
        const selectedBid = ref(null);
        const router = useRouter()
        const watchStore = useWatchStore()
        const userStore = useUserStore()
        // const watchId = computed(() => route.params.id)

        const fetchData = async () => {
            const userId = computed(() => userStore.userID);
            try {
                const userResponse = await axios.get(`http://localhost:8000/processbid/getAllAuctionAndUserhighestBidByUser/${userId.value}`);
                const data = userResponse.data.data;
                console.log(data)
                highestBids.value = data;
            } catch (error) {
                console.error(error);
            }
        };

        onMounted(() => {
            // Fetch data initially
            getAndSetNotification()
            fetchData();
        });

        // Method: Get Notifications and set to Store
        const getAndSetNotification = async () => {
            const userId = computed(() => userStore.userID);
            const notificationResponse = await axios.get(`http://127.0.0.1:8000/notification/${userId.value}`)
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

            const notificationStore = useNotificationStore()
            notificationStore.setNotifications(notificationList)
        }


        const goCheckout = (bid) => {
            const auctionID = bid.auction_id;
            router.push({name : 'Checkout', params: {id: auctionID}})
        }

        const isCheckoutEnabled = (bid) => {
            // Ensure bid.end_time is properly parsed as a Date object
            const endTime = new Date(bid.end_time);
            return new Date() < endTime;
        }


        const selectBid = (bid) => {
            selectedBid.value = bid;
            const currentBid = bid.current_price > bid.start_price ? bid.current_price - 500 : 'No bids made';
            const watchDetails = {
                'auctionID' : bid.auction_id,
                'title' : bid.auction_item,
                'manufactureYear' : bid.manufacture_year,
                'StartDate' : bid.start_time,
                'EndDate' : bid.end_time,
                'MinBid' : bid.start_price,
                'CurrentPrice' : bid.current_price,
                'CurrentBid' : currentBid,
                'WatchBoxPresent' : bid.watch_box_present,
                'WatchPapersPresent' : bid.watch_papers_present,
                'Condition' : bid.watch_condition,
                'AuctionWinner' : bid.auction_winner_id,
                'AuctionStatus' : bid.auction_status,
                'ImageList' : [bid.watch_image1 , bid.watch_image2, bid.watch_image3],
                'imageURL' : bid.watch_image2,
            }

            watchStore.setWatch(watchDetails)
            router.push({name: 'AuctionDetails', 
                params: {id : bid.watch_ref},
            })
        }
        return { highestBids, selectBid, goCheckout, isCheckoutEnabled, getAndSetNotification};
    }
}



</script>

<style scoped>
.outbidded {
  background-color: #ffcdd2; /* Light red color */
}
</style>