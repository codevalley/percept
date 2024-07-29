<template>
    <div
      @click="$emit('click')"
      class="flex items-center relative cursor-pointer"
      :class="{ 'text-primary': isActive, 'text-accent': !isActive }"
    >
      <inline-svg :src="item.icon" class="w-6 h-6 sm:w-7 sm:h-7 mr-2" />
      <span class="text-lg sm:text-xl font-bold leading-9">{{ item.label }}</span>
      <div v-if="isActive" class="w-full h-0.5 bg-primary absolute bottom-[-4px] left-0"></div>
    </div>
  </template>
  
  <script>
  import InlineSvg from 'vue-inline-svg';
  
  export default {
    name: 'NavItem',
    components: {
      InlineSvg,
    },
    props: {
      item: {
        type: Object,
        required: true,
      },
      isActive: {
        type: Boolean,
        default: false,
      },
    },
    emits: ['click'],
  };
  </script>