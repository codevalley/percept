<template>
  <div class="w-full">
    <div class="relative h-6 bg-neutral-200 rounded-full overflow-hidden">
      <div 
        class="absolute top-0 left-0 h-full rounded-full flex items-center justify-end pr-2"
        :class="activeColor"
        :style="{ width: `${percentage}%` }"
      >
        <span class="text-xs font-medium" :class="complementaryColor">{{ percentage.toFixed(1) }}%</span>
      </div>
    </div>
    <div class="flex justify-between mt-1 text-xs" :class="complementaryColor">
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
    },
    activeColor: {
      type: String,
      default: 'bg-accent-green'
    },
    complementaryColor: {
      type: String,
      default: 'text-primary'
    }
  }
}
</script>