<template>
  <div class="mypage-container">
    <div class="glass-card profile-card">
        <div class="profile-header">
            <div class="avatar-large">{{ user.username[0].toUpperCase() }}</div>
            <div class="profile-info">
                <h1>{{ user.nickname }}</h1>
                <p class="email">{{ user.email }}</p>
                <span class="role-badge">{{ user.role }}</span>
            </div>
            <button class="action-btn secondary">프로필 편집</button>
        </div>
        
        <div class="stats-summary">
            <div class="stat-item">
                <span class="label">목표</span>
                <span class="value">{{ user.career_goal }}</span>
            </div>
            <div class="divider"></div>
            <div class="stat-item">
                <span class="label">학습일</span>
                <span class="value">42일</span>
            </div>
            <div class="divider"></div>
            <div class="stat-item">
                <span class="label">획득 스킬</span>
                <span class="value">{{ skills.length }}개</span>
            </div>
        </div>
    </div>

    <div class="skills-section">
        <h2>획득한 스킬 (Earned Skills)</h2>
        <div class="skills-grid">
            <div v-for="skill in skills" :key="skill.id" class="glass-card skill-card">
                <div class="skill-icon">🏆</div>
                <div class="skill-info">
                    <h3>{{ skill.name }}</h3>
                    <p class="date">Acquired: {{ formatDate(skill.acquired_at) }}</p>
                    <p class="source">{{ skill.verification_source }}</p>
                </div>
            </div>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const user = ref({
    username: 'student1',
    nickname: '열공러',
    email: 'student@reboot.com',
    role: 'STUDENT',
    career_goal: 'JOB_SEEKER' // 취업 준비
})

const skills = ref([
    { id: 1, name: 'Python Basics', acquired_at: '2023-10-10', verification_source: 'Quiz: Python 101' },
    { id: 2, name: 'Vue.js Fundamentals', acquired_at: '2023-10-25', verification_source: 'Project: Todo App' },
    { id: 3, name: 'REST API Design', acquired_at: '2023-10-30', verification_source: 'Quiz: API Design' }
])

const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString()
}
</script>

<style scoped>
.mypage-container {
  padding: 40px;
  max-width: 800px;
  margin: 0 auto;
  color: white;
}

.profile-card {
    padding: 40px;
    border-radius: 16px;
    background: rgba(28, 50, 106, 0.4);
    margin-bottom: 40px;
}

.profile-header {
    display: flex;
    align-items: center;
    gap: 30px;
    margin-bottom: 30px;
}

.avatar-large {
    width: 100px;
    height: 100px;
    background: linear-gradient(135deg, #3b82f6, #8b5cf6);
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 3rem;
    font-weight: bold;
    color: white;
}

.profile-info h1 {
    margin: 0 0 5px 0;
    font-size: 2rem;
}

.email {
    color: #aaa;
    margin: 0 0 10px 0;
}

.role-badge {
    background: #333;
    padding: 4px 10px;
    border-radius: 15px;
    font-size: 0.8rem;
}

.action-btn {
    margin-left: auto;
    padding: 8px 16px;
    border-radius: 6px;
    border: 1px solid rgba(255,255,255,0.2);
    background: rgba(255,255,255,0.05);
    color: white;
    cursor: pointer;
}

.stats-summary {
    display: flex;
    justify-content: space-around;
    background: rgba(0,0,0,0.2);
    padding: 20px;
    border-radius: 12px;
}

.stat-item {
    text-align: center;
}

.label {
    display: block;
    font-size: 0.9rem;
    color: #ccc;
    margin-bottom: 5px;
}

.value {
    font-size: 1.2rem;
    font-weight: bold;
}

.divider {
    width: 1px;
    background: rgba(255,255,255,0.1);
}

.skills-section h2 {
    margin-bottom: 20px;
}

.skills-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
}

.skill-card {
    display: flex;
    gap: 15px;
    padding: 20px;
    background: rgba(255,255,255,0.05);
    border-radius: 12px;
    align-items: center;
}

.skill-icon {
    font-size: 2rem;
}

.skill-info h3 {
    margin: 0 0 5px 0;
    font-size: 1rem;
}

.date {
    font-size: 0.8rem;
    color: #aaa;
    margin: 0;
}

.source {
    font-size: 0.75rem;
    color: #888;
    margin: 2px 0 0 0;
}
</style>
