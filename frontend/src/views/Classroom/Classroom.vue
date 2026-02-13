<template>
  <div class="classroom-container">
    <!-- Top Navigation / Title -->
    <header class="class-header glass-card">
      <div class="header-left">
        <button class="icon-btn" @click="router.push('/dashboard')">←</button>
        <div>
          <h2 class="lecture-title">{{ isLiveMode ? '현장 강의 실시간 중계' : currentLecture.title }}</h2>
          <span class="course-title">{{ isLiveMode ? '실시간 마이크 연동 중' : currentCourse.title }}</span>
        </div>
      </div>
      <div class="header-right">
        <div class="progress-bar-container">
            <template v-if="isLiveMode">
              <span class="live-indicator">● LIVE</span>
            </template>
            <template v-else>
              <span class="progress-text">{{ currentLecture.ai_status === 'COMPLETED' ? 'AI 분석 완료' : 'AI 분석 중...' }}</span>
              <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: (currentLecture.ai_status === 'COMPLETED' ? 100 : 50) + '%' }"></div>
              </div>
            </template>
        </div>
      </div>
    </header>

    <div class="content-wrapper">
      <!-- Main Content: Video/Mic Area -->
      <main class="main-content glass-card">
        <div class="video-container">
            <!-- YouTube Case -->
            <div v-show="!isLiveMode" id="youtube-player" style="width: 100%; height: 100%;"></div>
            
            <!-- Live Mic Case -->
            <div v-if="isLiveMode" class="live-mic-container">
                <div class="mic-visualizer">
                    <div class="pulse-ring" :class="{ 'pulsing': isListening }"></div>
                    <div class="mic-icon" :class="{ 'active': isListening }">🎙️</div>
                </div>
                <h3>{{ isListening ? '강의 내용을 경청하고 있습니다...' : '마이크가 정지되었습니다' }}</h3>
                <p>교수님의 음성이 실시간으로 자막으로 변환됩니다.</p>
                <div class="stt-status">
                  <span :class="{ 'status-on': isListening }">{{ isListening ? '마이크 작동 중' : '마이크 준비 중' }}</span>
                </div>
            </div>

            <!-- Loading Placeholder -->
            <div v-if="!isLiveMode && !isPlayerReady" class="video-placeholder">
                <div v-if="!lectureLoadError" class="loader"></div>
                <p v-if="lectureLoadError" class="error-text">{{ lectureLoadError }}</p>
                <p v-else>{{ !currentLecture.video_url ? '강의 정보를 불러오는 중...' : '비디오를 준비하고 있습니다...' }}</p>
                <span v-if="!lectureLoadError && currentLecture.ai_status === 'PROCESSING'" class="processing-hint">AI 분석도 동시에 진행 중입니다. 잠시만 기다려주세요.</span>
            </div>
        </div>
        
        <div class="lecture-controls">
            <button class="action-btn" :class="{ 'completed': isCompleted }" @click="toggleComplete">
                {{ isCompleted ? '✅ 학습 완료' : '⭕ 학습 완료 체크' }}
            </button>
            <button v-if="isLiveMode" class="action-btn" :class="{ 'listening': isListening }" @click="toggleListening">
                {{ isListening ? '🔇 마이크 중지' : '🎙️ 마이크 시작' }}
            </button>
            <div v-else class="youtube-actions">
              <button class="action-btn" :class="{ 'listening': isListening }" @click="toggleListening" style="margin-right: 10px;">
                {{ isListening ? '🔇 실시간 Whisper 끄기' : '🎙️ 실시간 Whisper 켜기' }}
              </button>
              <div v-if="isTranscribing" class="transcribing-batch">AI 분석 중...</div>
              <button class="action-btn secondary" @click="nextLecture">다음 강의 →</button>
            </div>
        </div>
      </main>

      <!-- Sidebar: Tabs -->
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
            
            <!-- Live Script (강의 탭) -->
            <div v-if="activeTab === 'script'" class="script-list">
                <div 
                  v-for="(seg, idx) in lectureScript" 
                  :key="idx" 
                  class="script-segment"
                  :class="{ active: currentSegmentIndex === idx, 'live-seg': isLiveMode }"
                  @click="!isLiveMode && seekTo(seg.start)"
                  :ref="el => { if (currentSegmentIndex === idx) activeSegmentRef = el }"
                >
                  <span class="timestamp">{{ formatTime(seg.start) }}</span>
                  <p class="content">{{ seg.content }}</p>
                </div>
                <div v-if="!lectureScript.length" class="empty-state">
                  {{ isListening ? '영상의 소리를 분석하여 자막을 생성하고 있습니다 (약 10~20초 소요)...' : '실시간 Whisper를 켜서 영상 자막을 확인해 보세요.' }}
                </div>
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
                    <button @click="sendMessage">전송</button>
                </div>
            </div>

            <!-- Lecture Note (요약본) -->
            <div v-if="activeTab === 'note'" class="note-container">
                <h3>강의 핵심 요약</h3>
                <div v-if="currentLecture.original_script" class="ai-summary markdown-body">
                    {{ currentLecture.original_script }}
                </div>
                <div v-else class="empty-state">
                    {{ isLiveMode ? '강의가 종료된 후 요약본이 생성됩니다.' : '생성된 요약본이 없습니다.' }}
                </div>
            </div>

         </div>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '../../api/axios'

