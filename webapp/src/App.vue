<template>
  <div id="app">
    <SiteHeader />
    <router-view v-slot="{ Component }">
      <component :is="Component" />
    </router-view>
    <Toast 
      :message="toastMessage" 
      :type="toastType" 
      :duration="3000"
      @hidden="handleToastHidden"
    />
  </div>
</template>

<script>
import { ref } from 'vue';
import SiteHeader from '@/components/SiteHeader.vue';
import Toast from '@/components/ToastView.vue';

export default {
  name: 'App',
  components: {
    SiteHeader,
    Toast
  },
  setup() {
    const toastMessage = ref('');
    const toastType = ref('success');

    const handleToastHidden = () => {
      toastMessage.value = '';
    };

    return {
      toastMessage,
      toastType,
      handleToastHidden
    };
  }
}
</script>


<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;700&display=swap');

#app {
  font-family: 'IBM Plex Sans', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>