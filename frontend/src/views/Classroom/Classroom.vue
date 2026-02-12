<template>
  <div class="classroom-container">
    <!-- Top Navigation / Title -->
    <header class="class-header glass-card">
      <div class="header-left">
        <button class="icon-btn" @click="router.push('/dashboard')">←</button>
        <div>
          <h2 class="lecture-title">{{ currentLecture.title }}</h2>
          <span class="course-title">{{ currentCourse.title }}</span>
        </div>
      </div>
      <div class="header-right">
        <div class="progress-bar-container">
            <span class="progress-text">{{ currentCourse.progress }}% Completed</span>
            <div class="progress-bar">
                <div class="progress-fill" :style="{ width: currentCourse.progress + '%' }"></div>
            </div>
        </div>
      </div>
    </header>

    <div class="content-wrapper">
      <!-- Main Content: Video Player -->
      <main class="main-content glass-card">
        <div class="video-container">
           <!-- Placeholder for Youtube/Video Embed -->
           <iframe 
                v-if="currentLecture.video_url"
                width="100%" 
                height="100%" 
                :src="getEmbedUrl(currentLecture.video_url)" 
                title="YouTube video player" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                allowfullscreen>
            </iframe>
            <div v-else class="video-placeholder">
                <p>비디오를 불러오는 중입니다...</p>
            </div>
        </div>
        
        <div class="lecture-controls">
            <button class="action-btn" :class="{ 'completed': currentLecture.isCompleted }" @click="toggleComplete">
                {{ currentLecture.isCompleted ? '✅ 학습 완료' : '⭕ 학습 완료 체크' }}
            </button>
            <button class="action-btn secondary" @click="nextLecture">다음 강의 →</button>
        </div>
      </main>

      <!-- Sidebar: Tabs (Curriculum, AI Chat, Note) -->
      <aside class="sidebar glass-card">
         <div class="tabs">
            <button 
                v-for="tab in tabs" 
                :key="tab.id" 
                class="tab-btn" 
                :class="{ active: activeTab === tab.id }"
                @click="activeTab = tab.id"
            >
                {{ tab.label }}
            </button>
         </div>

         <div class="tab-content">
            
            <!-- Curriculum List -->
            <div v-if="activeTab === 'curriculum'" class="curriculum-list">
                <h3>강의 목차</h3>
                <ul>
                    <li v-for="item in curriculumItems" :key="item.id" 
                        class="curriculum-item" 
                        :class="{ active: item.id === currentLecture.id, completed: item.is_completed }"
                        @click="loadLecture(item.id)"
                    >
                        <span class="status-icon">{{ item.is_completed ? '✔' : (item.id === currentLecture.id ? '▶' : '•') }}</span>
                        <span class="item-title">{{ item.title }}</span>
                    </li>
                </ul>
            </div>

            <!-- AI Tutor Chat -->
            <div v-if="activeTab === 'chat'" class="chat-container">
                <div class="messages" ref="chatContainer">
                    <div v-for="msg in chatMessages" :key="msg.id" class="message" :class="msg.sender.toLowerCase()">
                        <div class="bubble">{{ msg.content }}</div>
                    </div>
                </div>
                <div class="input-area">
                    <input v-model="newMessage" @keyup.enter="sendMessage" placeholder="AI 튜터에게 질문하세요..." />
                    <button @click="sendMessage">Send</button>
                </div>
            </div>

            <!-- Lecture Note -->
            <div v-if="activeTab === 'note'" class="note-container">
                <h3>강의 핵심 요약</h3>
                <div class="ai-summary">
                    <p>{{ lectureNote.summary }}</p>
                </div>
                <div class="keywords">
                    <span v-for="kw in lectureNote.keywords" :key="kw" class="keyword-tag">#{{ kw }}</span>
                </div>
            </div>

         </div>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

// Mock Data
const currentCourse = ref({
    id: 1,
    title: 'Full Stack Web Development',
    progress: 45
})

const currentLecture = ref({
    id: 101,
    title: 'Vue.js Components Basics',
    video_url: 'https://www.youtube.com/watch?v=bzlFvd0b65c', // Placeholder URL
    isCompleted: false
})

const curriculumItems = ref([
    { id: 100, title: 'Introduction to Web', is_completed: true },
    { id: 101, title: 'Vue.js Components Basics', is_completed: false },
    { id: 102, title: 'State Management with Pinia', is_completed: false },
    { id: 103, title: 'Vue Router Navigation', is_completed: false },
])

const lectureNote = ref({
    summary: 'Vue.js 컴포넌트는 재사용 가능한 Vue 인스턴스입니다. Props를 통해 부모에서 자식으로 데이터를 전달하고, Emits를 통해 자식에서 부모로 이벤트를 보냅니다.',
    keywords: ['Component', 'Props', 'Emits', 'Reusability']
})

const chatMessages = ref([
    { id: 1, sender: 'AI', content: '안녕하세요! 이 강의에 대해 궁금한 점이 있으신가요?' }
])

// UI State
const tabs = [
    { id: 'curriculum', label: '목차' },
    { id: 'chat', label: 'AI 튜터' },
    { id: 'note', label: '노트' }
]
const activeTab = ref('curriculum')
const newMessage = ref('')

