<template>
  <draggable 
    :model-value="modelValue" 
    @update:model-value="$emit('update:modelValue', $event)"
    item-key="id"
    :disabled="disabled || isTouchDevice"
    @start="drag = true"
    @end="drag = false"
    :delay="200"
    :delayOnTouchOnly="true"
  >
    <template #item="{ element }">
      <div class="sortable-item" :class="{ 'is-dragging': drag }">
        <slot :item="element"></slot>
      </div>
    </template>
  </draggable>
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
      isTouchDevice.value = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    });

    return {
      drag,
      isTouchDevice
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