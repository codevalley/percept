<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-100">
    <h1 class="text-4xl font-bold mb-8 text-gray-800">Welcome to Percept</h1>
    <div class="flex justify-center space-x-6 mt-8">
      <button @click="$emit('participate')" class="px-6 py-3 text-lg font-semibold text-white bg-blue-500 rounded-full hover:bg-blue-600 transition duration-300">
        Participate
      </button>
      <button @click="$emit('create')" class="px-6 py-3 text-lg font-semibold text-white bg-green-500 rounded-full hover:bg-green-600 transition duration-300">
        Create
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeView'
}
</script>