const router = useRouter()
const route = useRoute()

// Mode State
const isLiveMode = computed(() => route.query.mode === 'live')
const youtubeUrlFromQuery = computed(() => route.query.youtube_url)

// Data State
const currentCourse = ref({ title: '로딩 중...' })
const currentLecture = ref({ script_segments: [], video_url: '' })
const lectureLoadError = ref('')
const liveSegments = ref([]) // For live STT
const isCompleted = ref(false)
const chatMessages = ref([
    { id: 1, sender: 'AI', content: '안녕하세요! 실시간 강의 중 궁금한 점이 생기면 물어보세요.' }
])
// Reverted: Removed liveSummary and liveTextBuffer for real-time display focus

const lectureScript = computed(() => {
  const backendSegments = currentLecture.value.script_segments || []
  const allSegments = [...backendSegments, ...liveSegments.value]
  
  // Sort by start time to handle hybrid view
  return allSegments.sort((a, b) => a.start - b.start)
})

// UI State
const tabs = [
    { id: 'script', label: '강의' },
    { id: 'chat', label: 'AI 튜터' },
    { id: 'note', label: '노트' }
]
const activeTab = ref('script')
const newMessage = ref('')
const currentSegmentIndex = ref(-1)
const activeSegmentRef = ref(null)
const isYoutubeInitialized = ref(false)

// Real-time Whisper STT Logic (Chunked)
let mediaRecorder = null
let audioChunks = []
const isListening = ref(false)
let chunkInterval = null
const isTranscribing = ref(false)
let pollingInterval = null
const isPlayerReady = ref(false)

const startRecordingChunks = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    mediaRecorder = new MediaRecorder(stream)
    
    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        uploadAudioSegment(event.data)
      }
    }

    mediaRecorder.start()
    isListening.value = true

    // Stop and restart every 10 seconds to create chunks
    chunkInterval = setInterval(() => {
        if (mediaRecorder && mediaRecorder.state === 'recording') {
            mediaRecorder.stop()
            mediaRecorder.start()
        }
    }, 10000)

  } catch (err) {
    console.error("Error accessing microphone:", err)
    alert("마이크 접근 권한이 필요합니다.")
  }
}

const stopRecordingChunks = () => {
  if (mediaRecorder) {
    mediaRecorder.stop()
    mediaRecorder.stream.getTracks().forEach(track => track.stop())
  }
  if (chunkInterval) clearInterval(chunkInterval)
  isListening.value = false
}

const uploadAudioSegment = async (blob) => {
  const formData = new FormData()
  formData.append('audio', blob, 'segment.webm')
  
  isTranscribing.value = true
  try {
    const response = await api.post(`/lectures/${currentLecture.value.id}/transcribe_segment/`, formData)
    const text = response.data.text
    if (text && text.trim()) {
      const timestamp = player && player.getCurrentTime ? player.getCurrentTime() : 0
      liveSegments.value.push({
        start: timestamp,
        content: text.trim()
      })
      scrollToActiveSegment()
    }
  } catch (error) {
    console.error("Transcription chunk failed:", error)
  } finally {
    isTranscribing.value = false
  }
}

