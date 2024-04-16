<template>
  <div v-if="loading2" class="loading-screen">
    <!-- add a watch pun -->
    <div>
      <h1 class="white-background rounded padded">
        Tick Tock Tick Tock..Submitting your bid~...
      </h1>
      <div class="loading-container">
        <div class="loading-spinner"></div>
      </div>
    </div>
  </div>
  <v-layout class="d-flex justify-space-between">
    <v-container>
      <v-row>
        <v-col cols="6" ml="3">
          <v-carousel show-arrows="hover" cycle hide-delimiter-background>
            <v-carousel-item v-for="(slide, i) in watchImages" :key="i">
              <div class="carousel-item">
                <img :src="slide" alt="Watch Image" />
              </div>
            </v-carousel-item>
          </v-carousel>
        </v-col>
        <v-col cols="6">
          <div>
            <v-sheet
              border="md"
              class="pa-6 mx-auto"
              color="amber-lighten-5"
              max-width="500"
              :style="{ fontFamily: 'Riviera Nights', minHeight: '500px' }"
            >
              <h2 class="sheet-title">Watch Name: {{ auctionName }}</h2>
              <v-divider class="mt-3 mb-3"></v-divider>

              <span class="d-flex justify-space-between">
                <h5 class="mb-3">
                  Start Date of Auction: <u>{{ auctionStartDate }}</u>
                </h5>

                <v-dialog max-width="500">
                  <template v-slot:activator="{ props: activatorProps }">
                    <v-btn
                      v-bind="activatorProps"
                      class="mb-2 mr-2"
                      rounded
                      :disabled="!isBidEnabled || isLeader"
                      >Bid</v-btn
                    >
                  </template>
                  <template v-slot:default="{ isActive }">
                    <v-card title="Confirm Bid of Amount">
                      <v-card-text>
                        Please confirm that you are willing and able to make a
                        total bid of $SGD {{ bidAmount }}
                      </v-card-text>

                      <v-card-subtitle
                        class="text-white-50"
                        style="white-space: normal"
                      >
                        Disclaimer: Down Payment of 10% of the Watch Winning Bid
                        must be made before full payment and claim of watch
                      </v-card-subtitle>

                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn
                          text="Close"
                          @click="isActive.value = false"
                        ></v-btn>
                        <v-btn
                          text="Make Bid"
                          @click="createBid(isActive)"
                        ></v-btn>
                      </v-card-actions>
                    </v-card>
                  </template>
                </v-dialog>
              </span>

              <h5 class="mb-3">
                End Date of Auction: <u>{{ auctionEndDate }}</u>
              </h5>

              <v-divider class="mt-3 mb-3"></v-divider>

              <u
                ><h4 class="mb-5 mainbid">
                  Next Bid to be placed: {{ bidAmount }} SGD
                </h4></u
              >

                <!-- add v-if -->
                <h5 class="mb-3 winner" v-if="isLeader || winnerTrue">You are the highest bidder</h5>
                <h5 class="mb-3 loser" v-else>You are not the highest bidder</h5>

              <!-- <h5 class="mb-3" v-if="isCurrentBidString">Current Bid: {{ Watch.CurrentBid }}</h5> -->
              <h5 class="mb-3" v-if="auctionCurrentPrice == 0">
                There has been no bids placed yet
              </h5>
              <h5 class="mb-3" v-else>
                Current Bid: $SGD {{ auctionCurrentPrice }}
              </h5>
              <h5 class="mb-3">Starting Bid: $SGD {{ auctionStartPrice }}</h5>
              <p class="mb-3">Watch Condition: {{ watchCondition }}</p>
              <p class="mb-3">Watch Box Present: {{ isWatchBoxPresent }}</p>
              <p class="mb-3">
                Watch Papers Present: {{ isWatchPapersPresent }}
              </p>

              <p class="mb-3">Watch Status: In Progress</p>
              <!-- add a v-if -->
              <v-divider class="mt-3 mb-3"></v-divider>
              <v-row v-if="winnerTrue">
                <v-col>
                  <v-btn color="success" @click="redirectToCheckout">Checkout</v-btn>
                </v-col>
              </v-row>
              <v-row v-else>
                <v-col>
                  <v-btn color="grey" @click="handleClick" disabled>Checkout</v-btn>
                </v-col>
              </v-row>
            </v-sheet>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </v-layout>
</template>


<script>
import { ref, watch, computed, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useWatchStore } from "@/store/watchStore";
import { useUserStore } from "@/store/userStore";
import { useNotificationStore } from "@/store/notification";
import axios from "axios";

