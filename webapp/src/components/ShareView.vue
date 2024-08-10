<template>
  <div class="border border-neutral-300 rounded-[25px] p-3 sm:p-5">
    <div :class="{'grid grid-cols-1 sm:grid-cols-2 gap-4': isCreator, 'flex justify-center': !isCreator}">
      <!-- Review Column (always visible) -->
      <div class="flex flex-col items-center p-2 sm:p-3">
        <h2 class="text-lg font-bold mb-2">{{ surveyLinkLabel }}</h2>
        <div @click="handleQRClick('survey')" class="cursor-pointer mb-4">
          <QRCode :value="surveyLink" :size="200" level="M" />
        </div>
        <FancyButton
          :label="surveyCode"
          icon="/assets/copy-icon.svg"
          :disabled="false"
          :is-actioning="false"
          @click="copyToClipboard('surveyCode')"
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

      <!-- Result Column (only for creators) -->
      <div v-if="isCreator" class="flex flex-col items-center p-2 sm:p-3">
        <h2 class="text-lg font-bold mb-2">{{ userLinkLabel }}</h2>
        <div @click="handleQRClick('results')" class="cursor-pointer mb-4">
          <QRCode :value="resultsLink" :size="200" level="M" />
        </div>
        <FancyButton
          :label="userCode"
          icon="/assets/copy-icon.svg"
          :disabled="false"
          :is-actioning="false"
          @click="copyToClipboard('userCode')"
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
        <p class="text-sm text-gray-600 mt-2">{{ userLinkDescription }}</p>
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
    surveyCode: String,
    userCode: String,
    isCreator: Boolean,
  },
  setup(props, { emit }) {
    const baseUrl = computed(() => process.env.VUE_APP_BASE_URL || '');
    const surveyLink = computed(() => `${baseUrl.value}/${props.surveyCode}`);
    const resultsLink = computed(() => `${baseUrl.value}/u/${props.userCode}`);

    const surveyLinkLabel = computed(() => props.isCreator ? "Review link" : "Your review link");
    const userLinkLabel = computed(() => "Result link");
    const surveyLinkDescription = computed(() => "Share it with your friends for feedback");
    const userLinkDescription = computed(() => "Bookmark and come here later to see results");

    const copyToClipboard = (type) => {
      const textToCopy = type === 'surveyCode' ? surveyLink.value : resultsLink.value;
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
      surveyLinkLabel,
      userLinkLabel,
      surveyLinkDescription,
      userLinkDescription,
      copyToClipboard,
      handleQRClick,
    };
  }
}
</script>