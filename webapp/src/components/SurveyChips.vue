<template>
  <div class="flex flex-wrap justify-center gap-2">
    <div v-if="isTrending" class="flex items-center px-2 py-1 bg-red-100 text-red-800 rounded-full text-xs font-semibold">
      <inline-svg src="/assets/analyze-icon.svg" class="w-4 h-4 mr-1" />
      Trending
    </div>
    <div v-if="participantBucket" class="flex items-center px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-semibold">
      <inline-svg src="/assets/scale-icon.svg" class="w-4 h-4 mr-1" />
      {{ participantBucket }} participants
    </div>
    <div v-if="timeLeft > 0" class="flex items-center px-2 py-1 bg-yellow-100 text-yellow-800 rounded-full text-xs font-semibold">
      <inline-svg src="/assets/timer-icon.svg" class="w-4 h-4 mr-1" />
      {{ timeLeft }} min left
    </div>
  </div>
</template>

<script>
import InlineSvg from 'vue-inline-svg';

export default {
  name: 'SurveyChips',
  components: {
    InlineSvg,
  },
  props: {
    isTrending: {
      type: Boolean,
      required: true
    },
    participantBucket: {
      type: String,
      default: ''
    },
    timeLeft: {
      type: Number,
      default: 0
    }
  }
}
</script>