export default {
  setup() {
    // Using Router variables
    const router = useRouter();
    const route = useRoute();
    const renderKey = ref(0);
    const winnerTrue = ref(false);
    const realWinner = ref("");
    const loading2 = ref(false);
    const isLeader = ref(false);

    // User details
    const userStore = useUserStore();
    const userId = computed(() => userStore.userID);
    const watchAuctionData = ref(0);
    

    // Fetch Auction Data on Before Mount
    onMounted(async () => {
      try {
        watchAuctionData.value = setInterval(fetchAuctionPrice, 100);
        getAndSetNotification();
        checkWinner();

        // checkWinner();
      } catch (error) {
        console.error(error);
      }
    });
    const id = route.params.id;

    // AuctionData Object
    const AuctionData = ref({});
    // Reactive properties
    const watchImages = ref([]);
    const auctionId = ref(0);
    const auctionName = ref("");
    const auctionStartDate = ref("");
    const auctionEndDate = ref("");
    const auctionStartPrice = ref(0);
    const auctionCurrentPrice = ref(0);
    const isWatchBoxPresent = ref(false);
    const isWatchPapersPresent = ref(false);
    const watchCondition = ref("");
    const reactiveCounter = ref(0);

    const isBidEnabled = computed(() => {
      const watchStartDate = new Date(auctionStartDate.value);
      const watchEndDate = new Date(auctionEndDate.value);

      // 2 hours in milliseconds
      const currentDate = new Date();

      return currentDate >= watchStartDate && currentDate <= watchEndDate;
    });

    const bidAmount = computed(() => {
      if (auctionCurrentPrice.value == 0) {
        return auctionStartPrice.value;
      } else {
        return auctionCurrentPrice.value + 500;
      }
    });

    watch(
      watchAuctionData,
      (newValue, oldValue) => {
        console.log("myValue changed from", oldValue, "to", newValue);
        try {
          console.log('fetching works')
          getAndSetNotification();

          // checkWinner();
        } catch (error) {
          console.error(error);
        }
      },
      { deep: true }
    );

    // Method: Fetch Data

    const fetchAuctionPrice = async () => {
      console.log("watching");
      const watchStore = useWatchStore();
      const auctionID = watchStore.getAuctionId;
      const response = await axios.get(
        `http://127.0.0.1:8000/auction/${auctionID}`
      );
      AuctionData.value = response.data;
      const obj = response.data.data;
      console.log(response.data);

      watchImages.value = [
        obj.watch_image1,
        obj.watch_image2,
        obj.watch_image3,
      ];
      auctionId.value = obj.auction_id;
      auctionName.value = obj.auction_item;
      auctionStartDate.value = obj.start_time;
      auctionEndDate.value = obj.end_time;
      auctionStartPrice.value = obj.start_price;
      auctionCurrentPrice.value = obj.current_price;
      isWatchBoxPresent.value = obj.watch_box_present
        ? "Present"
        : "Not Present";
      isWatchPapersPresent.value = obj.watch_papers_present
        ? "Present"
        : "Not Present";
      watchCondition.value = obj.watch_condition;
      checkLeader();
      checkWinner();
      watchAuctionData.value = obj.current_price
    };

    // Method: Get Notifications and set to Store
    const getAndSetNotification = async () => {
      const notificationResponse = await axios.get(
        `http://127.0.0.1:8000/notification/${userId.value}`
      );
      const notificationData = notificationResponse.data.data.notifications;
      const notificationList = [];
      for (let i = 0; i < notificationData.length; i++) {
        if (notificationData[i].notification_type == "outbid") {
          notificationList.push(
            `You have been outbidded at Auction ID: ${notificationData[i].auction_id}`
          );
        } else if (notificationData[i].notification_type == "winandpayremind") {
          notificationList.push(`Congratulations on winning auction ID: ${notificationData[i].auction_id}. 
                        Do log into Timely Watches and pay for the item within 1 hour. Or else, you may lose your item and the item will be offered to the second highest bidder.`);
        } else if (
          notificationData[i].notification_type == "rollbackandpayremind"
        ) {
          notificationList.push(`Congratulations on winning auction ID: ${notificationData[i].auction_id}. 
                        As the highest bidder has given up the offer, the item will be offered to you! Do log into Timely Watches and pay for the item within 1 hour.
                        Or else, you may lose your item and the item will be offered to the second highest bidder..`);
        } else if (notificationData[i].notification_type == "schedulesuccess") {
          notificationList.push(
            `You have scheduled a timeslot for auction ID: ${notificationData[i].auction_id}.`
          );
        }
      }

      const notificationStore = useNotificationStore();
      notificationStore.setNotifications(notificationList);
    };

    // Method: Create Bid
    const createBid = async (isActive) => {
      let bid = bidAmount.value;
      try {
        const bidParams = {
          auction_id: auctionId.value,
          bid_amount: bid,
          user_id: userId.value,
        };
        // make loading2 true
        loading2.value = true;
        const response = await axios.post(
          `http://127.0.0.1:8000/processbid/authbid`,
          bidParams
        );
        if (response.status > 200 && response.status < 300) {
          reactiveCounter.value++;
          console.log(reactiveCounter.value);
          isActive.value = false;
          loading2.value = false;
        } else {
          throw new Error("Unexpected Response status: " + response.data);
        }
      } catch (error) {
        alert("There is an error processing your bid");
        console.error("Error creating bid:", error);
        throw error;
      }
    };

    // Method 2: Check Winner on Mounted

    const checkWinner = async () => {
      try {
        const watchStore = useWatchStore();
        const auctionID = watchStore.getAuctionId;
        const response = await axios.get(
          `http://127.0.0.1:8000/auction/${auctionID}`
        );
        realWinner.value = response.data.data.auction_winner_id;
        console.log(realWinner.value);
        console.log(userId.value);
        if (
          realWinner.value == userId.value &&
          !(response.data.data.auction_status == 0 || response.data.data.auction_status == 1)
        ) {
          winnerTrue.value = true;
          renderKey.value++;
          console.log(winnerTrue.value);
        } 
        else if (
          realWinner.value == userId.value &&
          response.data.data.auction_status == 1
        ) {
          winnerTrue.value = true;
          renderKey.value++;
          console.log(winnerTrue.value);
        }
        else {
          winnerTrue.value = false;

        }
      } catch (error) {
        console.error(error);
      }
    };
    const handleClick = () => {
      console.log("clicked");
      checkWinner();
    };
    // Method: Check if winner
    const checkLeader = async () => {
      try {
        const watchStore = useWatchStore();
        const auctionID = watchStore.getAuctionId;
        const response = await axios.get(
          `http://127.0.0.1:8000/auction/${auctionID}`
        );
        realWinner.value = response.data.data.auction_winner_id;
        console.log(realWinner.value);
        console.log(userId.value);
        if (
          realWinner.value == userId.value &&
          response.data.data.auction_status == 1
        ) {
          isLeader.value = true;
        } else {
          isLeader.value = false;
        }
      } catch (error) {
        console.error(error);
      }
    };

    // Method: Redirect to Checkout
    const redirectToCheckout = () => {
      router.push({ name: "Checkout", params: { id: auctionId.value } });
    };

    return {
      userId,
      id,
      auctionId,
      bidAmount,
      AuctionData,
      auctionName,
      auctionStartDate,
      auctionEndDate,
      auctionStartPrice,
      auctionCurrentPrice,
      watchCondition,
      loading2,
      isWatchBoxPresent,
      handleClick,
      checkWinner,
      isWatchPapersPresent,
      createBid,
      watchImages,
      isBidEnabled,
      redirectToCheckout,
      getAndSetNotification,
      winnerTrue,
      fetchAuctionPrice,
      reactiveCounter,
      isLeader,
      checkLeader,
    };
  },
};
</script>


