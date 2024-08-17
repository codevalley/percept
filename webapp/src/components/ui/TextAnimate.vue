<template>
  <h2 class="animated-text">
    <transition-group name="fade" tag="span">
      <span v-for="(word, wordIndex) in words" :key="`word-${wordIndex}`" class="word">
        <transition-group name="fade" tag="span">
          <span 
            v-for="(letter, letterIndex) in word.split('')" 
            :key="`letter-${wordIndex}-${letterIndex}`" 
            class="letter"
          >
            {{ letter }}
          </span>
        </transition-group>
        {{ wordIndex < words.length - 1 ? ' ' : '' }}
      </span>
    </transition-group>
  </h2>
</template>

<script>
import { ref, watch } from 'vue';

export default {
  name: 'TextAnimate',
  props: {
    text: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const words = ref([]);

    const animateText = () => {
      words.value = props.text.split(' ');
    };

    watch(() => props.text, animateText, { immediate: true });

    return {
      words
    };
  }
}
</script>

<style scoped>
.animated-text {
  display: inline-block;
}

.word {
  display: inline-block;
  margin-right: 0.25em;
}

.letter {
  display: inline-block;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease, transform 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>