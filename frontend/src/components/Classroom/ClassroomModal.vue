<template>
  <div v-if="show" class="modal-overlay" @click.self="close">
    <div class="modal-content glass-card">
      <h2 class="modal-title">강의실 입장 모드 선택</h2>
      <p class="modal-desc">학습 방식을 선택해 주세요.</p>
      
      <div class="mode-options">
        <!-- YouTube Mode -->
        <div class="mode-card" :class="{ active: selectedMode === 'youtube' }" @click="selectedMode = 'youtube'">
          <div class="icon">📺</div>
          <h3>유튜브 강의</h3>
          <p>YouTube 링크를 입력하여<br/>AI 요약과 함께 학습합니다.</p>
        </div>

        <!-- Live Mode -->
        <div class="mode-card" :class="{ active: selectedMode === 'live' }" @click="selectedMode = 'live'">
          <div class="icon">🎙️</div>
          <h3>현장 강의</h3>
          <p>PC 마이크를 통해 실시간으로<br/>강의 내용을 자막으로 변환합니다.</p>
        </div>
      </div>

      <!-- URL Input for YouTube Mode -->
      <div v-if="selectedMode === 'youtube'" class="url-input-container">
        <label>YouTube URL</label>
        <input 
          v-model="youtubeUrl" 
          type="text" 
          class="glass-input" 
          placeholder="https://www.youtube.com/watch?v=..."
          @keyup.enter="handleConfirm"
        />
      </div>

      <div class="modal-actions">
        <button class="action-btn secondary" @click="close">취소</button>
        <button class="action-btn primary" :disabled="!isReady" @click="handleConfirm">
          입장하기
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  show: Boolean
})

const emit = defineEmits(['close', 'confirm'])

const selectedMode = ref('youtube')
const youtubeUrl = ref('')

const isReady = computed(() => {
  if (selectedMode.value === 'live') return true
  return youtubeUrl.value.trim().length > 0 && youtubeUrl.value.includes('youtube.com')
})

const close = () => {
  emit('close')
}

const handleConfirm = () => {
  if (!isReady.value) return
  emit('confirm', {
    mode: selectedMode.value,
    url: youtubeUrl.value
  })
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(5px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  width: 100%;
  max-width: 500px;
  padding: 30px;
  background: rgba(28, 50, 106, 0.9);
  border-radius: 20px;
  text-align: center;
  color: white;
}

.modal-title {
  font-size: 1.5rem;
  margin-bottom: 10px;
}

.modal-desc {
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 25px;
}

.mode-options {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 25px;
}

.mode-card {
  padding: 20px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.mode-card:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-5px);
}

.mode-card.active {
  background: rgba(59, 130, 246, 0.2);
  border-color: #3b82f6;
  box-shadow: 0 0 15px rgba(59, 130, 246, 0.3);
}

.mode-card .icon {
  font-size: 2.5rem;
  margin-bottom: 10px;
}

.mode-card h3 {
  font-size: 1.1rem;
  margin-bottom: 8px;
}

.mode-card p {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.5);
  line-height: 1.4;
}

.url-input-container {
  text-align: left;
  margin-bottom: 25px;
  animation: fadeIn 0.3s ease-out;
}

.url-input-container label {
  display: block;
  font-size: 0.9rem;
  margin-bottom: 8px;
  color: #ccc;
}

.glass-input {
  width: 100%;
  padding: 12px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: white;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
}

.action-btn {
  padding: 10px 25px;
  border-radius: 8px;
  border: none;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn.primary {
  background: #3b82f6;
  color: white;
}

.action-btn.primary:disabled {
  background: #555;
  cursor: not-allowed;
}

.action-btn.secondary {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
