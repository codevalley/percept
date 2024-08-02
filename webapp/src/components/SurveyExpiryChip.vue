<template>
    <div class="inline-flex items-center px-2 py-1 rounded-full text-xs font-semibold h-6"
         :class="chipClass">
      <inline-svg :src="iconSrc" class="w-4 h-4 mr-1 flex-shrink-0" />
      <span class="whitespace-nowrap leading-none">{{ chipText }}</span>
    </div>
</template>
  
  <script>
  import { computed } from 'vue';
  import InlineSvg from 'vue-inline-svg';
  
  export default {
    name: 'SurveyExpiryChip',
    components: {
      InlineSvg,
    },
    props: {
      expiryDate: {
        type: String,
        required: true
      },
      isExpired: {
        type: Boolean,
        required: true
      }
    },
    setup(props) {
      const chipClass = computed(() => {
        return props.isExpired
          ? 'bg-green-100 text-green-800'
          : 'bg-yellow-100 text-yellow-800';
      });
  
      const iconSrc = computed(() => {
        return props.isExpired
          ? '/assets/yes-icon.svg'
          : '/assets/timer-icon.svg';
      });
  
      const chipText = computed(() => {
        if (props.isExpired) {
          return 'Survey completed';
        } else {
          const timeLeft = getTimeLeft(props.expiryDate);
          return `${timeLeft} left`;
        }
      });
  
      const getTimeLeft = (expiryDate) => {
        const now = new Date();
        const expiry = new Date(expiryDate);
        const diffMs = expiry - now;
        const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
        const diffHours = Math.floor((diffMs % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const diffMinutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
  
        if (diffDays > 0) {
          return `${diffDays} day${diffDays > 1 ? 's' : ''}`;
        } else if (diffHours > 0) {
          return `${diffHours} hour${diffHours > 1 ? 's' : ''}`;
        } else {
          return `${diffMinutes} min`;
        }
      };
  
      return {
        chipClass,
        iconSrc,
        chipText
      };
    }
  }
  </script>