<style scoped>
@font-face {
  font-family: Riviera Nights;
  src: url(@/styles/rivieraNights/RivieraNights-Regular.otf);
}

.sheet-title {
  font-family: Riviera Nights, sans-serif;
  font-style: oblique;
}

p {
  font-size: 14px;
}

.carousel-item {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 400px; /* Set the height of the carousel item as needed */
}

.carousel-item img {
  min-width: 100%;
  min-height: 100%;
  object-fit: contain; /* Adjust the object-fit property as needed */
}

.mainbid {
  font-size: 40px;
  font-weight: bold;
  color: white;
  background-color: black;
  padding: 10px;
  text-align: center;

  
}

.img-container {
  padding: 0 0px; /* Adjust as needed */
}
.my-table td,
.my-table th {
  border: 1px solid #000; /* Add lines */
  padding: 10px; /* Add spacing */
}

.loading-screen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.loading-spinner {
  border: 16px solid #f3f3f3;
  border-top: 16px solid #3498db;
  border-radius: 50%;
  width: 120px;
  height: 120px;
  animation: spin 500ms linear infinite;
}
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 17vh; /* This makes the container take up the full height of the viewport */
}

.winner{
  color: green;
  font-weight: bold;

}
.loser{
  color: red;
  font-weight: bold;
}

.white-background {
  background-color: white;
}

.rounded {
  border-radius: 40px;
}

.padded {
  padding: 20px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>