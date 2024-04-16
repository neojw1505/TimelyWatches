<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <v-app>
  <div class="layout">
    <video class="video-background" autoplay loop muted>
      <source src="../assets/watches.mov">
    </video>

    <div class='content'>
      <v-btn @click="toggleRegister">Toggle Form</v-btn>
      <SignUpForm v-if="isRegister" class="form" />
      <LoginForm v-else class="form" />
    </div>
  </div>
  </v-app>
</template>

<script setup>
import SignUpForm from '@/components/SignUpForm.vue';
import LoginForm from '@/components/LoginForm.vue';

</script>

<script>
export default {
  data() {
    return {
      isRegister : true,
    }
  },
  methods: {
    toggleRegister() {
      this.isRegister = !this.isRegister
    }
  }
}
</script>

<style scoped>
@font-face {
  font-family: Riviera Nights;
  src: url(@/styles/rivieraNights/RivieraNights-Regular.otf)
}

html, body, .layout {
  height: 100%;
  margin: 0; /* Remove default margins */
  overflow: hidden; /* Hide overflow to prevent scrollbars */
}

.layout {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-image: linear-gradient(to bottom, rgba(255, 187, 51, 0.8), rgba(121, 52, 0, 0.8));
  background-size: cover;
  background-repeat: no-repeat;
}

.content {
  position: relative;
  z-index: 1; /* Ensure content stays on top of the video */
  margin-top: 30px;
}

.video-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover; /* Ensure the video covers the entire area */
}

.header {
  font-family: Riviera Nights;
  font-size: 36px;
  text-align: center;
  margin-top: 20px;
  color: white;
}

.form {
  margin-bottom: 20px;
}

</style>