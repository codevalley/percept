<template>
    <draggable 
      v-model="internalItems" 
      item-key="id"
      :disabled="disabled"
      @start="drag = true"
      @end="drag = false"
    >
      <template #item="{ element, index }">
        <div class="sortable-item" :class="{ 'is-dragging': drag }">
          <slot :item="element" :index="index"></slot>
        </div>
      </template>
    </draggable>
  </template>
  
  <script>
  import { ref, computed } from 'vue';
  import draggable from 'vuedraggable';
  
  export default {
    name: 'SortableList',
    components: {
      draggable
    },
    props: {
      items: {
        type: Array,
        required: true
      },
      disabled: {
        type: Boolean,
        default: false
      }
    },
    emits: ['update:items'],
    setup(props, { emit }) {
      const drag = ref(false);
  
      const internalItems = computed({
        get: () => props.items,
        set: (value) => emit('update:items', value)
      });
  
      return {
        internalItems,
        drag
      };
    }
  }
  </script>
  
  <style scoped>
  .sortable-item {
    transition: all 0.3s;
  }
  .sortable-item.is-dragging {
    opacity: 0.5;
  }
  </style>