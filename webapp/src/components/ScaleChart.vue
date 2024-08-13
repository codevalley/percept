<template>
  <div class="w-full">
    <div class="relative w-full h-8 bg-gray-200 rounded-full">
      <div 
        class="absolute top-0 h-full bg-blue-500 rounded-full" 
        :style="{ width: `${(average / max) * 100}%` }"
      ></div>
      <div 
        class="absolute top-0 w-1 h-full bg-red-500" 
        :style="{ left: `${(median / max) * 100}%` }"
      ></div>
      <div 
        v-if="userScore"
        class="absolute top-0 w-2 h-full bg-green-500" 
        :style="{ left: `${(userScore / max) * 100}%` }"
      ></div>
    </div>
    <div class="flex justify-between mt-1 text-xs text-gray-500">
      <span>1</span>
      <span>{{ max }}</span>
    </div>
    <div class="flex justify-between mt-1 text-sm">
      <span class="text-blue-500">Average: {{ average.toFixed(1) }}</span>
      <span class="text-red-500">Median: {{ median.toFixed(1) }}</span>
      <span v-if="userScore" class="text-green-500">Your Score: {{ userScore }}</span>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    average: {
      type: Number,
      required: true
    },
    median: {
      type: Number,
      required: true
    },
    max: {
      type: Number,
      required: true
    },
    userScore: {
      type: Number,
      default: null
    }
  },
  mounted() {
    console.log('ScaleChart mounted with props:', this.$props);
  }
}
</script>