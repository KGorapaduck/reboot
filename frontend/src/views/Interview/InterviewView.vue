<template>
  <div class="interview-container">
    <div v-if="!sessionActive" class="persona-selection">
        <h1>모의 면접 (Mock Interview)</h1>
        <p>원하는 면접관 페르소나를 선택하여 면접을 시작하세요.</p>
        
        <div class="persona-grid">
        <div v-for="persona in personas" :key="persona.id" class="glass-card persona-card">
            <h2>{{ persona.name }}</h2>
            <p class="role-badge">{{ persona.role }}</p>
            <p class="desc">{{ persona.description }}</p>
            <span class="difficulty" :class="persona.difficulty.toLowerCase()">{{ persona.difficulty }}</span>
            <button @click="startInterview(persona)" class="action-btn primary">면접 시작</button>
        </div>
        </div>
    </div>

    <div v-else class="chat-interface glass-card">
        <div class="chat-header">
            <div class="header-info">
                <h2>{{ currentPersona.name }}</h2>
                <span class="status-badge">면접 진행중</span>
            </div>
            <div class="timer">
                {{ formatTime(elapsedTime) }}
            </div>
            <button @click="endInterview" class="action-btn danger">면접 종료</button>
        </div>

        <div class="messages-area" ref="messagesContainer">
            <div v-for="msg in messages" :key="msg.id" class="message-row" :class="msg.sender.toLowerCase()">
                <div class="avatar">
                    {{ msg.sender === 'AI' ? '🤖' : '👤' }}
                </div>
                <div class="message-bubble">
                    {{ msg.content }}
                </div>
            </div>
        </div>

        <div class="input-area">
            <textarea 
                v-model="inputMessage" 
                @keydown.enter.prevent="sendMessage" 
                placeholder="답변을 입력하세요..."
                rows="2"
            ></textarea>
            <button @click="sendMessage" class="send-btn" :disabled="!inputMessage.trim()">전송</button>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'

// Mock Data
const personas = ref([
  { 
      id: 'tech_lead', 
      name: '깐깐한 기술 팀장', 
      role: 'TECH_LEAD', 
      difficulty: 'HARD',
      description: '깊이 있는 기술 질문과 꼬리물기 질문을 주로 합니다.'
  },
  { 
      id: 'hr_manager', 
      name: '온화한 인사 담당자', 
      role: 'HR', 
      difficulty: 'NORMAL',
      description: '인성, 협업 경험, 커리어 목표에 대해 물어봅니다.'
  },
  { 
      id: 'vc_investor', 
      name: '날카로운 VC 심사역', 
      role: 'VC', 
      difficulty: 'HARD',
      description: '사업성과 비즈니스 모델에 대해 집요하게 파고듭니다.'
  }
])

// State
const sessionActive = ref(false)
const currentPersona = ref(null)
const messages = ref([])
const inputMessage = ref('')
const elapsedTime = ref(0)
const messagesContainer = ref(null)
let timerInterval = null

// Methods
const startInterview = (persona) => {
    currentPersona.value = persona
    sessionActive.value = true
    messages.value = [
        { id: 1, sender: 'AI', content: `안녕하세요. ${persona.name}입니다. 지원자님의 포트폴리오를 잘 보았습니다. 간단한 자기소개 부탁드립니다.` }
    ]
    startTimer()
}

const sendMessage = () => {
    if(!inputMessage.value.trim()) return

    // User Message
    messages.value.push({
        id: Date.now(),
        sender: 'USER',
        content: inputMessage.value
    })

    const userText = inputMessage.value
    inputMessage.value = ''
    scrollToBottom()

    // AI Response Simulation
    setTimeout(() => {
        messages.value.push({
            id: Date.now() + 1,
            sender: 'AI',
            content: `"${userText}"에 대한 답변 잘 들었습니다. 다음 질문 드리겠습니다... (AI 생성 응답)`
        })
        scrollToBottom()
    }, 1500)
}

