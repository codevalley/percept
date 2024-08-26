<template>
  <div class="sortable-list-container">
    <draggable 
      v-if="!isTouchDevice"
      :model-value="modelValue" 
      @update:model-value="$emit('update:modelValue', $event)"
      item-key="id"
      :disabled="disabled"
      @start="drag = true"
      @end="drag = false"
    >
      <template #item="{ element }">
        <div class="sortable-item" :class="{ 'is-dragging': drag }">
          <slot :item="element"></slot>
        </div>
      </template>
    </draggable>

    <div v-else>
      <div v-for="element in modelValue" :key="element.id" class="sortable-item">
        <slot :item="element"></slot>
      </div>
    </div>

    <!-- Visual marker -->
    <div class="implementation-marker" :class="{ 'touch': isTouchDevice, 'non-touch': !isTouchDevice }"></div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import draggable from 'vuedraggable';

export default {
  name: 'SortableList',
  components: {
    draggable
  },
  props: {
    modelValue: {
      type: Array,
      required: true
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update:modelValue'],
  setup() {
    const drag = ref(false);
    const isTouchDevice = ref(false);

    onMounted(() => {
      isTouchDevice.value = 'ontouchstart' in window || navigator.maxTouchPoints > 0 || navigator.msMaxTouchPoints > 0;
      console.log('Is touch device:', isTouchDevice.value);
    });

    return {
      drag,
      isTouchDevice
    };
  }
}
</script>

<style scoped>
.sortable-list-container {
  position: relative;
}

.sortable-item {
  transition: all 0.3s;
}

.sortable-item.is-dragging {
  opacity: 0.5;
}

.implementation-marker {
  position: absolute;
  top: 5px;
  right: 5px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.implementation-marker.touch {
  background-color: #ff0000; /* Red for touch devices */
}

.implementation-marker.non-touch {
  background-color: #00ff00; /* Green for non-touch devices */
}
</style>