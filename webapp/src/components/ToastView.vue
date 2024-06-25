<template>
    <transition name="fade">
      <div v-if="isVisible" class="toast" :class="type">
        {{ message }}
      </div>
    </transition>
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
  
  <style scoped>
  .toast {
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 10px 20px;
    border-radius: 4px;
    color: white;
    font-weight: bold;
    z-index: 9999;
  }
  
  .success {
    background-color: #4CAF50;
  }
  
  .error {
    background-color: #F44336;
  }
  
  .fade-enter-active, .fade-leave-active {
    transition: opacity 0.5s;
  }
  .fade-enter, .fade-leave-to {
    opacity: 0;
  }
  </style>