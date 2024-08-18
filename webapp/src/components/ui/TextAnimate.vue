<template>
  <component :is="wrapperTag" :class="wrapperClass" ref="textContainer">
    <template v-if="['rollIn', 'whipIn'].includes(type)">
      <span
        v-for="(word, wordIndex) in words"
        :key="`word-${wordIndex}`"
        class="inline-block mr-[0.25em] whitespace-nowrap"
      >
        <transition-group
          :name="type"
          tag="span"
          :style="getWordTransitionStyle(wordIndex)"
        >
          <span
            v-for="(char, charIndex) in word.split('')"
            :key="`char-${wordIndex}-${charIndex}`"
            class="inline-block -mr-[0.01em]"
          >
            {{ char }}
          </span>
        </transition-group>
      </span>
    </template>
    <template v-else>
      <transition-group
        :name="type"
        tag="span"
        :style="{ display: 'flex', overflow: 'hidden' }"
      >
        <span
          v-for="(letter, index) in letters"
          :key="`letter-${index}`"
          :style="getLetterStyle(index)"
        >
          {{ letter === ' ' ? '\u00A0' : letter }}
        </span>
      </transition-group>
    </template>
  </component>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue';

export default {
  name: 'TextAnimate',
  props: {
    text: {
      type: String,
      required: true
    },
    type: {
      type: String,
      default: 'whipInUp',
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
      default: 0
    },
    duration: {
      type: Number,
      default: 0.75
    }
  },
  setup(props) {
    const textContainer = ref(null);
    const isVisible = ref(false);

    const words = computed(() => props.text.split(' '));
    const letters = computed(() => Array.from(props.text));

    const wrapperTag = computed(() => ['rollIn', 'whipIn'].includes(props.type) ? 'h2' : 'span');
    const wrapperClass = computed(() => [
      'mt-10 text-4xl font-black text-black dark:text-neutral-100 py-5 pb-8 px-8 md:text-5xl',
      { 'flex flex-wrap': !['rollIn', 'whipIn'].includes(props.type) }
    ]);

    const getWordTransitionStyle = (index) => ({
      '--delay': `${index * 0.13}s`,
      '--stagger': '0.025s'
    });

    const getLetterStyle = (index) => ({
      '--index': index,
      '--total': letters.value.length,
      '--delay': `${props.delay + (index * 0.05)}s`
    });

    onMounted(() => {
      const observer = new IntersectionObserver(
        ([entry]) => {
          isVisible.value = entry.isIntersecting;
        },
        { threshold: 0.1 }
      );

      if (textContainer.value) {
        observer.observe(textContainer.value);
      }

      return () => {
        if (textContainer.value) {
          observer.unobserve(textContainer.value);
        }
      };
    });

    watch(isVisible, (newValue) => {
      if (newValue) {
        textContainer.value.classList.add('animate');
      } else {
        textContainer.value.classList.remove('animate');
      }
    });

    return {
      textContainer,
      words,
      letters,
      wrapperTag,
      wrapperClass,
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
  transition-duration: v-bind('duration + "s"');
  transition-timing-function: cubic-bezier(0.175, 0.885, 0.32, 1.275);
  transition-delay: calc(var(--delay) + var(--index) * 0.05s);
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
  transform: translateY(0.25em);
}

.whip-in-up-enter-from,
.whip-in-up-leave-to {
  transform: translateY(200%);
}

.calm-in-up-enter-from,
.calm-in-up-leave-to {
  transform: translateY(200%);
}

.roll-in-enter-active,
.whip-in-enter-active {
  transition-delay: calc(var(--delay) + var(--index) * var(--stagger));
}
</style>