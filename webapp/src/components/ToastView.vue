<template>
  <Transition
    enter-active-class="transition duration-300 ease-out"
    enter-from-class="transform translate-y-2 opacity-0"
    enter-to-class="transform translate-y-0 opacity-100"
    leave-active-class="transition duration-300 ease-in"
    leave-from-class="transform translate-y-0 opacity-100"
    leave-to-class="transform translate-y-2 opacity-0"
  >
    <div 
      v-if="isVisible" 
      class="fixed top-5 right-5 px-6 py-3 rounded-md font-bold text-white shadow-lg z-50"
      :class="[
        type === 'success' ? 'bg-accent-green' : 'bg-accent',
      ]"
    >
      {{ $t(message) }}
    </div>
  </Transition>
</template>

<script>
import { ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';

export default {
  name: 'ToastView',
  props: {
    message: {
      type: String,
      required: true
    },
    type: {
      type: String,
      default: 'success',
      validator: (value) => ['success', 'error'].includes(value)
    },
    duration: {
      type: Number,
      default: 3000
    }
  },
  emits: ['hidden'],
  setup(props, { emit }) {
    const { t } = useI18n();
    const isVisible = ref(false);

    const showToast = () => {
      console.log('Showing toast:', t(props.message), props.type);
      isVisible.value = true;
      setTimeout(() => {
        hideToast();
      }, props.duration);
    };

    const hideToast = () => {
      isVisible.value = false;
      emit('hidden');
    };

    watch(() => props.message, (newVal) => {
      if (newVal) {
        showToast();
      }
    });

    return {
      isVisible,
      showToast,
      hideToast
    };
  }
};
</script>