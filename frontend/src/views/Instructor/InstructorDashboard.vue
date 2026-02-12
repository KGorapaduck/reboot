<template>
  <div class="dashboard-container">
    <h1 class="page-title">강사 대시보드</h1>
    
    <div class="dashboard-grid">
      <!-- Upload Section -->
      <section class="glass-card upload-section">
        <h2>새 강의 업로드</h2>
        <form @submit.prevent="handleUpload" class="upload-form">
          <div class="form-group">
            <label>강의 제목</label>
            <input v-model="newLecture.title" type="text" class="glass-input" placeholder="예: 파이썬 기초 - 변수" required />
          </div>
          
          <div class="form-group">
            <label>동영상 URL (YouTube/S3)</label>
            <input v-model="newLecture.videoUrl" type="url" class="glass-input" placeholder="https://..." required />
          </div>
          
          <div class="form-group">
            <label>강의 설명</label>
            <textarea v-model="newLecture.description" class="glass-input" rows="3" placeholder="강의에 대한 간단한 설명을 입력하세요"></textarea>
          </div>

          <button type="submit" class="glass-button primary-btn" :disabled="isUploading">
            {{ isUploading ? '업로드 중...' : '강의 업로드' }}
          </button>
        </form>
      </section>

      <!-- Lecture List & AI Status -->
      <section class="glass-card list-section">
        <div class="section-header">
          <h2>내 강의 및 AI 분석 상태</h2>
          <button @click="fetchLectures" class="refresh-btn">
            🔄 새로고침
          </button>
        </div>

        <div v-if="lectures.length === 0" class="empty-state">
          업로드된 강의가 없습니다.
        </div>

        <div v-else class="lecture-list">
          <div v-for="lecture in lectures" :key="lecture.id" class="lecture-item">
            <div class="lecture-info">
              <h3>{{ lecture.title }}</h3>
              <p class="meta-text">{{ lecture.created_at }}</p>
            </div>
            
            <div class="ai-status">
              <span class="status-badge" :class="lecture.ai_status.toLowerCase()">
                {{ { 'PENDING': '대기중', 'PROCESSING': '분석중', 'COMPLETED': '완료', 'FAILED': '실패' }[lecture.ai_status] || lecture.ai_status }}
              </span>
              <div v-if="lecture.ai_status === 'FAILED'" class="error-msg">
                ⚠ {{ lecture.processing_error === 'Audio track missing' ? '오디오 트랙 없음' : lecture.processing_error }}
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const isUploading = ref(false)
const newLecture = ref({
  title: '',
  videoUrl: '',
  description: ''
})

// Mock Data for now
const lectures = ref([
  {
    id: 1,
    title: 'Python Basics - Variable',
    videoUrl: 'http://example.com/1',
    ai_status: 'COMPLETED',
    created_at: '2024-05-20'
  },
  {
    id: 2,
    title: 'Advanced AI Concepts',
    videoUrl: 'http://example.com/2',
    ai_status: 'PROCESSING',
    created_at: '2024-05-21'
  },
  {
    id: 3,
    title: 'Broken Video Test',
    videoUrl: 'http://example.com/3',
    ai_status: 'FAILED',
    processing_error: 'Audio track missing',
    created_at: '2024-05-22'
  }
])

const handleUpload = async () => {
  isUploading.value = true
  
  // Simulate API call
  setTimeout(() => {
    lectures.value.unshift({
      id: Date.now(),
      title: newLecture.value.title,
      videoUrl: newLecture.value.videoUrl,
      ai_status: 'PENDING',
      created_at: new Date().toISOString().split('T')[0]
    })
    
    newLecture.value = { title: '', videoUrl: '', description: '' }
    isUploading.value = false
    alert('강의가 업로드되었습니다! AI 분석이 시작됩니다.')
  }, 1000)
}

const fetchLectures = () => {
  // TODO: Fetch from backend API
  console.log('최신 강의 목록을 불러오는 중...')
}
</script>

<style scoped>
.dashboard-container {
  padding: 40px;
  max-width: 1200px;
  margin: 0 auto;
  color: white;
}

.page-title {
  font-size: 2rem;
  margin-bottom: 30px;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  padding-bottom: 10px;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: 30px;
}

@media (max-width: 900px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
}

.glass-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 25px;
  backdrop-filter: blur(10px);
}

.upload-section h2, .list-section h2 {
  font-size: 1.3rem;
  margin-bottom: 20px;
  color: #a5f3fc;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 0.9rem;
  color: #ddd;
}

.glass-input {
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(0, 0, 0, 0.2);
  color: white;
  font-size: 1rem;
}

.glass-input:focus {
  outline: none;
  border-color: #a5f3fc;
  background: rgba(0, 0, 0, 0.3);
}

.primary-btn {
  width: 100%;
  padding: 12px;
  background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%);
  border: none;
  border-radius: 8px;
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: transform 0.2s;
}

.primary-btn:hover {
  transform: translateY(-2px);
}

.primary-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* List Section */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.refresh-btn {
  background: transparent;
  border: 1px solid rgba(255,255,255,0.2);
  color: white;
  padding: 5px 10px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.8rem;
}

.refresh-btn:hover {
  background: rgba(255,255,255,0.1);
}

.lecture-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
  max-height: 500px;
  overflow-y: auto;
}

.lecture-item {
  background: rgba(255, 255, 255, 0.03);
  padding: 15px;
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background 0.2s;
}

.lecture-item:hover {
  background: rgba(255, 255, 255, 0.08);
}

.lecture-info h3 {
  font-size: 1rem;
  margin: 0 0 5px 0;
}

.meta-text {
  font-size: 0.8rem;
  color: #aaa;
  margin: 0;
}

.ai-status {
  text-align: right;
  min-width: 100px;
}

.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: bold;
}

.status-badge.completed {
  background: rgba(34, 197, 94, 0.2);
  color: #4ade80;
}

.status-badge.processing {
  background: rgba(234, 179, 8, 0.2);
  color: #facc15;
  animation: pulse 1.5s infinite;
}

.status-badge.pending {
  background: rgba(148, 163, 184, 0.2);
  color: #cbd5e1;
}

.status-badge.failed {
  background: rgba(239, 68, 68, 0.2);
  color: #f87171;
}

.error-msg {
  font-size: 0.7rem;
  color: #f87171;
  margin-top: 4px;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

/* Scrollbar for lecture list */
.lecture-list::-webkit-scrollbar {
  width: 6px;
}
.lecture-list::-webkit-scrollbar-track {
  background: rgba(255,255,255,0.05);
}
.lecture-list::-webkit-scrollbar-thumb {
  background: rgba(255,255,255,0.2);
  border-radius: 3px;
}
</style>