// Methods
const getEmbedUrl = (url) => {
    // Basic YouTube ID extractor for demo
    if (!url) return ''
    const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
    const match = url.match(regExp);
    return (match && match[2].length === 11) ? 'https://www.youtube.com/embed/' + match[2] : url;
}

const toggleComplete = () => {
    currentLecture.value.isCompleted = !currentLecture.value.isCompleted
    // Update curriculum item status in real app
}

const nextLecture = () => {
    // Logic to find next id
    alert("다음 강의로 이동합니다.")
}

const loadLecture = (id) => {
    // In real app, fetch lecture detail by id
    console.log(`Load lecture ${id}`)
    currentLecture.value.title = curriculumItems.value.find(i => i.id === id).title
    currentLecture.value.id = id
}

const sendMessage = () => {
    if (!newMessage.value.trim()) return
    // Add user message
    chatMessages.value.push({ id: Date.now(), sender: 'USER', content: newMessage.value })
    
    // Simulate AI response
    setTimeout(() => {
        chatMessages.value.push({ 
            id: Date.now() + 1, 
            sender: 'AI', 
            content: `"${newMessage.value}"에 대한 답변입니다. (RAG 검색 결과 표시 예정)` 
        })
    }, 1000)
    
    newMessage.value = ''
}
</script>

<style scoped>
.classroom-container {
    height: calc(100vh - 80px); /* Adjust based on navbar height */
    display: flex;
    flex-direction: column;
    padding: 20px;
    gap: 20px;
    color: white;
}

/* Header */
.class-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 25px;
    background: rgba(28, 50, 106, 0.4);
    border-radius: 12px;
}

.header-left {
    display: flex;
    gap: 15px;
    align-items: center;
}

.icon-btn {
    background: none;
    border: none;
    color: white;
    font-size: 1.5rem;
    cursor: pointer;
}

.lecture-title {
    margin: 0;
    font-size: 1.2rem;
}

.course-title {
    font-size: 0.8rem;
    color: #aaa;
}

.progress-bar-container {
    width: 200px;
    text-align: right;
}

.progress-text {
    font-size: 0.8rem;
    color: #ccc;
    margin-bottom: 5px;
    display: block;
}

.progress-bar {
    height: 8px;
    background: #333;
    border-radius: 4px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: #4caf50;
    transition: width 0.3s;
}

/* Content Layout */
.content-wrapper {
    display: flex;
    flex: 1;
    gap: 20px;
    overflow: hidden; /* Prevent body scroll */
}

/* Main Video Area */
.main-content {
    flex: 2;
    display: flex;
    flex-direction: column;
    background: rgba(20, 20, 30, 0.8);
    border-radius: 12px;
    padding: 20px;
}

.video-container {
    flex: 1;
    background: black;
    border-radius: 8px;
    overflow: hidden;
    position: relative;
}

.video-placeholder {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    color: #555;
}

.lecture-controls {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
}

.action-btn {
    padding: 10px 20px;
    border-radius: 6px;
    border: none;
    cursor: pointer;
    font-weight: bold;
    background: #333;
    color: white;
}

.action-btn.completed {
    background: #4caf50;
}

.action-btn.secondary {
    background: #007bff;
}

/* Sidebar */
.sidebar {
    flex: 1;
    background: rgba(28, 50, 106, 0.4);
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    min-width: 300px;
}

.tabs {
    display: flex;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}

.tab-btn {
    flex: 1;
    background: none;
    border: none;
    padding: 15px;
    color: #aaa;
    cursor: pointer;
    font-weight: bold;
}

.tab-btn.active {
    color: white;
    border-bottom: 2px solid #007bff;
    background: rgba(255,255,255,0.05);
}

.tab-content {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
}

/* Curriculum List */
.curriculum-list ul {
    list-style: none;
    padding: 0;
}

.curriculum-item {
    padding: 10px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    cursor: pointer;
    display: flex;
    gap: 10px;
    align-items: center;
}

.curriculum-item:hover, .curriculum-item.active {
    background: rgba(255,255,255,0.1);
}

.status-icon {
    width: 20px;
    text-align: center;
}

.item-title {
    font-size: 0.95rem;
}

/* Chat */
.chat-container {
    display: flex;
    flex-direction: column;
    height: 100%;
}

.messages {
    flex: 1;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding-bottom: 10px;
}

.message {
    max-width: 80%;
    padding: 10px;
    border-radius: 8px;
    font-size: 0.9rem;
}

.message.ai {
    align-self: flex-start;
    background: #333;
    color: #eee;
}

.message.user {
    align-self: flex-end;
    background: #007bff;
    color: white;
}

.input-area {
    display: flex;
    gap: 10px;
    margin-top: 10px;
}

.input-area input {
    flex: 1;
    padding: 10px;
    border-radius: 4px;
    border: 1px solid #444;
    background: #222;
    color: white;
}

.input-area button {
    padding: 10px 15px;
    background: #007bff;
    border: none;
    border-radius: 4px;
    color: white;
    cursor: pointer;
}

/* Note */
.ai-summary {
    background: rgba(255,255,0,0.1);
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 20px;
    line-height: 1.5;
}

.keyword-tag {
    display: inline-block;
    background: #444;
    padding: 5px 10px;
    border-radius: 15px;
    font-size: 0.8rem;
    margin-right: 5px;
    margin-bottom: 5px;
}
</style>
