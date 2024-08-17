<template>
  <span>{{ displayValue }}</span>
</template>

<script>
import { ref, watch, onMounted, onUnmounted } from 'vue';
import gsap from 'gsap';

export default {
  name: 'AnimatedNumber',
  props: {
    value: {
      type: Number,
      required: true
    },
    duration: {
      type: Number,
      default: 1
    },
    precision: {
      type: Number,
      default: 0
    },
    format: {
      type: Function,
      default: num => num.toLocaleString()
    }
  },
  setup(props, { emit }) {
    const displayValue = ref(props.format(0));
    let tween = null;

    const animateValue = () => {
      if (tween) tween.kill();
      
      const obj = { value: parseFloat(displayValue.value.replace(/,/g, '')) };
      tween = gsap.to(obj, {
        value: props.value,
        duration: props.duration,
        ease: 'power2.out',
        onStart: () => emit('animationStart'),
        onUpdate: () => {
          displayValue.value = props.format(parseFloat(obj.value.toFixed(props.precision)));
        },
        onComplete: () => emit('animationComplete')
      });
    };

    watch(() => props.value, animateValue);

    onMounted(animateValue);
    onUnmounted(() => {
      if (tween) tween.kill();
    });

    return { displayValue };
  }
}
</script>