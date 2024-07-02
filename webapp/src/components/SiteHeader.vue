<template>
  <header class="max-w-[859px] mx-auto relative font-['IBM_Plex_Sans'] mb-16">
    <div class="max-w-6xl mx-auto px-4 flex items-center justify-between h-20">
      <div class="flex items-center">
        <img src="/assets/backwave.svg" alt="Backwave logo" class="w-16 h-16" />
        <h1 class="text-5xl font-bold ml-2 text-black self-start mt-1">Backwave</h1>
      </div>
      <nav class="flex items-center space-x-8">
        <a href="#" class="flex items-center relative" :class="{ 'text-zinc-900': currentPage === 'participate', 'text-green-800': currentPage !== 'participate' }" @click="changePage('participate')">
          <inline-svg src="/assets/hash-icon.svg" class="w-7 h-7 mr-2" />
          <span class="text-xl font-bold leading-9">Participate</span>
          <div v-if="currentPage === 'participate'" class="w-full h-0.5 bg-black absolute bottom-[-4px] left-0"></div>
        </a>
        <a href="#" class="flex items-center relative" :class="{ 'text-zinc-900': currentPage === 'create', 'text-green-800': currentPage !== 'create' }" @click="changePage('create')">
          <inline-svg src="/assets/yes-icon.svg" class="w-7 h-7 mr-2" />
          <span class="text-xl font-bold leading-9">Create</span>
          <div v-if="currentPage === 'create'" class="w-full h-0.5 bg-black absolute bottom-[-4px] left-0"></div>
        </a>
        <a href="#" class="flex items-center relative" :class="{ 'text-zinc-900': currentPage === 'analyze', 'text-green-800': currentPage !== 'analyze' }" @click="changePage('analyze')">
          <inline-svg src="/assets/analyze-icon.svg" class="w-7 h-7 mr-2" />
          <span class="text-xl font-bold leading-9">Analyze</span>
          <div v-if="currentPage === 'analyze'" class="w-full h-0.5 bg-black absolute bottom-[-4px] left-0"></div>
        </a>
      </nav>
    </div>
  </header>
</template>

<script>
import { ref } from 'vue';
import InlineSvg from 'vue-inline-svg';

export default {
  name: 'SiteHeader',
  components: {
    InlineSvg,
  },
  props: {
    initialPage: {
      type: String,
      default: 'create'
    }
  },
  setup(props, { emit }) {
    const currentPage = ref(props.initialPage);

    const changePage = (page) => {
      currentPage.value = page;
      emit('page-changed', page);
    };

    return {
      currentPage,
      changePage,
    };
  },
};
</script>