const endInterview = () => {
    clearInterval(timerInterval)
    if(confirm('면접을 종료하고 결과를 확인하시겠습니까?')) {
        sessionActive.value = false
        alert('면접이 종료되었습니다. 피드백 페이지로 이동합니다. (구현 예정)')
        elapsedTime.value = 0
    } else {
        startTimer()
    }
}

const startTimer = () => {
    timerInterval = setInterval(() => {
        elapsedTime.value++
    }, 1000)
}

const formatTime = (seconds) => {
    const m = Math.floor(seconds / 60).toString().padStart(2, '0')
    const s = (seconds % 60).toString().padStart(2, '0')
    return `${m}:${s}`
}

const scrollToBottom = () => {
    nextTick(() => {
        if(messagesContainer.value) {
            messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
        }
    })
}
</script>

<style scoped>
.interview-container {
  padding: 40px;
  max-width: 1000px;
  margin: 0 auto;
  color: #fff;
  height: calc(100vh - 80px);
  display: flex;
  flex-direction: column;
}

/* Persona Selection */
.persona-selection {
    text-align: center;
}

.persona-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
  margin-top: 40px;
}

.persona-card {
  background: rgba(28, 50, 106, 0.4);
  padding: 30px;
  border-radius: 12px;
  text-align: center;
  transition: transform 0.2s, background 0.2s;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.persona-card:hover {
  transform: translateY(-5px);
  background: rgba(28, 50, 106, 0.6);
}

.role-badge {
    background: rgba(255,255,255,0.1);
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.8rem;
    margin-bottom: 10px;
    color: #ccc;
}

.desc {
    font-size: 0.9rem;
    color: #ddd;
    margin-bottom: 20px;
    flex: 1;
}

.difficulty {
    display: inline-block;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 0.8rem;
    margin-bottom: 20px;
    font-weight: bold;
}
.difficulty.hard { color: #ff6b6b; background: rgba(255, 107, 107, 0.1); }
.difficulty.normal { color: #feca57; background: rgba(254, 202, 87, 0.1); }

/* Chat Interface */
.chat-interface {
    flex: 1;
    display: flex;
    flex-direction: column;
    background: rgba(20, 20, 30, 0.8);
    border-radius: 12px;
    overflow: hidden;
}

.chat-header {
    padding: 15px 25px;
    background: rgba(28, 50, 106, 0.5);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.header-info h2 {
    margin: 0;
    font-size: 1.2rem;
}

.status-badge {
    font-size: 0.8rem;
    color: #4caf50;
}

.timer {
    font-family: monospace;
    font-size: 1.2rem;
    font-weight: bold;
}

.messages-area {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.message-row {
    display: flex;
    gap: 15px;
    max-width: 80%;
}

.message-row.user {
    align-self: flex-end;
    flex-direction: row-reverse;
}

.avatar {
    width: 40px;
    height: 40px;
    background: rgba(255,255,255,0.1);
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 1.2rem;
}

.message-bubble {
    padding: 12px 18px;
    border-radius: 12px;
    line-height: 1.5;
    background: #333;
    color: #fff;
    white-space: pre-wrap;
}

.message-row.user .message-bubble {
    background: #3b82f6;
    color: white;
}

.input-area {
    padding: 20px;
    background: rgba(0,0,0,0.2);
    display: flex;
    gap: 15px;
    align-items: flex-end;
}

textarea {
    flex: 1;
    padding: 12px;
    border-radius: 8px;
    border: 1px solid #444;
    background: #222;
    color: white;
    resize: none;
    font-family: inherit;
}

.send-btn {
    padding: 10px 20px;
    height: 50px;
    background: #3b82f6;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: bold;
    cursor: pointer;
}

.send-btn:disabled {
    background: #555;
    cursor: not-allowed;
}

.action-btn {
    padding: 8px 16px;
    border-radius: 6px;
    border: none;
    cursor: pointer;
    font-weight: 600;
}

.primary { background: #3b82f6; color: white; }
.danger { background: #ff4757; color: white; }
</style>
