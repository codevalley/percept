<template>
  <div v-if="showSurveyLink || showResultsLink" class="border border-neutral-300 rounded-[25px] p-3 sm:p-5">
    <div class="border border-neutral-300 rounded-[25px] p-3 sm:p-5">
      <div :class="{'grid grid-cols-1 sm:grid-cols-2 gap-4': showSurveyLink && showResultsLink, 'flex justify-center': !(showSurveyLink && showResultsLink)}">
        <!-- Survey Link Column -->
        <div v-if="showSurveyLink" class="flex flex-col items-center p-2 sm:p-3">
          <h2 class="text-lg font-bold mb-2">{{ surveyLinkLabel }}</h2>
          <div @click="handleQRClick('survey')" class="cursor-pointer mb-4">
            <QRCode :value="surveyLink" :size="200" level="M" />
          </div>
          <FancyButton
            :label="surveyCode"
            icon="/assets/copy-icon.svg"
            :disabled="false"
            :is-actioning="false"
            @click="copyToClipboard('survey')"
            :border-width="1"
            button-height="40px"
            icon-size="20px"
            font-size="text-sm"
            :min-width="'60%'"
            bg-color="white"
            border-color="black"
            text-color="text-primary"
            disabled-bg-color="gray"
            disabled-border-color="gray"
            disabled-text-color="text-gray-400"
          />
          <p class="text-sm text-gray-600 mt-2">{{ surveyLinkDescription }}</p>
        </div>

        <!-- Results Link Column -->
        <div v-if="showResultsLink" class="flex flex-col items-center p-2 sm:p-3">
          <h2 class="text-lg font-bold mb-2">{{ resultsLinkLabel }}</h2>
          <div @click="handleQRClick('results')" class="cursor-pointer mb-4">
            <QRCode :value="resultsLink" :size="200" level="M" />
          </div>
          <FancyButton
            :label="resultsCode"
            icon="/assets/copy-icon.svg"
            :disabled="false"
            :is-actioning="false"
            @click="copyToClipboard('results')"
            :border-width="1"
            button-height="40px"
            icon-size="20px"
            font-size="text-sm"
            :min-width="'60%'"
            bg-color="white"
            border-color="black"
            text-color="text-primary"
            disabled-bg-color="gray"
            disabled-border-color="gray"
            disabled-text-color="text-gray-400"
          />
          <p class="text-sm text-gray-600 mt-2">{{ resultsLinkDescription }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue';
import QRCode from 'qrcode.vue';
import FancyButton from '@/components/FancyButton.vue';

export default {
  name: 'ShareView',
  components: {
    QRCode,
    FancyButton,
  },
  props: {
    showSurveyLink: Boolean,
    showResultsLink: Boolean,
    surveyCode: String,
    resultsCode: String,
    surveyLinkLabel: String,
    resultsLinkLabel: String,
    surveyLinkDescription: String,
    resultsLinkDescription: String,
    baseUrl: {
      type: String,
      default: ''
    }
  },
  emits: ['copy-success', 'copy-error'],
  setup(props, { emit }) {
    const surveyLink = computed(() => `${props.baseUrl}/${props.surveyCode}`);
    const resultsLink = computed(() => `${props.baseUrl}/u/${props.resultsCode}`);

    const copyToClipboard = (type) => {
      const textToCopy = type === 'survey' ? surveyLink.value : resultsLink.value;
      navigator.clipboard.writeText(textToCopy).then(() => {
        emit('copy-success', `Link copied to clipboard`);
      }, () => {
        emit('copy-error', 'Failed to copy link');
      });
    };

    const handleQRClick = (type) => {
      const link = type === 'survey' ? surveyLink.value : resultsLink.value;
      navigator.clipboard.writeText(link).then(() => {
        emit('copy-success', `QR code link copied to clipboard`);
      }, () => {
        emit('copy-error', 'Failed to copy QR code link');
      });
    };

    return {
      surveyLink,
      resultsLink,
      copyToClipboard,
      handleQRClick,
    };
  }
}
</script>