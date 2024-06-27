<template>
  <Transition
    enter-active-class="transition duration-300 ease-out"
    enter-from-class="transform translate-y-2 opacity-0"
    enter-to-class="transform translate-y-0 opacity-100"
    leave-active-class="transition duration-300 ease-in"
    leave-from-class="transform translate-y-0 opacity-100"
    leave-to-class="transform translate-y-2 opacity-0"
  >
    <div v-if="isVisible" 
         class="fixed top-5 right-5 px-6 py-3 rounded-md font-bold text-white shadow-lg z-50"
         :class="[
           type === 'success' ? 'bg-green-500' : 'bg-red-500'
         ]">
      {{ message }}
    </div>
  </Transition>
</template>

<script>
export default {
  name: 'ToastView',
  props: {
    message: String,
    type: {
      type: String,
      default: 'success'
    },
    duration: {
      type: Number,
      default: 3000
    }
  },
  data() {
    return {
      isVisible: false
    }
  },
  watch: {
    message(newVal) {
      if (newVal) {
        this.showToast();
      }
    }
  },
  methods: {
    showToast() {
      console.log('Showing toast:', this.message, this.type);
      this.isVisible = true;
      setTimeout(() => {
        this.hideToast();
      }, this.duration);
    },
    hideToast() {
      this.isVisible = false;
      this.$emit('hidden');
    }
  }
}
</script>