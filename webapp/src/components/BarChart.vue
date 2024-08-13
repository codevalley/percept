<template>
    <div class="w-full">
      <div class="flex items-center">
        <div class="w-full bg-gray-200 rounded-full h-6 mr-2">
          <div class="bg-green-500 h-6 rounded-full" :style="{ width: `${percentage}%` }"></div>
        </div>
        <span class="text-sm font-medium">{{ percentage.toFixed(1) }}%</span>
      </div>
      <div class="flex justify-between mt-1 text-xs text-gray-500">
        <span>No</span>
        <span>Yes</span>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      percentage: {
        type: Number,
        required: true
      }
    }
  }
  </script>