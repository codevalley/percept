<template>
    <button 
      class="fancy-button"
      :class="[
        { 'has-icon': icon },
        { 'disabled': disabled },
        buttonColorClass
      ]"
      :style="buttonStyle"
      @click="handleClick"
      :disabled="disabled"
    >
      <div class="button-content flex items-center justify-center">
        <inline-svg 
          v-if="icon"
          :src="icon" 
          :class="['mr-2', iconColorClass]" 
          :style="iconStyle"
        />
        <span :class="textClass">{{ label }}</span>
      </div>
      <div class="button-background"></div>
    </button>
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
    },
    setup(props, { emit }) {
      const buttonColorClass = computed(() => {
        return `button-${props.color}`;
      });
  
      const buttonStyle = computed(() => {
        const sizes = {
          small: { height: '32px', fontSize: '14px', padding: '0 12px' },
          medium: { height: '40px', fontSize: '16px', padding: '0 16px' },
          large: { height: '48px', fontSize: '18px', padding: '0 20px' },
        };
        return {
          ...sizes[props.size],
        };
      });
  
      const iconStyle = computed(() => ({
        width: props.iconSize,
        height: props.iconSize,
      }));
  
      const iconColorClass = computed(() => {
        return props.disabled ? 'text-gray-400' : `text-${props.color}-icon`;
      });
  
      const textClass = computed(() => {
        return props.disabled ? 'text-gray-400' : `text-${props.color}-text`;
      });
  
      const handleClick = (event) => {
        if (!props.disabled) {
          emit('click', event);
        }
      };
  
      return {
        buttonColorClass,
        buttonStyle,
        iconStyle,
        iconColorClass,
        textClass,
        handleClick,
      };
    },
  };
  </script>
  
  <style scoped>
  .fancy-button {
    position: relative;
    border-radius: 9999px;
    overflow: hidden;
    transition: all 0.3s ease;
    cursor: pointer;
    outline: none;
    border: none;
  }
  
  .fancy-button:disabled {
    cursor: not-allowed;
  }
  
  .button-content {
    position: relative;
    z-index: 2;
  }
  
  .button-background {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 1;
    transition: all 0.3s ease;
  }
  
  /* Primary Button Styles */
  .button-primary .button-background {
    background-color: #3B82F6; /* Blue-500 */
  }
  
  .button-primary:hover .button-background {
    background-color: #2563EB; /* Blue-600 */
  }
  
  .button-primary:active .button-background {
    background-color: #1D4ED8; /* Blue-700 */
  }
  
  .button-primary.disabled .button-background {
    background-color: #BFDBFE; /* Blue-200 */
  }
  
  /* Secondary Button Styles */
  .button-secondary .button-background {
    background-color: #6B7280; /* Gray-500 */
  }
  
  .button-secondary:hover .button-background {
    background-color: #4B5563; /* Gray-600 */
  }
  
  .button-secondary:active .button-background {
    background-color: #374151; /* Gray-700 */
  }
  
  .button-secondary.disabled .button-background {
    background-color: #E5E7EB; /* Gray-200 */
  }
  
  /* Accent Button Styles */
  .button-accent .button-background {
    background-color: #10B981; /* Green-500 */
  }
  
  .button-accent:hover .button-background {
    background-color: #059669; /* Green-600 */
  }
  
  .button-accent:active .button-background {
    background-color: #047857; /* Green-700 */
  }
  
  .button-accent.disabled .button-background {
    background-color: #A7F3D0; /* Green-200 */
  }
  
  /* Text and Icon Colors */
  .text-primary-text, .text-primary-icon { color: white; }
  .text-secondary-text, .text-secondary-icon { color: white; }
  .text-accent-text, .text-accent-icon { color: white; }
  
  .disabled .text-primary-text,
  .disabled .text-secondary-text,
  .disabled .text-accent-text,
  .disabled .text-primary-icon,
  .disabled .text-secondary-icon,
  .disabled .text-accent-icon {
    color: #9CA3AF; /* Gray-400 */
  }
  </style>