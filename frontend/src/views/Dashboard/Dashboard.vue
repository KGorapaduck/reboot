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

    <!-- Learning Diagnosis Section (New) -->
    <section class="diagnosis-section">
      <h2 class="section-title">학습 진단 리포트 (Beta)</h2>
      <div class="diagnosis-grid">
        <!-- Cohort Comparison -->
        <div class="glass-card diagnosis-card">
          <h3>나의 위치</h3>
          <p class="desc">수강생 평균 대비 진도율</p>
          <div class="comparison-chart">
            <div class="bar-group">
              <span class="label">나 ({{ activeCurriculum.progress }}%)</span>
              <div class="bar-bg"><div class="bar-fill my-bar" :style="{ width: `${activeCurriculum.progress}%` }"></div></div>
            </div>
            <div class="bar-group">
              <span class="label">평균 ({{ cohortStats.avg_progress }}%)</span>
              <div class="bar-bg"><div class="bar-fill avg-bar" :style="{ width: `${cohortStats.avg_progress}%` }"></div></div>
            </div>
          </div>
          <p class="insight">{{ progressInsight }}</p>
        </div>

        <!-- Retention / Risk Analysis -->
        <div class="glass-card diagnosis-card">
          <h3>이탈 위험도 분석</h3>
          <div class="risk-meter">
            <div class="risk-circle" :class="retentionMetrics.riskLevel">
              <span>{{ retentionMetrics.dropout_risk_score * 100 }}%</span>
            </div>
            <div class="risk-info">
              <p>현재 <strong>{{ riskLabel }}</strong> 상태입니다.</p>
              <p class="suggestion">{{ riskSuggestion }}</p>
            </div>
          </div>
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
                <span class="last-accessed">{{ new Date(lecture.last_accessed).toLocaleDateString() }}</span>
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
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../api/axios'

const router = useRouter()

// Data refs
const user = ref({})
const totalStudyTime = ref(0)
const completedLecturesCount = ref(0)
const earnedSkillsCount = ref(0)
const curriculums = ref([])
const recentLectures = ref([])

// Advanced Analytics Data
const cohortStats = ref({ avg_progress: 0, avg_quiz_score: 0 })
const retentionMetrics = ref({ dropout_risk_score: 0, riskLevel: 'low', quiz_fail_streak: 0 })

const riskLabel = computed(() => {
    const score = retentionMetrics.value.dropout_risk_score * 100
    if (score > 70) return '위험'
    if (score > 30) return '주의'
    return '안전'
})

const riskSuggestion = computed(() => {
    const score = retentionMetrics.value.dropout_risk_score * 100
    if (score > 70) return '상담을 신청하거나 복습이 필요합니다!'
    if (score > 30) return '조금 더 집중해서 강의를 들어보세요.'
    return '현재 아주 잘하고 계십니다! 🚀'
})

const loading = ref(true)
const error = ref(null)

// API Fetch
const fetchDashboardData = async () => {
    try {
        loading.value = true
        // Assuming backend runs on port 8000. Setup vite proxy or absolute URL for now.
        const response = await api.get('/dashboard/')
        const data = response.data
        
        user.value = data.user
        totalStudyTime.value = data.stats.total_study_time
        completedLecturesCount.value = data.stats.completed_lectures_count
        earnedSkillsCount.value = data.stats.earned_skills_count
        curriculums.value = data.curriculums
        recentLectures.value = data.recent_lectures
        
        // Extract cohort stats & retention from first curriculum for demo
        if (data.curriculums.length > 0) {
            cohortStats.value = data.curriculums[0].cohort_analytics || { avg_progress: 0 }
            retentionMetrics.value = data.curriculums[0].retention_metrics || { dropout_risk_score: 0 }
        }
    } catch (err) {
        console.error("Dashboard fetch error:", err)
        error.value = "데이터를 불러오는 데 실패했습니다."
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    fetchDashboardData()
})

const activeCurriculum = computed(() => curriculums.value[0] || { progress: 0 })

const progressInsight = computed(() => {
    if (!activeCurriculum.value) return "로딩 중..."
    const diff = activeCurriculum.value.progress - cohortStats.value.avg_progress
    if (diff > 10) return "훌륭합니다! 평균보다 앞서가고 있어요. 🚀"
    if (diff < -10) return "조금 뒤쳐져 있지만, 꾸준히 하면 따라잡을 수 있어요! 💪"
    return "평균적인 속도로 잘 진행하고 있습니다. 👌"
})


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

/* Diagnosis Section */
.diagnosis-section {
    margin-bottom: 40px;
}

.diagnosis-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
}

.diagnosis-card {
    padding: 25px;
    background: rgba(28, 50, 106, 0.241);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
}

.diagnosis-card h3 {
    margin: 0 0 10px 0;
    font-size: 1.1rem;
}

.diagnosis-card .desc {
    font-size: 0.9rem;
    color: #ccc;
    margin-bottom: 20px;
}

.comparison-chart {
    display: flex;
    flex-direction: column;
    gap: 15px;
    margin-bottom: 15px;
}

.bar-group {
    display: flex;
    align-items: center;
    gap: 10px;
}

.bar-group .label {
    width: 80px;
    font-size: 0.9rem;
}

.bar-bg {
    flex: 1;
    height: 10px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 5px;
    overflow: hidden;
}

.bar-fill {
    height: 100%;
    border-radius: 5px;
}

.my-bar { background: #3b82f6; }
.avg-bar { background: #9ca3af; }

.insight {
    font-size: 0.9rem;
    color: #a7f3d0;
    margin-top: 10px;
}

.risk-meter {
    display: flex;
    align-items: center;
    gap: 20px;
}

.risk-circle {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 1.2rem;
    font-weight: bold;
    border: 5px solid;
}

.risk-circle.low { border-color: #22c55e; color: #22c55e; }
.risk-circle.medium { border-color: #eab308; color: #eab308; }
.risk-circle.high { border-color: #ef4444; color: #ef4444; }

.risk-info p {
    margin: 5px 0;
}

.suggestion {
    font-size: 0.9rem;
    color: #ccc;
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
