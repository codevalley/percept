<template>
  <div class="w-full">
    <div class="relative w-full h-6 bg-neutral-200 rounded-full overflow-visible mt-6"> <!-- Changed to overflow-visible -->
      <!-- Progress Bar -->
      <div 
        class="absolute top-0 h-full rounded-full"
        :class="{ [activeColor]: !useProgressiveColor }"
        :style="barStyle"
      ></div>
      
      <!-- Average Value -->
      <div 
        class="absolute top-0 h-full flex items-center"
        :style="{ left: `calc(${calculatePosition(average)}% - 8px)` }"
      >
        <span class="text-xs font-medium text-primary">{{ average.toFixed(1) }}</span>
      </div>
      
      <!-- Min/Max Labels -->
      <div class="absolute w-full h-full flex items-center justify-between px-2">
        <span class="text-xs font-medium" :class="complementaryColor">1</span>
        <span class="text-xs font-medium" :class="complementaryColor">{{ max }}</span>
      </div>
      
      <!-- Median Triangle -->
      <div 
        class="absolute bottom-0 w-0 h-0 border-l-4 border-r-4 border-b-4 border-transparent"
        :class="[complementaryColor]"
        :style="{ 
          left: `calc(${calculatePosition(median)}% - 4px)`, 
          borderBottomColor: 'currentColor',
          bottom: '-4px'
        }"
      ></div>
      
      <!-- User Score Triangle -->
      <div 
        v-if="userScore"
        class="absolute top-0 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent"
        :class="[complementaryColor]"
        :style="{ 
          left: `calc(${calculatePosition(userScore)}% - 4px)`, 
          borderTopColor: 'currentColor',
          top: '-4px'
        }"
      ></div>
      
      <!-- User Score Label -->
      <div 
        v-if="userScore"
        class="absolute flex items-center"
        :style="{ 
          left: `calc(${calculatePosition(userScore)}% - 16px)`, 
          whiteSpace: 'nowrap',
          textAlign: 'center',
          width: '32px',
          top: '-24px'
        }"
      >
        <span :class="complementaryColor">{{ userScore.toFixed(1) }} (U)</span>
      </div>
    </div>
    
    <!-- Labels for Median -->
    <div class="relative mt-1">
      <div class="absolute left-0 right-0 flex justify-between text-xs">
        <!-- Median Label -->
        <div 
          class="absolute flex items-center"
          :style="{ 
            left: `calc(${calculatePosition(median)}% - 16px)`, 
            transform: 'translateX(-50%)',
            whiteSpace: 'nowrap',
            textAlign: 'center',
          }"
        >
          <span :class="complementaryColor">{{ median.toFixed(1) }} (M)</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    average: {
      type: Number,
      required: true
    },
    median: {
      type: Number,
      required: true
    },
    max: {
      type: Number,
      required: true
    },
    userScore: {
      type: Number,
      default: null
    },
    activeColor: {
      type: String,
      default: 'bg-accent-green'
    },
    complementaryColor: {
      type: String,
      default: 'text-primary'
    },
    useProgressiveColor: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    barStyle() {
      if (this.useProgressiveColor) {
        const startColor = [0xBE, 0x18, 0x5D]; // #BE185D
        const endColor = [0xD8, 0xF8, 0x9D]; // #D8F89D
        const ratio = (this.average - 1) / (this.max - 1);
        const color = startColor.map((start, i) => {
          const end = endColor[i];
          return Math.round(start + (end - start) * ratio);
        });
        return {
          width: `${this.calculateWidth(this.average)}%`,
          backgroundColor: `rgb(${color[0]}, ${color[1]}, ${color[2]})`
        };
      } else {
        return { width: `${this.calculateWidth(this.average)}%` };
      }
    }
  },
  methods: {
    calculateWidth(value) {
      // Adjust the calculation to account for rounded corners
      const adjustedMax = this.max - 1;
      const adjustedValue = value - 1;
      return (adjustedValue / adjustedMax) * 94 + 3; // 94% is the width of the rectangular part, 3% for left rounded corner
    },
    calculatePosition(value) {
      // Adjust the position calculation to account for rounded corners
      const adjustedMax = this.max - 1;
      const adjustedValue = value - 1;
      return (adjustedValue / adjustedMax) * 94 + 3; // 94% is the width of the rectangular part, 3% for left rounded corner
    }
  }
}
</script>