const requestMicPermission = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    // We just want to ensure permission is granted, so we stop the stream immediately
    stream.getTracks().forEach(track => track.stop())
    console.log("Classroom: Microphone permission granted.")
  } catch (err) {
    console.warn("Classroom: Microphone permission denied or not available.", err)
  }
}

const toggleListening = () => {
  if (isLiveMode.value) {
    if (isListening.value) {
      stopRecordingChunks()
    } else {
      startRecordingChunks()
    }
  } else {
    // YouTube Multi-mode STT: Just trigger/ensure polling is active
    if (!isListening.value) {
        isListening.value = true
        startPolling()
    } else {
        isListening.value = false
    }
  }
}

// YouTube Player Logic
let player = null
let timeTracker = null

const fetchLectureData = async () => {
    if (isLiveMode.value) return

    const lectureId = route.params.id || route.query.lectureId
    const targetUrl = route.query.youtube_url || route.query.youtubeUrl
    
    console.log("Classroom: Route Query received:", route.query)
    console.log("Classroom: Fetching data...", { lectureId, targetUrl })
    lectureLoadError.value = ''

    try {
        let response
        if (targetUrl) {
            console.log("Classroom: Calling get_by_url for", targetUrl)
            response = await api.post('/lectures/get_by_url/', { video_url: targetUrl })
            currentLecture.value = response.data
            console.log("Classroom: URL match result:", response.data)
            
            if (currentLecture.value.ai_status !== 'COMPLETED') {
                startPolling()
            }
        } else if (lectureId) {
            console.log("Classroom: Calling get by ID", lectureId)
            response = await api.get(`/lectures/${lectureId}/`)
            currentLecture.value = response.data
        } else {
            console.warn("Classroom: No lecture ID or URL provided")
        }

        if (currentLecture.value) {
            console.log("Classroom: Lecture data loaded successfully:", JSON.stringify(currentLecture.value, null, 2))
            if (currentLecture.value.course_name) {
                currentCourse.value.title = currentLecture.value.course_name
            }
            if (currentLecture.value.video_url) {
                console.log("Classroom: Video URL found, initializing player:", currentLecture.value.video_url)
                initYoutubePlayer(currentLecture.value.video_url)
            } else {
                console.warn("Classroom: CRITICAL - Lecture found but video_url is missing in response!", currentLecture.value)
                lectureLoadError.value = '강의 비디오 정보를 찾을 수 없습니다.'
            }
        }
    } catch (error) {
        console.error("Classroom: Failed to fetch lecture:", error)
        lectureLoadError.value = '강의 정보를 불러오는 데 실패했습니다. 네트워크 상태를 확인해 주세요.'
    }
}

const stopPolling = () => {
    if (pollingInterval) {
        clearInterval(pollingInterval)
        pollingInterval = null
    }
}

// Watch for isListening and ai_status to adjust polling
watch([isListening, () => currentLecture.value.ai_status], ([listening, status]) => {
    if (listening || status === 'PROCESSING') {
        stopPolling()
        startPolling(2000) // Poll every 2s for real-time feel
    } else if (status === 'COMPLETED') {
        stopPolling()
    }
})

const startPolling = (ms = 5000) => {
    if (pollingInterval) stopPolling()
    pollingInterval = setInterval(async () => {
        try {
            const response = await api.get(`/lectures/${currentLecture.value.id}/`)
            // Only update if data changed (more segments)
            if (response.data.script_segments?.length !== currentLecture.value.script_segments?.length) {
                currentLecture.value = response.data
            }
            if (currentLecture.value.ai_status === 'COMPLETED') {
                stopPolling()
            }
        } catch (error) {
            console.error("Polling error:", error)
            stopPolling()
        }
    }, ms)
}

// YouTube IDs and initialization logic below
const extractYoutubeId = (url) => {
    if (!url) return null
    // Support all common YouTube URL formats
    const patterns = [
        /(?:v=|\/)([0-9A-Za-z_-]{11}).*/,
        /youtu\.be\/([0-9A-Za-z_-]{11})/,
        /embed\/([0-9A-Za-z_-]{11})/
    ]
    for (const pattern of patterns) {
        const match = url.match(pattern)
        if (match && match[1]) return match[1]
    }
    return null
}

