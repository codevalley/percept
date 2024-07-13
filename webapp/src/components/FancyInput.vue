<template>
    <div class="flex items-center">
      <div :class="['fancy-border', { 'checking': isChecking, 'error': isError }]">
        <div :class="[
          'flex items-center justify-between px-4 h-full rounded-full bg-white border transition-colors',
          isValid ? 'border-accent-green' : 
          isError ? 'border-red-500' : 'border-neutral-300'
        ]">
          <inline-svg 
            :src="isError ? '/assets/error-icon.svg' : icon" 
            :class="['w-6 h-6 cursor-pointer mr-2', 
              isError ? 'text-red-500' : 'text-primary']" 
            @click="$emit('rotate')" 
          />
          <div class="relative fancy-input-container flex-grow">
            <input 
              ref="fancyInput"
              :value="modelValue"
              @input="handleInput"
              class="bg-transparent focus:outline-none w-full"
              :class="[
                'text-base font-medium',
                isError ? 'text-red-500' : 'text-primary'
              ]"
              :placeholder="placeholder"
            />
            <span ref="measureSpan" class="measure-span text-base font-medium"></span>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, watch, onMounted, nextTick } from 'vue';
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
      loaderColor: {
        type: String,
        default: 'red',
      },
    },
    emits: ['update:modelValue', 'rotate', 'input'],
    setup(props, { emit }) {
      const fancyInput = ref(null);
      const measureSpan = ref(null);
  
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
  
      watch(() => props.modelValue, adjustWidth);
      watch(() => props.placeholder, adjustWidth);
  
      onMounted(() => {
        nextTick(adjustWidth);
      });
  
      return {
        fancyInput,
        measureSpan,
        handleInput,
      };
    },
  };
  </script>
  
  <style scoped>
  .fancy-border {
    --offset: 3px;
    --loader-color: v-bind(loaderColor);
    background: white;
    border-radius: 9999px;
    position: relative;
    overflow: hidden;
    height: 40px;
    width: auto;
    display: inline-block;
  }
  
  .fancy-border::before {
    content: '';
    background: conic-gradient(transparent 270deg, var(--loader-color), transparent);
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    aspect-ratio: 1;
    width: 100%;
    opacity: 0;
    transition: opacity 0.3s ease;
  }
  
  .fancy-border.checking::before {
    opacity: 1;
    animation: rotate 2s linear infinite;
  }
  
  .fancy-border::after {
    content: '';
    background: inherit;
    border-radius: inherit;
    position: absolute;
    inset: var(--offset);
  }
  
  .fancy-border > div {
    position: relative;
    z-index: 10;
    height: 100%;
  }
  
  @keyframes rotate {
    from {
      transform: translate(-50%, -50%) scale(1.4) rotate(0turn);
    }
    to {
      transform: translate(-50%, -50%) scale(1.4) rotate(1turn);
    }
  }
  
  .fancy-input-container {
    position: relative;
    display: inline-block;
  }
  
  .fancy-input-container .measure-span {
    visibility: hidden;
    white-space: pre;
    position: absolute;
    top: 0;
    left: 0;
    z-index: -1;
  }
  </style>