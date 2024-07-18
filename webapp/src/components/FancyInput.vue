<template>
  <div class="fancy-input-wrapper" :style="wrapperStyle">
    <div class="fancy-background" :class="[
      { 'checking': isChecking, 'valid': isValid && isFocused, 'error': isError, 'disabled': disabled },
      isChecking ? 'conic' : 'neutral-bg'
    ]" :style="backgroundStyle">
      <div class="fancy-inner flex items-center justify-between rounded-full" :style="innerStyle">
        <div v-if="icon" class="icon-container" :style="iconContainerStyle">
          <inline-svg :src="iconToShow" :class="['cursor-pointer', iconColorClass]" :style="iconStyle"
            @click="$emit('rotate')" />
        </div>
        <div class="input-container flex-grow" :class="{ 'text-center': !icon }">
          <input ref="fancyInput" :value="modelValue" @input="handleInput" @focus="handleFocus" @blur="handleBlur"
            class="bg-transparent focus:outline-none w-full" :class="[textColorClass, fontSize]" :style="inputStyle"
            :placeholder="placeholder" :disabled="disabled" />
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
    disabled: {
      type: Boolean,
      default: false,
    },
    bgColor: {
      type: String,
      default: 'white',
    },
    disabledBgColor: {
      type: String,
      default: '#F3F4F6',
    },
    textColor: {
      type: String,
      default: 'text-primary',
    },
    disabledTextColor: {
      type: String,
      default: 'text-gray-400',
    },
    iconColor: {
      type: String,
      default: 'text-primary',
    },
    loaderColor: {
      type: String,
      default: '#BE185D',
    },
    borderColor: {
      type: String,
      default: '#E5E7EB',
    },
    disabledBorderColor: {
      type: String,
      default: '#F3F4F6',
    },
    validBorderColor: {
      type: String,
      default: '#22C55E',
    },
    errorBorderColor: {
      type: String,
      default: '#EF4444',
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
      '--border-color': props.disabled ? props.disabledBorderColor :
        props.isError ? props.errorBorderColor :
          props.isValid && isFocused.value ? props.validBorderColor :
            props.borderColor,
      '--loader-color': props.loaderColor,
      '--input-height': props.inputHeight,
    }));

    const innerStyle = computed(() => ({
      height: props.inputHeight,
      padding: props.icon ? `0 8px 0 8px` : `0 8px`,
      backgroundColor: props.disabled ? props.disabledBgColor : props.bgColor,
    }));

    const iconContainerStyle = computed(() => ({
      width: props.iconSize,
      height: props.iconSize,
      minWidth: props.iconSize,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      marginRight: '8px',
    }));

    const iconStyle = computed(() => ({
      width: '100%',
      height: '100%',
    }));

    const inputStyle = computed(() => ({
      height: props.inputHeight,
      paddingRight: '8px',
      paddingLeft: props.icon ? `0` : `8px`,
      textAlign: props.icon ? 'left' : 'center',
    }));

    const iconToShow = computed(() => {
      if (props.isError) return '/assets/error-icon.svg';
      if (props.isValid && isFocused.value) return '/assets/check-icon.svg';
      return props.icon;
    });

    const iconColorClass = computed(() => {
      if (props.disabled) return 'text-gray-400';
      if (props.isError) return 'text-red-500';
      if (props.isValid && isFocused.value) return 'text-green-500';
      return props.iconColor;
    });

    const textColorClass = computed(() => {
      if (props.disabled) return props.disabledTextColor;
      if (props.isError) return 'text-red-500';
      return props.textColor;
    });

    const adjustWidth = () => {
      if (fancyInput.value && measureSpan.value) {
        measureSpan.value.textContent = fancyInput.value.value || fancyInput.value.placeholder || '';
        const iconWidth = props.icon ? parseInt(props.iconSize) : 0;
        const newWidth = `${measureSpan.value.offsetWidth + iconWidth + (props.icon ? 36 : 34)}px`;
        dynamicWidth.value = newWidth;
      }
    };

    const handleInput = (event) => {
      if (!props.disabled) {
        emit('update:modelValue', event.target.value);
        emit('input', event);
        nextTick(adjustWidth);
      }
    };

    const handleFocus = () => {
      if (!props.disabled) {
        isFocused.value = true;
      }
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
    watch(() => props.modelValue, adjustWidth);
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
      textColorClass,
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
  background-color: var(--border-color);
  transition: all 0.3s ease;
  width: 100%;
  height: calc(var(--input-height) + (var(--border-width) * 2));
}

.fancy-background::before {
  content: '';
  position: absolute;
  inset: 0;
  background-color: var(--border-color);
  border-radius: 9999px;
}

.fancy-background.conic::after {
  content: '';
  position: absolute;
  top: -150%;
  left: -150%;
  right: -150%;
  bottom: -150%;
  background-image: conic-gradient(from 0deg,
      var(--loader-color),
      var(--border-color),
      var(--loader-color),
      var(--border-color),
      var(--loader-color));
  animation: rotate 2s linear infinite;
  opacity: 0.7;
}

.fancy-inner {
  position: absolute;
  top: var(--border-width);
  left: var(--border-width);
  right: var(--border-width);
  bottom: var(--border-width);
  z-index: 1;
  border-radius: 9999px;
}

.input-container {
  position: relative;
  overflow: hidden;
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