const initYoutubePlayer = (videoUrl) => {
    const videoId = extractYoutubeId(videoUrl)
    if (!videoId) {
        console.error("Invalid YouTube ID extracted from:", videoUrl)
        return
    }

    if (player && player.videoId === videoId && isPlayerReady.value) return

    // If API ready, initialize
    const createPlayer = () => {
        if (player && typeof player.destroy === 'function') {
            try { player.destroy() } catch(e) {}
        }

        player = new window.YT.Player('youtube-player', {
            height: '100%',
            width: '100%',
            videoId: videoId,
            playerVars: {
              'autoplay': 0,
              'modestbranding': 1,
              'rel': 0
            },
            events: {
                'onReady': (event) => {
                    isPlayerReady.value = true
                    isYoutubeInitialized.value = true
                    player.videoId = videoId
                },
                'onStateChange': onPlayerStateChange,
                'onError': (e) => {
                    console.error("YouTube Player Error:", e.data)
                    alert("비디오를 재생할 수 없습니다. URL을 확인해 주세요.")
                }
            }
        })
    }

    if (window.YT && window.YT.Player) {
        createPlayer()
    } else {
        // Load script if not present
        if (!document.getElementById('youtube-api-script')) {
            const tag = document.createElement('script')
            tag.id = 'youtube-api-script'
            tag.src = "https://www.youtube.com/iframe_api"
            const firstScriptTag = document.getElementsByTagName('script')[0]
            firstScriptTag.parentNode.insertBefore(tag, firstScriptTag)
        }
        
        // Wait for API
        const checkYoutubeApi = setInterval(() => {
            if (window.YT && window.YT.Player) {
                clearInterval(checkYoutubeApi)
                createPlayer()
            }
        }, 100)
        
        // Timeout after 10s
        setTimeout(() => clearInterval(checkYoutubeApi), 10000)
    }
}

// Watch for route changes to re-fetch data if component is reused
watch(() => route.fullPath, () => {
    stopPolling()
    stopTimeTracking()
    fetchLectureData()
})

const onPlayerStateChange = (event) => {
    if (event.data === window.YT.PlayerState.PLAYING) {
        startTimeTracking()
        // Auto-start STT functionality on play for YouTube mode
        if (!isLiveMode.value && !isListening.value) {
            isListening.value = true
        }
    } else {
        stopTimeTracking()
    }
}

const startTimeTracking = () => {
    stopTimeTracking()
    timeTracker = setInterval(() => {
        if (player && player.getCurrentTime) {
            const currentTime = player.getCurrentTime()
            updateActiveSegment(currentTime)
        }
    }, 500)
}

const stopTimeTracking = () => {
    if (timeTracker) clearInterval(timeTracker)
}

const updateActiveSegment = (time) => {
    const segments = currentLecture.value.script_segments
    if (!segments) return

    const index = segments.findIndex((seg, idx) => {
        const nextStart = segments[idx + 1] ? segments[idx + 1].start : Infinity
        return time >= seg.start && time < nextStart
    })

    if (index !== -1 && index !== currentSegmentIndex.value) {
        currentSegmentIndex.value = index
        scrollToActiveSegment()
    }
}

const scrollToActiveSegment = () => {
    nextTick(() => {
        if (activeSegmentRef.value) {
            activeSegmentRef.value.scrollIntoView({ behavior: 'smooth', block: 'center' })
        }
    })
}

const seekTo = (seconds) => {
    if (player && player.seekTo) {
        player.seekTo(seconds, true)
        player.playVideo()
    }
}

