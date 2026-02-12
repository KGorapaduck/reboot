<template>
  <div class="dashboard-container">
    <!-- Welcome Section -->
    <section class="welcome-section">
      <h1 class="greeting">
        안녕하세요! <span class="username">{{ username }}님!</span> 👋
      </h1>
      <p class="subtitle">오늘도 새로운 지식을 쌓아볼까요?</p>
    </section>

    <!-- Stats Grid -->
    <section class="stats-grid">
      <div class="glass-card stat-card">
        <div class="stat-icon-wrapper blue-icon">
          <!-- Clock Icon -->
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
        </div>
        <div class="stat-info">
          <span class="stat-label">총 학습 시간</span>
          <span class="stat-value">{{ studyTime }}분</span>
        </div>
      </div>

      <div class="glass-card stat-card">
        <div class="stat-icon-wrapper purple-icon">
          <!-- Book Icon -->
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
        </div>
        <div class="stat-info">
          <span class="stat-label">완료한 수업</span>
          <span class="stat-value">{{ completedClasses }}개</span>
        </div>
      </div>

      <div class="glass-card stat-card">
        <div class="stat-icon-wrapper green-icon">
          <!-- Trophy Icon -->
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"></path><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"></path><path d="M4 22h16"></path><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"></path><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"></path><path d="M18 2H6v7a6 6 0 0 0 12 0V2z"></path></svg>
        </div>
        <div class="stat-info">
          <span class="stat-label">최근 퀴즈 점수</span>
          <span class="stat-value">{{ quizScore }}점</span>
        </div>
      </div>
    </section>

    <!-- Goals Section -->
    <section class="goals-section">
      <h2 class="section-title">오늘의 목표</h2>
      <div class="goals-grid">
        <!-- Daily Quest Card -->
        <div class="glass-card goal-card quest-card">
          <div class="quest-progress">
            <div class="progress-circle">
              <span class="progress-text">0%</span>
            </div>
            <div class="quest-details">
              <h3>일일 퀘스트 진행중</h3>
              <p>0시간 / 6.3시간 (목표)</p>
            </div>
          </div>
          <button class="action-btn white-btn">이어서 하기</button>
        </div>

        <!-- Join Class Card -->
        <div class="glass-card goal-card join-card">
          <div class="join-content">
            <h3>🏫 클래스 참여하기</h3>
            <p>강사님께 전달받은 입장 코드를 입력하여<br>새로운 클래스에 참여하세요.</p>
          </div>
          <!-- Input could go here if interactive -->
        </div>
      </div>
    </section>

    <!-- Recent Courses Section -->
    <section class="recent-courses-section">
      <div class="section-header">
        <h2 class="section-title">최근 수강 목록</h2>
        <button class="view-all-btn">전체보기</button>
      </div>
      
      <div class="glass-card empty-state-card">
        <p class="empty-text">아직 학습 기록이 없습니다.</p>
        <button class="action-btn primary-btn" @click="startLearning">학습 시작하기</button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('testuser') // Mock data
const studyTime = ref(0)
const completedClasses = ref(0)
const quizScore = ref(0)

const startLearning = () => {
  router.push('/classroom')
}

// Ensure login check
onMounted(() => {
  // If we had a real backend, we'd fetch user data here
  const storedUser = localStorage.getItem('username') // Hypothetical
  if (storedUser) {
    // username.value = storedUser
  }
})
</script>

<style scoped>
.dashboard-container {
  padding: 40px;
  max-width: 1200px;
  margin: 0 auto;
  color: white;
  animation: fadeIn 0.5s ease-out;
}

/* Welcome Section */
.welcome-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 40px;
}

.greeting {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0;
}

.username {
  color: #050d18; /* Blue highlight */
}

.subtitle {
  color: rgba(255, 255, 255, 0.7);
  font-size: 1.1rem;
  margin-bottom: 5px;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 25px;
  background: rgba(28, 50, 106, 0.241); /* Darker background */
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.stat-icon-wrapper {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 20px;
  background: rgba(28, 50, 106, 0.241);
}

.blue-icon { color: #3b82f6; background: rgba(59, 130, 246, 0.1); }
.purple-icon { color: #a855f7; background: rgba(168, 85, 247, 0.1); }
.green-icon { color: #22c55e; background: rgba(34, 197, 94, 0.1); }

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-label {
  font-size: 0.9rem;
  color: #e5e7eb;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
}

/* Goals Section */
.goals-section {
  margin-bottom: 40px;
}

.section-title {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 20px;
  color: #e5e7eb;
}

.goals-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.goal-card {
  padding: 25px;
  background: rgba(28, 50, 106, 0.241);
  min-height: 120px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Quest Card Specifics */
.quest-card {
  display: flex;
  justify-content: space-between;
}

.quest-progress {
  display: flex;
  align-items: center;
  gap: 20px;
}

.progress-circle {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  border: 4px solid #333; /* Background ring */
  border-top-color: #3b82f6; /* Active ring mock */
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 0.9rem;
  font-weight: bold;
}

.quest-details h3 {
  font-size: 1rem;
  margin: 0 0 5px 0;
}

.quest-details p {
  font-size: 0.8rem;
  color: #e5e7eb;
  margin: 0;
}

/* Join Card Specifics */
.join-card {
  background: rgba(28, 50, 106, 0.241); /* Slight blue tint */
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.join-content h3 {
  font-size: 1rem;
  color: #93c5fd;
  margin: 0 0 8px 0;
}

.join-content p {
  font-size: 0.85rem;
  color: #dbeafe;
  line-height: 1.4;
  margin: 0;
}

/* Buttons */
.action-btn {
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.white-btn {
  background: white;
  color: #111;
}

.white-btn:hover {
  background: #f3f4f6;
}

.primary-btn {
  background: #3b82f6;
  color: white;
}

.primary-btn:hover {
  background: #2563eb;
}

.view-all-btn {
  background: rgba(28, 50, 106, 0.241);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 0.8rem;
  cursor: pointer;
}

.view-all-btn:hover {
  background: rgba(30, 58, 138, 0.2);
}

/* Recent Courses */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.empty-state-card {
  padding: 60px;
  text-align: center;
  background: rgba(28, 50, 106, 0.241);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 20px;
  border: 1px dashed rgba(255, 255, 255, 0.2);
}

.empty-text {
  color: #a4aab6;
  font-size: 1rem;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
