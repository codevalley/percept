<template>
    <div class="fancy-button-wrapper" :style="wrapperStyle">
      <div class="fancy-background" 
           :class="{ 'actioning': isActioning, 'disabled': disabled }" 
           :style="backgroundStyle">
        <button class="fancy-inner flex items-center justify-center rounded-full" 
                :style="innerStyle"
                :disabled="disabled" 
                @click="handleClick">
          <div v-if="icon" class="icon-container" :style="iconContainerStyle">
            <inline-svg :src="icon" 
                        :class="['cursor-pointer', iconColorClass]" 
                        :style="iconStyle" />
          </div>
          <span :class="[textColorClass, fontSize]" :style="labelStyle">{{ label }}</span>
        </button>
      </div>
    </div>
  </template>
  <script>
  import { ref, computed, onMounted, nextTick } from 'vue';
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
        default: '',
      },
      disabled: {
        type: Boolean,
        default: false,
      },
      isActioning: {
        type: Boolean,
        default: false,
      },
      bgColor: {
        type: String,
        default: '#E5E7EB',
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
      buttonHeight: {
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
    emits: ['click'],
    setup(props, { emit }) {
      const buttonRef = ref(null);
      const dynamicWidth = ref('auto');
  
      const wrapperStyle = computed(() => ({
        '--border-width': `${props.borderWidth}px`,
        width: dynamicWidth.value,
        maxWidth: props.maxWidth,
        minWidth: props.minWidth,
      }));
  
      const backgroundStyle = computed(() => ({
        '--border-color': props.disabled ? props.disabledBorderColor : props.borderColor,
        '--loader-color': props.loaderColor,
        '--button-height': props.buttonHeight,
        
      }));
  
      const innerStyle = computed(() => ({
        height: props.buttonHeight,
        backgroundColor: props.disabled && !props.isActioning ? props.disabledBgColor : props.bgColor,
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
  
      const labelStyle = computed(() => ({
        lineHeight: props.buttonHeight,
        paddingLeft: props.icon ? '0' : '8px',
      }));
  
      const iconColorClass = computed(() => {
        return props.disabled ? 'text-gray-400' : props.iconColor;
      });
  
      const textColorClass = computed(() => {
        return props.disabled ? props.disabledTextColor : props.textColor;
      });
  
      const adjustWidth = () => {
        if (buttonRef.value) {
          const iconWidth = props.icon ? parseInt(props.iconSize) : 0;
          const textWidth = buttonRef.value.offsetWidth;
          const newWidth = `${textWidth + iconWidth + (props.icon ? 36 : 32)}px`;
          dynamicWidth.value = newWidth;
        }
      };
  
      const handleClick = (event) => {
        if (!props.disabled && !props.isActioning) {
          emit('click', event);
        }
      };
  
      onMounted(() => {
        nextTick(adjustWidth);
      });
  
      return {
        buttonRef,
        wrapperStyle,
        backgroundStyle,
        innerStyle,
        iconContainerStyle,
        iconStyle,
        labelStyle,
        iconColorClass,
        textColorClass,
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
  }
  
  .fancy-background {
    position: relative;
    z-index: 0;
    border-radius: 9999px;
    overflow: hidden;
    background-color: var(--border-color);
    transition: all 0.4s ease;
    width: 100%;
    height: calc(var(--button-height) + (var(--border-width) * 2));
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
    background-image: conic-gradient(
      from 0deg,
      var(--loader-color),
      var(--border-color),
      var(--loader-color),
      var(--border-color),
      var(--loader-color)
    );
    animation: rotate 2s linear infinite;
  }
  
  .fancy-inner {
    position: absolute;
    top: var(--border-width);
    left: var(--border-width);
    right: var(--border-width);
    bottom: var(--border-width);
    z-index: 1;
    border: none;
    outline: none;
    cursor: pointer;
    transition: all 0.3s ease;
    border-radius: 9999px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .fancy-inner:disabled {
    cursor: not-allowed;
  }
  
  @keyframes rotate {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
  </style>