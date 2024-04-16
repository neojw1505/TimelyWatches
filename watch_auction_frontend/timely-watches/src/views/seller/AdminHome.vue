<template>
    <v-container class="mx-auto">
        <h1>Admin Home</h1>
    </v-container>  
  <v-row>
    <v-col cols="12" sm="6" md="4">
  <v-card
    class="mx-auto"
    height="200"
    image="https://static01.nyt.com/images/2020/05/02/style/02sp-watchauctions-inyt-online/merlin_130053107_f07713e8-2205-431f-aac8-908f9685c780-articleLarge.jpg?quality=75&auto=webp&disable=upscale"
    max-width="200"
    theme="dark"
    title="Create Auction"
    link
    href="/admin/create"
  ></v-card>
    </v-col>
    <v-col cols="12" sm="6" md="4">
  <v-card
    class="mx-auto"
    height="200"
    image="https://cst.brightspotcdn.com/dims4/default/d86ce2a/2147483647/strip/true/crop/1600x834+0+33/resize/840x438!/quality/90/?url=https%3A%2F%2Fcdn.vox-cdn.com%2Fthumbor%2FIrCISbrrwiqzQDZkky92b0fTNbo%3D%2F0x0%3A1600x900%2F1600x900%2Ffilters%3Afocal%28550x500%3A551x501%29%2Fcdn.vox-cdn.com%2Fuploads%2Fchorus_asset%2Ffile%2F20064251%2Fslack_imgs.jpg"
    max-width="200"
    theme="dark"
    title="View Auction List"
    link
    href="/admin/auctionlist"
  ></v-card>
    </v-col>
    <v-col cols="12" sm="6" md="4">
  <v-card
    class="mx-auto"
    height="200"
    image="https://images.pexels.com/photos/5386754/pexels-photo-5386754.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
    max-width="200"
    theme="dark"
    title="View Schedule"
    link
    href="/admin/adminschedule"
  ></v-card>
</v-col>
  </v-row>
</template>
<style>
    .mx-auto {
        margin-left: 10px;
        margin-right: 10px;
        margin-top: 20px;
    }
</style>
