<template>
  <div class="script-search-panel">
    <div class="search-header">
      <input 
        v-model="searchQuery" 
        placeholder="강의 내용 검색..." 
        class="search-input"
        @input="handleSearch"
      />
    </div>
    
    <div class="search-results" v-if="filteredSegments.length > 0">
      <div 
        v-for="(segment, index) in filteredSegments" 
        :key="index"
        class="result-item"
        @click="$emit('seek-to', segment.start)"
      >
        <span class="timestamp">{{ formatTime(segment.start) }}</span>
        <p class="content" v-html="highlight(segment.content)"></p>
      </div>
    </div>
    <div v-else-if="searchQuery" class="no-results">
      검색 결과가 없습니다.
    </div>
  </div>
</template>

<script setup>
import { ref, computed, defineProps } from 'vue';

const props = defineProps({
  scriptSegments: {
    type: Array, // [{start: 0, content: "...", keywords: []}]
    default: () => []
  }
});

const searchQuery = ref('');

const filteredSegments = computed(() => {
  if (!searchQuery.value) return [];
  const query = searchQuery.value.toLowerCase();
  return props.scriptSegments.filter(seg => 
    seg.content.toLowerCase().includes(query) || 
    (seg.keywords && seg.keywords.some(k => k.toLowerCase().includes(query)))
  );
});

const formatTime = (seconds) => {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s < 10 ? '0' : ''}${s}`;
};

const highlight = (text) => {
  if (!searchQuery.value) return text;
  const regex = new RegExp(`(${searchQuery.value})`, 'gi');
  return text.replace(regex, '<mark>$1</mark>');
};
</script>

<style scoped>
.script-search-panel {
  display: flex;
  flex-direction: column;
  height: 100%;
  border-left: 1px solid #eee;
  background: white;
}

.search-header {
  padding: 1rem;
  border-bottom: 1px solid #f0f0f0;
}

.search-input {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.search-results {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
}

.result-item {
  padding: 0.8rem;
  border-bottom: 1px solid #f5f5f5;
  cursor: pointer;
  transition: background 0.2s;
}

.result-item:hover {
  background: #f9f9f9;
}

.timestamp {
  font-size: 0.8rem;
  color: #666;
  font-weight: bold;
}

.content {
  font-size: 0.9rem;
  color: #333;
  margin-top: 0.3rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.no-results {
  padding: 2rem;
  text-align: center;
  color: #999;
}
</style>