const formatTime = (seconds) => {
    if (!seconds && seconds !== 0) return '0:00'
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${secs.toString().padStart(2, '0')}`
}

const toggleComplete = () => {
    isCompleted.value = !isCompleted.value
}

const nextLecture = () => {
  alert("다음 강의로 이동합니다.")
}

const sendMessage = () => {
    if (!newMessage.value.trim()) return
    chatMessages.value.push({ id: Date.now(), sender: 'USER', content: newMessage.value })
    
    setTimeout(() => {
        chatMessages.value.push({ 
            id: Date.now() + 1, 
            sender: 'AI', 
            content: `"${newMessage.value}"에 대해 분석된 데이터 기반으로 답변을 준비 중입니다.` 
        })
    }, 1000)
    
    newMessage.value = ''
}

onMounted(() => {
    fetchLectureData()
    if (isLiveMode.value) {
      startRecordingChunks()
    }
})

onUnmounted(() => {
    stopTimeTracking()
    stopPolling()
    stopRecordingChunks()
})
</script>

<style scoped>
.classroom-container {
    height: calc(100vh - 80px);
    display: flex;
    flex-direction: column;
    padding: 20px;
    gap: 20px;
    color: white;
}

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

.live-indicator {
    color: #ef4444;
    font-weight: bold;
    animation: blink 1s infinite;
}

@keyframes blink {
    50% { opacity: 0.3; }
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

.content-wrapper {
    display: flex;
    flex: 1;
    gap: 20px;
    overflow: hidden;
}

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
    display: flex;
    justify-content: center;
    align-items: center;
}

.video-placeholder {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.9);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    z-index: 10;
    text-align: center;
    gap: 15px;
}

.loader {
    width: 40px;
    height: 40px;
    border: 3px solid rgba(255, 255, 255, 0.1);
    border-radius: 50%;
    border-top-color: #3b82f6;
    animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

.processing-hint {
    font-size: 0.8rem;
    color: #3b82f6;
    opacity: 0.8;
}

.transcribing-batch {
    display: inline-block;
    font-size: 0.8rem;
    color: #3b82f6;
    margin-right: 10px;
    animation: pulse 1.5s infinite;
}

.error-text {
    color: #ef4444;
    font-weight: bold;
}

/* Live Mic UI */
.live-mic-container {
    text-align: center;
    animation: fadeIn 0.5s ease-out;
}

.mic-visualizer {
    position: relative;
    width: 120px;
    height: 120px;
    margin: 0 auto 20px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.mic-icon {
    font-size: 4rem;
    z-index: 2;
    transition: transform 0.3s;
}

.mic-icon.active {
    transform: scale(1.1);
}

.pulse-ring {
    position: absolute;
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background: rgba(59, 130, 246, 0.3);
    z-index: 1;
}

.pulse-ring.pulsing {
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { transform: scale(1); opacity: 0.5; }
    100% { transform: scale(1.8); opacity: 0; }
}

.stt-status {
    margin-top: 15px;
    font-size: 0.9rem;
    color: #666;
}

.status-on {
    color: #3b82f6;
    font-weight: bold;
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

.action-btn.listening {
    background: #ef4444;
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
    min-width: 350px;
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

/* Script List */
.script-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.script-segment {
    padding: 12px;
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.03);
    cursor: pointer;
    transition: all 0.3s;
    border: 1px solid transparent;
}

.script-segment:hover {
    background: rgba(255, 255, 255, 0.08);
}

.script-segment.active {
    background: rgba(59, 130, 246, 0.15);
    border-color: rgba(59, 130, 246, 0.4);
}

.timestamp {
    font-size: 0.75rem;
    color: #3b82f6;
    font-weight: bold;
}

.script-segment .content {
    margin: 5px 0 0 0;
    font-size: 0.95rem;
    line-height: 1.5;
    color: #eee;
}

.script-segment.active .content {
    color: white;
    font-weight: 500;
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
}

.message {
    max-width: 85%;
    padding: 10px;
    border-radius: 12px;
    font-size: 0.9rem;
}

.message.ai {
    align-self: flex-start;
    background: rgba(255, 255, 255, 0.1);
}

.message.user {
    align-self: flex-end;
    background: #3b82f6;
}

.input-area {
    display: flex;
    gap: 10px;
    margin-top: 15px;
    padding-top: 10px;
    border-top: 1px solid rgba(255,255,255,0.1);
}

.input-area input {
    flex: 1;
    padding: 10px;
    background: rgba(0,0,0,0.2);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 6px;
    color: white;
}

.input-area button {
  padding: 0 15px;
  background: #3b82f6;
  border: none;
  border-radius: 6px;
  color: white;
  cursor: pointer;
}

/* Note */
.ai-summary {
    white-space: pre-wrap;
    line-height: 1.6;
    color: #ddd;
}

.empty-state {
    text-align: center;
    color: #777;
    margin-top: 40px;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
