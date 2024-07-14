<template>
    <div class="max-w-[768px] mx-auto px-4 pt-16 text-center">
      <h1 class="text-3xl font-bold text-accent mb-4">404 - Page Not Found</h1>
      <p class="text-xl text-primary">The page you're looking for doesn't exist or has been moved.</p>
      <router-link to="/" class="mt-8 inline-block px-6 py-2 bg-primary text-white rounded-full">
        Go Home
      </router-link>
    </div>
  </template>
  
  <script>
  export default {
    name: 'NotFound'
  }
  </script>