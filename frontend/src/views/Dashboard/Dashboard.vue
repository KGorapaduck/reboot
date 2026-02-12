<template>
  <div class="dashboard-container">
    <!-- Welcome Section -->
    <section class="welcome-section">
      <h1 class="greeting">
        안녕하세요! <span class="username">{{ user.nickname || user.username }}님!</span> 👋
      </h1>
      <p class="subtitle">오늘도 목표를 향해 달려볼까요?</p>
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
          <span class="stat-value">{{ totalStudyTime }}분</span>
        </div>
      </div>

      <div class="glass-card stat-card">
        <div class="stat-icon-wrapper purple-icon">
          <!-- Book Icon -->
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
        </div>
        <div class="stat-info">
          <span class="stat-label">완료한 강의</span>
          <span class="stat-value">{{ completedLecturesCount }}개</span>
        </div>
      </div>

      <div class="glass-card stat-card">
        <div class="stat-icon-wrapper green-icon">
          <!-- Trophy Icon -->
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"></path><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"></path><path d="M4 22h16"></path><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"></path><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"></path><path d="M18 2H6v7a6 6 0 0 0 12 0V2z"></path></svg>
        </div>
        <div class="stat-info">
          <span class="stat-label">획득 스킬</span>
          <span class="stat-value">{{ earnedSkillsCount }}개</span>
        </div>
      </div>
    </section>

    <!-- Goals/Curriculum Section -->
    <section class="goals-section">
      <h2 class="section-title">내 커리큘럼 (My Curriculums)</h2>
      <div class="goals-grid" v-if="curriculums.length > 0">
        <div v-for="curr in curriculums" :key="curr.id" class="glass-card goal-card">
          <div class="quest-progress">
             <!-- Circular Progress Placeholder -->
            <div class="progress-circle" :style="{ background: `conic-gradient(#3b82f6 ${curr.progress}%, #333 0)` }">
              <span class="progress-text">{{ curr.progress }}%</span>
            </div>
            <div class="quest-details">
              <h3>{{ curr.course_title }}</h3>
              <p>{{ curr.status }} | 목표: {{ curr.target_date }}</p>
            </div>
          </div>
          <button class="action-btn white-btn" @click="resumeLearning(curr.course_id)">이어하기</button>
        </div>
      </div>
       <div v-else class="glass-card empty-state-card">
        <p class="empty-text">등록된 커리큘럼이 없습니다.</p>
        <button class="action-btn primary-btn">코스 찾기</button>
      </div>
    </section>

    <!-- Recent Activity Section -->
    <section class="recent-courses-section">
      <div class="section-header">
        <h2 class="section-title">최근 학습 강의</h2>
      </div>
      
      <div v-if="recentLectures.length > 0" class="recent-list">
        <div v-for="lecture in recentLectures" :key="lecture.id" class="glass-card lecture-card" @click="goToLecture(lecture.id)">
            <div class="lecture-info">
                <h3>{{ lecture.title }}</h3>
                <span class="course-name">{{ lecture.course_name }}</span>
            </div>
            <div class="play-icon">▶</div>
        </div>
      </div>

      <div v-else class="glass-card empty-state-card">
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

// Mock User Data based on ERD User & UserProfile
const user = ref({
    id: 1,
    username: 'student1',
    nickname: '열공러',
    role: 'STUDENT',
    career_goal: 'JOB_SEEKER'
})

// Mock Statistics
const totalStudyTime = ref(420) // minutes
const completedLecturesCount = ref(12)
const earnedSkillsCount = ref(3)

// Mock Curriculums based on ERD Curriculum & CurriculumItem
const curriculums = ref([
    {
        id: 101,
        course_id: 1,
        course_title: 'Full Stack Web Development',
        status: 'ACTIVE',
        target_date: '2023-12-31',
        progress: 45 // Calculated from CurriculumItems
    },
    {
        id: 102,
        course_id: 2,
        course_title: 'Python for Data Science',
        status: 'ACTIVE',
        target_date: '2024-01-15',
        progress: 10
    }
])

// Mock Recent Lectures based on Access History (or sorted CurriculumItems)
const recentLectures = ref([
    {
        id: 1001,
        course_name: 'Full Stack Web Development',
        title: 'Introduction to Vue.js',
        last_accessed: '2023-10-27T10:00:00'
    },
    {
        id: 2005,
        course_name: 'Python for Data Science',
        title: 'Pandas Basics',
        last_accessed: '2023-10-26T15:30:00'
    }
])

const resumeLearning = (courseId) => {
  // Logic to find the next unfinished lecture in the course
  console.log(`Resuming course ${courseId}`)
  router.push(`/classroom/${courseId}`) // Ideally redirect to specific lecture
}

const goToLecture = (lectureId) => {
    router.push(`/classroom?lectureId=${lectureId}`)
}

const startLearning = () => {
    // Navigate to course catalog or first course
    alert("코스 목록 페이지로 이동합니다. (구현 예정)")
}
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
  color: #050d18; /* Blue highlight via text-shadow or color? Adjusted for visibility */
  text-shadow: 0 0 10px rgba(59, 130, 246, 0.8);
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
  border-radius: 12px;
}

.stat-icon-wrapper {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 20px;
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
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 20px;
}

.goal-card {
  padding: 25px;
  background: rgba(28, 50, 106, 0.241);
  border-radius: 12px;
  min-height: 120px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid rgba(255, 255, 255, 0.1);
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
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 0.9rem;
  font-weight: bold;
  position: relative;
}

/* Inner circle for donut chart effect */
.progress-circle::before {
    content: "";
    position: absolute;
    width: 40px;
    height: 40px;
    background: #1e1e1e; /* Match card bg roughly or dark */
    border-radius: 50%;
}
.progress-text {
    position: relative;
    z-index: 1;
}

.quest-details h3 {
  font-size: 1rem;
  margin: 0 0 5px 0;
}

.quest-details p {
  font-size: 0.8rem;
  color: #aaa;
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

/* Recent Lectures */
.recent-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.lecture-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.2s;
}

.lecture-card:hover {
    background: rgba(255, 255, 255, 0.1);
}

.course-name {
    display: block;
    font-size: 0.8rem;
    color: #888;
    margin-top: 5px;
}

.empty-state-card {
  padding: 40px;
  text-align: center;
  background: rgba(28, 50, 106, 0.241);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 20px;
  border: 1px dashed rgba(255, 255, 255, 0.2);
  border-radius: 12px;
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
