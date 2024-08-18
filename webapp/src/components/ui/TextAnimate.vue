<template>
  <component :is="wrapperTag" ref="textContainer">
    <!-- Handle word-based animation types -->
    <template v-if="['rollIn', 'whipIn'].includes(type)">
      <span
        v-for="(word, wordIndex) in words"
        :key="`word-${wordIndex}`"
        class="inline-block whitespace-nowrap"
      >
        <transition-group
          :name="type"
          tag="span"
          :style="getWordTransitionStyle(wordIndex)"
          appear
        >
          <span
            v-for="(char, charIndex) in word.split('')"
            :key="`char-${wordIndex}-${charIndex}`"
            class="inline-block"
          >
            {{ char }}
          </span>
        </transition-group>
        {{ wordIndex < words.length - 1 ? ' ' : '' }}
      </span>
    </template>
    <!-- Handle letter-based animation types -->
    <template v-else>
      <transition-group
        :name="type"
        tag="span"
        appear
      >
        <span
          v-for="(letter, index) in letters"
          :key="`letter-${index}`"
          :style="getLetterStyle(index)"
          class="inline-block"
        >
          {{ letter === ' ' ? '\u00A0' : letter }}
        </span>
      </transition-group>
    </template>
  </component>
</template>

<script>
import { ref, computed, onMounted } from 'vue';

export default {
  name: 'TextAnimate',
  props: {
    text: {
      type: String,
      required: true
    },
    type: {
      type: String,
      default: 'fadeIn',
      validator: (value) => [
        'fadeIn',
        'fadeInUp',
        'popIn',
        'shiftInUp',
        'rollIn',
        'whipIn',
        'whipInUp',
        'calmInUp'
      ].includes(value)
    },
    delay: {
      type: Number,
      default: 0.25
    },
    duration: {
      type: Number,
      default: 0.75
    }
  },
  setup(props) {
    const textContainer = ref(null);
    const words = computed(() => props.text.split(' '));
    const letters = computed(() => Array.from(props.text));

    const wrapperTag = computed(() => ['rollIn', 'whipIn'].includes(props.type) ? 'h2' : 'span');

    const getWordTransitionStyle = (index) => ({
      '--delay': `${props.delay + index * 0.13}s`,
      '--stagger': '0.025s'
    });

    const getLetterStyle = (index) => ({
      '--index': index,
      '--total': letters.value.length,
      '--delay': `${props.delay + index * 0.05}s`,
      'animation-delay': `calc(var(--delay) + ${index * 0.05}s)`
    });

    onMounted(() => {
      if (textContainer.value) {
        textContainer.value.style.setProperty('--duration', `${props.duration}s`);
      }
    });

    return {
      textContainer,
      words,
      letters,
      wrapperTag,
      getWordTransitionStyle,
      getLetterStyle
    };
  }
};
</script>


<style scoped>
.fade-in-enter-active,
.fade-in-leave-active,
.fade-in-up-enter-active,
.fade-in-up-leave-active,
.pop-in-enter-active,
.pop-in-leave-active,
.shift-in-up-enter-active,
.shift-in-up-leave-active,
.roll-in-enter-active,
.roll-in-leave-active,
.whip-in-enter-active,
.whip-in-leave-active,
.whip-in-up-enter-active,
.whip-in-up-leave-active,
.calm-in-up-enter-active,
.calm-in-up-leave-active {
  transition-duration: var(--duration);
  transition-timing-function: cubic-bezier(0.175, 0.885, 0.32, 1.275);
  transition-delay: var(--delay);
}

.fade-in-enter-from,
.fade-in-leave-to {
  opacity: 0;
}

.fade-in-up-enter-from,
.fade-in-up-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

.pop-in-enter-from,
.pop-in-leave-to {
  opacity: 0;
  transform: scale(0);
}

.shift-in-up-enter-from,
.shift-in-up-leave-to {
  transform: translateY(100%);
}

.roll-in-enter-from,
.roll-in-leave-to,
.whip-in-enter-from,
.whip-in-leave-to {
  opacity: 0;
  transform: translateY(0.35em);
}

.whip-in-up-enter-from,
.whip-in-up-leave-to {
  transform: translateY(200%);
}

/* Add custom styles for each animation type as needed */
</style>
