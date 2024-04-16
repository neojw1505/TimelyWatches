<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <!-- Include profile picture and allow user to upload image -->
  <div>
    <ProfilePictureUpload />
    <Settings />
  </div>
</template>




<script setup>
import ProfilePictureUpload from "@/components/ProfileUpload.vue";
import Settings from "@/components/ProfileSettings.vue";
import { useNotificationStore } from "@/store/notification";
import { useUserStore } from "@/store/userStore";
import { onMounted } from "vue";
import axios from "axios";

onMounted(async () => {
  const userID = useUserStore().getUserId();
  const notificationResponse = await axios.get(
    `http://127.0.0.1:8000/notification/${userID}`
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
});
</script>

<style scoped>
@font-face {
  font-family: Riviera Nights;
  src: url(@/styles/rivieraNights/RivieraNights-Regular.otf);
}

.text {
  font-family: Riviera Nights, sans-serif;
  font-style: italic;
}
</style>

