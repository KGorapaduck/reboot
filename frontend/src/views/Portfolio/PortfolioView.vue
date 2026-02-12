<template>
  <div class="portfolio-container">
    <!-- Header -->
    <header class="page-header">
      <h1>내 포트폴리오</h1>
      <button class="action-btn primary" @click="createNewPortfolio">+ 포트폴리오 생성</button>
    </header>

    <div class="content-wrapper">
      <!-- Left: Portfolio List -->
      <aside class="list-section glass-card">
        <ul class="portfolio-list">
          <li 
            v-for="item in portfolios" 
            :key="item.id" 
            class="portfolio-item" 
            :class="{ active: selectedPortfolio && selectedPortfolio.id === item.id }"
            @click="selectPortfolio(item)"
          >
            <div class="item-header">
               <span class="item-title">{{ item.title }}</span>
               <span class="badge" :class="item.type.toLowerCase()">{{ item.type }}</span>
            </div>
            <span class="item-date">{{ formatDate(item.created_at) }}</span>
          </li>
        </ul>
      </aside>

      <!-- Right: Detail/Preview -->
      <main class="detail-section glass-card">
        <div v-if="selectedPortfolio" class="detail-content">
            <div class="detail-header">
                <h2>{{ selectedPortfolio.title }}</h2>
                <div class="detail-actions">
                    <button class="action-btn secondary">편집</button>
                    <button class="action-btn secondary">다운로드</button>
                </div>
            </div>
            
            <div class="markdown-preview">
                <!-- In a real app, use 'marked' or similar to render HTML -->
                <pre>{{ selectedPortfolio.compiled_markdown }}</pre>
            </div>

            <div class="project-section">
                <h3>포함된 프로젝트</h3>
                <div class="project-chips">
                    <span v-for="proj in selectedPortfolio.projects" :key="proj.id" class="project-chip">
                        {{ proj.name }}
                    </span>
                    <button class="add-project-btn">+ 프로젝트 추가</button>
                </div>
            </div>
        </div>
        <div v-else class="empty-state">
            <p>좌측 목록에서 포트폴리오를 선택하세요.</p>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const portfolios = ref([
  { 
      id: 1, 
      title: 'Backend Developer Resume', 
      type: 'RESUME', 
      created_at: '2023-10-27T10:00:00',
      compiled_markdown: '# John Doe\n\n## Backend Developer\n\nExperienced in Django, Python...',
      projects: [{ id: 101, name: 'E-commerce API' }]
  },
  { 
      id: 2, 
      title: 'AI Startup Plan', 
      type: 'BUSINESS_PLAN', 
      created_at: '2023-11-02T14:30:00',
      compiled_markdown: '# Re:Boot Business Plan\n\n## Executive Summary\n\nAI-driven learning platform...',
      projects: [{ id: 102, name: 'Market Analysis' }]
  }
])

const selectedPortfolio = ref(null)

const selectPortfolio = (item) => {
    selectedPortfolio.value = item
}

const createNewPortfolio = () => {
    alert("새 포트폴리오 생성 마법사가 실행됩니다. (구현 예정)")
}

const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'short', day: 'numeric' }
    return new Date(dateString).toLocaleDateString('ko-KR', options)
}
</script>

<style scoped>
.portfolio-container {
  padding: 40px;
  max-width: 1200px;
  margin: 0 auto;
  color: white;
  height: calc(100vh - 80px); /* Adjust for navbar */
  display: flex;
  flex-direction: column;
}

.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.page-header h1 {
    font-size: 2rem;
    font-weight: 700;
    margin: 0;
}

.content-wrapper {
    display: flex;
    gap: 20px;
    flex: 1;
    overflow: hidden;
}

/* List Section */
.list-section {
    flex: 1;
    background: rgba(28, 50, 106, 0.4);
    border-radius: 12px;
    overflow-y: auto;
    padding: 10px;
    min-width: 300px;
}

.portfolio-list {
    list-style: none;
    padding: 0;
}

.portfolio-item {
    padding: 15px;
    margin-bottom: 10px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.2s;
}

.portfolio-item:hover, .portfolio-item.active {
    background: rgba(255, 255, 255, 0.15);
    border: 1px solid rgba(59, 130, 246, 0.5);
}

.item-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 5px;
}

.item-title {
    font-weight: bold;
    font-size: 1rem;
}

.badge {
    font-size: 0.7rem;
    padding: 2px 6px;
    border-radius: 4px;
    text-transform: uppercase;
}

.badge.resume { background: #3b82f6; color: white; }
.badge.business_plan { background: #a855f7; color: white; }

.item-date {
    font-size: 0.8rem;
    color: #aaa;
}

/* Detail Section */
.detail-section {
    flex: 2;
    background: rgba(20, 20, 30, 0.6);
    border-radius: 12px;
    padding: 30px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
}

.detail-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    padding-bottom: 15px;
}

.detail-header h2 {
    margin: 0;
    font-size: 1.5rem;
}

.detail-actions {
    display: flex;
    gap: 10px;
}

.markdown-preview {
    flex: 1;
    background: rgba(0,0,0,0.3);
    padding: 20px;
    border-radius: 8px;
    overflow-y: auto;
    font-family: monospace;
    white-space: pre-wrap;
    color: #ddd;
    line-height: 1.6;
}

.project-section {
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid rgba(255,255,255,0.1);
}

.project-chips {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 10px;
}

.project-chip {
    background: rgba(59, 130, 246, 0.2);
    padding: 5px 10px;
    border-radius: 15px;
    font-size: 0.9rem;
    color: #93c5fd;
}

.add-project-btn {
    background: none;
    border: 1px dashed #666;
    color: #888;
    padding: 5px 10px;
    border-radius: 15px;
    cursor: pointer;
}

.empty-state {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    color: #666;
}

/* Buttons */
.action-btn {
    padding: 8px 16px;
    border-radius: 6px;
    border: none;
    cursor: pointer;
    font-weight: 600;
}

.primary { background: #3b82f6; color: white; }
.secondary { background: rgba(255,255,255,0.1); color: white; }
</style>
