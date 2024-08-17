<template>
  <span class="type-writer">
    {{ displayText }}<span class="cursor" :class="{ 'blink': isCursorVisible }"></span>
  </span>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue';

export default {
  name: 'TypeWriter',
  props: {
    texts: {
      type: Array,
      required: true
    },
    delay: {
      type: Number,
      default: 1000
    },
    typingSpeed: {
      type: Number,
      default: 50
    }
  },
  setup(props) {
    const displayText = ref('');
    const currentTextIndex = ref(0);
    const isCursorVisible = ref(true);
    let typingInterval = null;
    let cursorInterval = null;

    const typeText = () => {
      const currentText = props.texts[currentTextIndex.value];
      let charIndex = 0;

      clearInterval(typingInterval);
      typingInterval = setInterval(() => {
        if (charIndex < currentText.length) {
          displayText.value += currentText[charIndex];
          charIndex++;
        } else {
          clearInterval(typingInterval);
          setTimeout(eraseText, props.delay);
        }
      }, props.typingSpeed);
    };

    const eraseText = () => {
      clearInterval(typingInterval);
      typingInterval = setInterval(() => {
        if (displayText.value.length > 0) {
          displayText.value = displayText.value.slice(0, -1);
        } else {
          clearInterval(typingInterval);
          currentTextIndex.value = (currentTextIndex.value + 1) % props.texts.length;
          setTimeout(typeText, props.typingSpeed);
        }
      }, props.typingSpeed / 2);
    };

    const blinkCursor = () => {
      cursorInterval = setInterval(() => {
        isCursorVisible.value = !isCursorVisible.value;
      }, 500);
    };

    onMounted(() => {
      typeText();
      blinkCursor();
    });

    onUnmounted(() => {
      clearInterval(typingInterval);
      clearInterval(cursorInterval);
    });

    return {
      displayText,
      isCursorVisible
    };
  }
}
</script>

<style scoped>
.type-writer {
  position: relative;
}

.cursor {
  display: inline-block;
  width: 2px;
  height: 1em;
  background-color: currentColor;
  margin-left: 2px;
  vertical-align: middle;
}

.cursor.blink {
  animation: blink 0.7s infinite;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}
</style>