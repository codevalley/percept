<template>
  <svg :width="size" :height="size" :viewBox="`0 0 ${size} ${size}`" :fill="fill" :stroke="stroke">
    <g :transform="`scale(${scale})`">
      <use :xlink:href="`/assets/${name}-icon.svg#icon`" />
    </g>
  </svg>
</template>

<script>
export default {
  name: 'SvgIcon',
  props: {
    name: {
      type: String,
      required: true
    },
    size: {
      type: [Number, String],
      default: 24
    },
    fill: {
      type: String,
      default: 'none'
    },
    stroke: {
      type: String,
      default: 'currentColor'
    }
  },
  computed: {
    scale() {
      return this.size / 24; // Assuming original SVG size is 24x24
    }
  }
}
</script>