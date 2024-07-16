<template>
  <div class="fancy-button-wrapper" :style="wrapperStyle" @click="handleClick">
    <div 
      class="fancy-background"
      :class="[
        { 'has-icon': icon },
        { 'disabled': disabled },
        { 'conic': isVerifying },
        buttonColorClass
      ]"
      :style="backgroundStyle"
    >
      <div class="fancy-inner flex items-center justify-center rounded-full" :style="innerStyle">
        <div v-if="icon" class="icon-container" :style="iconContainerStyle">
          <inline-svg 
            :src="icon" 
            :class="['mr-2', iconColorClass]" 
            :style="iconStyle"
          />
        </div>
        <span :class="textClass">{{ label }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue';
import InlineSvg from 'vue-inline-svg';

export default {
  name: 'FancyButton',
  components: {
    InlineSvg,
  },
  props: {
    label: {
      type: String,
      required: true,
    },
    icon: {
      type: String,
      default: null,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    isVerifying: {
      type: Boolean,
      default: false,
    },
    color: {
      type: String,
      default: 'primary',
      validator: (value) => ['primary', 'secondary', 'accent'].includes(value),
    },
    size: {
      type: String,
      default: 'medium',
      validator: (value) => ['small', 'medium', 'large'].includes(value),
    },
    iconSize: {
      type: String,
      default: '24px',
    },
    borderWidth: {
      type: Number,
      default: 2,
    },
  },
  setup(props, { emit }) {
    const buttonHeight = computed(() => 
      props.size === 'small' ? '32px' : props.size === 'large' ? '48px' : '40px'
    );

    const wrapperStyle = computed(() => ({
      '--border-width': `${props.borderWidth}px`,
      '--button-height': buttonHeight.value,
    }));

    const backgroundStyle = computed(() => ({
      '--bg-color': props.disabled ? '#BFDBFE' : '#3B82F6',
      '--loader-color': '#BE185D',
    }));

    const innerStyle = computed(() => ({
      height: buttonHeight.value,
      padding: props.size === 'small' ? '0 12px' : props.size === 'large' ? '0 20px' : '0 16px',
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

    const buttonColorClass = computed(() => `button-${props.color}`);

    const iconColorClass = computed(() => 
      props.disabled ? 'text-gray-400' : `text-${props.color}-icon`
    );

    const textClass = computed(() => 
      props.disabled ? 'text-gray-400' : `text-${props.color}-text`
    );

    const handleClick = (event) => {
      if (!props.disabled && !props.isVerifying) {
        emit('click', event);
      }
    };

    return {
      wrapperStyle,
      backgroundStyle,
      innerStyle,
      iconContainerStyle,
      iconStyle,
      buttonColorClass,
      iconColorClass,
      textClass,
      handleClick,
    };
  },
};
</script>

<style scoped>
.fancy-button-wrapper {
  display: inline-flex;
  align-items: center;
  position: relative;
  cursor: pointer;
  padding: var(--border-width);
}

.fancy-background {
  position: relative;
  border-radius: 9999px;
  overflow: hidden;
  background-color: var(--bg-color);
  transition: all 0.3s ease;
  width: 100%;
  height: var(--button-height);
}

.fancy-background::before {
  content: '';
  position: absolute;
  inset: 0;
  background-color: var(--bg-color);
  border-radius: 9999px;
  z-index: 1;
}

.fancy-background.disabled::before {
  background-color: #E5E7EB;
}

.fancy-background.conic::after {
  content: '';
  position: absolute;
  inset: calc(-1 * var(--border-width));
  background-image: conic-gradient(
    from 0deg,
    var(--loader-color),
    var(--bg-color),
    var(--loader-color),
    var(--bg-color),
    var(--loader-color)
  );
  animation: rotate 2s linear infinite;
  z-index: 3; /* Move to top for debugging */
  opacity: 0.7;
}

.fancy-inner {
  position: relative;
  height: 100%;
  background: white;
  z-index: 2;
  border-radius: 9999px;
}

@keyframes rotate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* Button color styles */
.button-primary .fancy-inner { background-color: #3B82F6; }
.button-secondary .fancy-inner { background-color: #6B7280; }
.button-accent .fancy-inner { background-color: #10B981; }

/* Hover styles */
.fancy-button-wrapper:hover:not(.disabled) .fancy-inner { filter: brightness(1.05); }

/* Active styles */
.fancy-button-wrapper:active:not(.disabled) .fancy-inner { filter: brightness(0.95); }

/* Disabled style */
.disabled { cursor: not-allowed; }
.disabled .fancy-inner { background-color: #E5E7EB; }

/* Text and icon color styles */
.text-primary-text, .text-primary-icon { color: white; }
.text-secondary-text, .text-secondary-icon { color: white; }
.text-accent-text, .text-accent-icon { color: white; }

.disabled .text-primary-text,
.disabled .text-secondary-text,
.disabled .text-accent-text,
.disabled .text-primary-icon,
.disabled .text-secondary-icon,
.disabled .text-accent-icon {
  color: #9CA3AF;
}

/* Scale effect on click */
.fancy-button-wrapper:active:not(.disabled) {
  transform: scale(0.98);
}
</style>