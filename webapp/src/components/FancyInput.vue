<template>
  <div class="fancy-input-wrapper" :style="wrapperStyle">
    <div 
      class="fancy-background"
      :class="[
        { 'checking': isChecking, 'valid': isValid && isFocused, 'error': isError },
        isChecking ? 'conic' : isError ? 'error-bg' : 'neutral-bg'
      ]"
      :style="backgroundStyle"
    >
      <div class="fancy-inner flex items-center justify-between rounded-full" :style="innerStyle">
        <div v-if="icon" class="icon-container" :style="iconContainerStyle">
          <inline-svg 
            :src="iconToShow" 
            :class="['cursor-pointer', iconColorClass]" 
            :style="iconStyle"
            @click="$emit('rotate')" 
          />
        </div>
        <div class="input-container flex-grow" :class="{ 'text-center': !icon }">
          <input 
            ref="fancyInput"
            :value="modelValue"
            @input="handleInput"
            @focus="handleFocus"
            @blur="handleBlur"
            class="bg-transparent focus:outline-none w-full"
            :class="[isError ? 'text-red-500' : textColor, fontSize]"
            :style="inputStyle"
            :placeholder="placeholder"
          />
          <span ref="measureSpan" :class="fontSize" class="measure-span font-medium"></span>
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
    maxWidth: {
      type: String,
      default: null,
    },
    minWidth: {
      type: String,
      default: null,
    },
    borderWidth: {
      type: Number,
      default: 2,
    },
    inputHeight: {
      type: String,
      default: '38px',
    },
    iconSize: {
      type: String,
      default: '24px',
    },
    fontSize: {
      type: String,
      default: 'text-base',
    },
  },
  emits: ['update:modelValue', 'rotate', 'input'],
  setup(props, { emit }) {
    const fancyInput = ref(null);
    const measureSpan = ref(null);
    const isFocused = ref(false);
    const dynamicWidth = ref('auto');

    const wrapperStyle = computed(() => ({
      '--border-width': `${props.borderWidth}px`,
      width: dynamicWidth.value,
      maxWidth: props.maxWidth,
      minWidth: props.minWidth,
    }));

    const backgroundStyle = computed(() => ({
      '--bg-color': props.bgColor,
      '--loader-color': props.loaderColor,
      '--valid-border-color': props.validBorderColor,
      '--error-bg-color': props.errorBgColor,
      '--input-height': props.inputHeight,
    }));

    const iconContainerStyle = computed(() => ({
      width: props.iconSize,
      height: props.iconSize,
      minWidth: props.iconSize,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      marginRight: '8px', // Space between icon and input
    }));

    const iconStyle = computed(() => ({
      width: '100%',
      height: '100%',

    }));
    
    const innerStyle = computed(() => ({
      height: props.inputHeight,
      padding: props.icon ? `0 8px 0 8px` : `0 8px`, // Adjust padding based on icon presence
    }));

    const inputStyle = computed(() => ({
      height: props.inputHeight,
      paddingRight: '8px', // Add some padding on the right side
      paddingLeft: props.icon? `0` : `8px`,
      textAlign: props.icon ? 'left' : 'center', // Center text if no icon
    }));

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
        const iconWidth = props.icon ? parseInt(props.iconSize) : 0;
        const newWidth = `${measureSpan.value.offsetWidth + iconWidth + (props.icon ? 36 : 34)}px`; // Adjust padding based on icon presence
        dynamicWidth.value = newWidth;
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
      wrapperStyle,
      backgroundStyle,
      innerStyle,
      inputStyle,
      iconToShow,
      iconColorClass,
      handleInput,
      handleFocus,
      handleBlur,
      iconContainerStyle,
      iconStyle,
    };
  },
};
</script>

<style scoped>
.fancy-input-wrapper {
  display: inline-flex;
  align-items: center;
  position: relative;
}

.fancy-background {
  position: relative;
  z-index: 0;
  border-radius: 9999px;
  overflow: hidden;
  background-color: var(--bg-color);
  transition: all 0.3s ease;
  width: 100%;
  height: calc(var(--input-height) + (var(--border-width) * 2));
}

.fancy-background::before {
  content: '';
  position: absolute;
  inset: 0;
  background-color: var(--bg-color);
  border-radius: 9999px;
}

.fancy-background.valid::before {
  background-color: var(--valid-border-color);
}

.fancy-background.error-bg::before {
  background-color: var(--error-bg-color);
}

.fancy-background.conic::after {
  content: '';
  position: absolute;
  top: -150%;
  left: -150%;
  right: -150%;
  bottom: -150%;
  background-image: conic-gradient(
    from 0deg,
    var(--loader-color),
    var(--bg-color),
    var(--loader-color),
    var(--bg-color),
    var(--loader-color)
  );
  animation: rotate 2s linear infinite;

  opacity: 0.7; /* Adjust this value for visibility during debugging */
}

.fancy-inner {
  position: absolute;
  top: var(--border-width);
  left: var(--border-width);
  right: var(--border-width);
  bottom: var(--border-width);
  background: white;
  z-index: 1;
}
.input-container {
  position: relative;
  overflow: hidden; /* Prevent text from overflowing */
}

.input-container.text-center input {
  text-align: center;
}

@keyframes rotate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
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