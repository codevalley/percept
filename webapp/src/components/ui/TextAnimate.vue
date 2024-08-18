<template>
  <span class="inline-block">
    <template v-if="shouldAnimate">
      <span
        v-for="(char, index) in characters"
        :key="`char-${index}`"
        :style="getCharStyle(index)"
        :class="`animate-${type}`"
        class="inline-block opacity-0"
      >
        {{ char === ' ' ? '\u00A0' : char }}
      </span>
    </template>
    <template v-else>
      {{ text }}
    </template>
  </span>
</template>

<script>
import { computed } from 'vue';

const validAnimationTypes = [
  'fadeIn',
  'fadeInUp',
  'popIn',
  'shiftInUp',
  'rollIn',
  'whipIn',
  'whipInUp',
  'calmInUp'
];

export default {
  name: 'TextAnimate',
  props: {
    text: {
      type: String,
      required: true
    },
    type: {
      type: String,
      default: 'fadeIn'
    },
    delay: {
      type: Number,
      default: 0
    },
    duration: {
      type: Number,
      default: 0.75
    },
    stagger: {
      type: Number,
      default: 0.03
    }
  },
  setup(props) {
    const characters = computed(() => props.text.split(''));

    const shouldAnimate = computed(() => 
      props.type !== 'none' && validAnimationTypes.includes(props.type)
    );

    const getCharStyle = (index) => ({
      'animation-delay': `${props.delay + props.stagger * index}s`,
      'animation-duration': `${props.duration}s`,
      'animation-fill-mode': 'forwards'
    });

    return {
      characters,
      shouldAnimate,
      getCharStyle
    };
  }
};
</script>

<style scoped>
@keyframes fadeIn {
  0% { opacity: 0; }
  100% { opacity: 1; }
}

@keyframes fadeInUp {
  0% { opacity: 0; transform: translateY(20px); }
  100% { opacity: 1; transform: translateY(0); }
}

@keyframes popIn {
  0% { opacity: 0; transform: scale(0); }
  100% { opacity: 1; transform: scale(1); }
}

@keyframes shiftInUp {
  0% { opacity: 0; transform: translateY(100%); }
  100% { opacity: 1; transform: translateY(0); }
}

@keyframes rollIn {
  0% { opacity: 0; transform: translateY(0.35em) rotate(-15deg); }
  100% { opacity: 1; transform: translateY(0) rotate(0); }
}

@keyframes whipIn {
  0% { opacity: 0; transform: translateY(0.35em) skewY(5deg); }
  100% { opacity: 1; transform: translateY(0) skewY(0); }
}

@keyframes whipInUp {
  0% { opacity: 0; transform: translateY(200%) skewY(-10deg); }
  100% { opacity: 1; transform: translateY(0) skewY(0); }
}

@keyframes calmInUp {
  0% { opacity: 0; transform: translateY(20px); }
  50% { opacity: 0.5; }
  100% { opacity: 1; transform: translateY(0); }
}

/* Add classes for each animation type */
.animate-fadeIn { animation-name: fadeIn; }
.animate-fadeInUp { animation-name: fadeInUp; }
.animate-popIn { animation-name: popIn; }
.animate-shiftInUp { animation-name: shiftInUp; }
.animate-rollIn { animation-name: rollIn; }
.animate-whipIn { animation-name: whipIn; }
.animate-whipInUp { animation-name: whipInUp; }
.animate-calmInUp { animation-name: calmInUp; }
</style>