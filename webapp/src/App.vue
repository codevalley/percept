<template>
  <div id="app" class="font-['IBM_Plex_Sans'] min-h-screen bg-white">
    <SiteHeader @page-changed="handlePageChange" />
    <router-view></router-view>
  </div>
</template>

<script>
import { useRouter } from 'vue-router';
import SiteHeader from '@/components/SiteHeader.vue';

export default {
  name: 'App',
  components: {
    SiteHeader,
  },
  setup() {
    const router = useRouter();

    const handlePageChange = (page) => {
      console.log(`Page changed to: ${page}`);
      // Handle navigation based on the page
      switch(page) {
        case 'home':
          router.push('/');
          break;
        case 'create':
          router.push('/create');
          break;
        case 'participate':
          // This might open the participate input in the header instead of navigating
          break;
        case 'analyze':
          // This might open the analyze input in the header instead of navigating
          break;
        default:
          console.warn(`Unhandled page change: ${page}`);
      }
    };

    return {
      handlePageChange
    };
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;700&display=swap');

#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>