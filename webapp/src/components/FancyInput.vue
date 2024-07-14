<template>
  <div class="fancy-input-wrapper" :style="{ '--offset': offset + 'px' }">
    <div 
      class="fancy-background"
      :class="[
        { 'checking': isChecking, 'valid': isValid && isFocused, 'error': isError },
        isChecking ? 'conic' : isError ? 'error-bg' : neutralBorderColor
      ]"
      :style="{
        '--bg-color': bgColor,
        '--loader-color': loaderColor,
        '--valid-border-color': validBorderColor,
        '--neutral-border-color': neutralBorderColor,
        '--error-bg-color': errorBgColor
      }"
    >
      <div class="fancy-inner flex items-center justify-between px-4 rounded-full" :class="isError ? 'bg-opacity-10' : 'bg-white'">
        <inline-svg 
          :src="iconToShow" 
          :class="['w-6 h-6 cursor-pointer mr-2', iconColorClass]" 
          @click="$emit('rotate')" 
        />
        <div class="relative flex-grow">
          <input 
            ref="fancyInput"
            :value="modelValue"
            @input="handleInput"
            @focus="handleFocus"
            @blur="handleBlur"
            class="bg-transparent focus:outline-none w-full text-base font-medium"
            :class="isError ? 'text-red-500' : textColor"
            :placeholder="placeholder"
          />
          <span ref="measureSpan" class="measure-span text-base font-medium"></span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch, onMounted, nextTick } from 'vue';
import InlineSvg from 'vue-inline-svg';

export default {
  name: 'FancyInput',
  components: {
    InlineSvg,
  },
  props: {
    modelValue: {
      type: String,
      required: true,
    },
    icon: {
      type: String,
      required: true,
    },
    placeholder: {
      type: String,
      default: '',
    },
    isChecking: {
      type: Boolean,
      default: false,
    },
    isValid: {
      type: Boolean,
      default: false,
    },
    isError: {
      type: Boolean,
      default: false,
    },
    bgColor: {
      type: String,
      default: '#E5E7EB', // Tailwind's neutral-200
    },
    textColor: {
      type: String,
      default: 'text-primary',
    },
    iconColor: {
      type: String,
      default: 'text-primary',
    },
    loaderColor: {
      type: String,
      default: '#BE185D',
    },
    validBorderColor: {
      type: String,
      default: 'border-green-500',
    },
    neutralBorderColor: {
      type: String,
      default: 'border-neutral-300',
    },
    errorBgColor: {
      type: String,
      default: '#EF4444', // Tailwind's red-500
    },
    offset: {
      type: Number,
      default: 2,
    },
  },
  emits: ['update:modelValue', 'rotate', 'input'],
  setup(props, { emit }) {
    const fancyInput = ref(null);
    const measureSpan = ref(null);
    const isFocused = ref(false);

    const iconToShow = computed(() => {
      if (props.isError) return '/assets/error-icon.svg';
      if (props.isValid && isFocused.value) return '/assets/check-icon.svg';
      return props.icon;
    });

    const iconColorClass = computed(() => {
      if (props.isError) return 'text-red-500';
      if (props.isValid && isFocused.value) return 'text-green-500';
      return props.iconColor;
    });

    const adjustWidth = () => {
      if (fancyInput.value && measureSpan.value) {
        measureSpan.value.textContent = fancyInput.value.value || fancyInput.value.placeholder || '';
        fancyInput.value.style.width = `${measureSpan.value.offsetWidth}px`;
      }
    };

    const handleInput = (event) => {
      emit('update:modelValue', event.target.value);
      emit('input', event);
      nextTick(adjustWidth);
    };

    const handleFocus = () => {
      isFocused.value = true;
    };

    const handleBlur = () => {
      isFocused.value = false;
    };

    watch(() => props.modelValue, (newValue) => {
      nextTick(() => {
        if (fancyInput.value) {
          fancyInput.value.value = newValue;
          adjustWidth();
        }
      });
    });

    watch(() => props.placeholder, adjustWidth);

    onMounted(() => {
      nextTick(adjustWidth);
    });

    return {
      fancyInput,
      measureSpan,
      isFocused,
      iconToShow,
      iconColorClass,
      handleInput,
      handleFocus,
      handleBlur,
    };
  },
};
</script>

<style scoped>
.fancy-input-wrapper {
  display: inline-block;
  position: relative;
}

.fancy-background {
  position: relative;
  z-index: 0;
  border-radius: 9999px;
  overflow: hidden;
  padding: var(--offset);
  background-color: var(--bg-color);
  border: 1px solid var(--neutral-border-color);
  transition: all 0.3s ease;
}

.fancy-background.valid {
  border-color: var(--valid-border-color);
}

.fancy-background.error-bg {
  background-color: var(--error-bg-color);
  border-color: var(--error-bg-color);
}

.fancy-background::before {
  content: '';
  position: absolute;
  z-index: -2;
  top: 50%;
  left: 50%;
  width: 100%;
  padding-top: 100%;
  transform: translate(-50%, -50%);
  background-color: var(--bg-color);
  background-repeat: no-repeat;
  background-position: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.fancy-background::after {
  content: '';
  position: absolute;
  z-index: -1;
  inset: var(--offset);
  background: var(--bg-color);
  border-radius: 9999px;
}

.fancy-background.conic::before {
  opacity: 1;
  background-image: conic-gradient(var(--loader-color), var(--bg-color), var(--loader-color));
  animation: rotate 2s linear infinite;
}

.fancy-inner {
  position: relative;
  z-index: 1;
  height: 40px;
}

@keyframes rotate {
  100% {
    transform: translate(-50%, -50%) rotate(1turn);
  }
}

.measure-span {
  visibility: hidden;
  white-space: pre;
  position: absolute;
  top: 0;
  left: 0;
}
</style>