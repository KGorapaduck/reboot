<template>
  <div class="instructor-dashboard">
    <div class="glass-container">
      <h1>Instructor Dashboard</h1>
      <p>강의를 업로드하고 AI 분석 상태를 관리하세요.</p>
      
      <div class="upload-section glass-container" style="margin-top: 20px;">
        <h3>새 강의 업로드</h3>
        <div style="display: flex; flex-direction: column; gap: 10px;">
          <input type="text" class="glass-input" placeholder="강의 제목 입력" />
          <input type="file" class="glass-button" style="width: fit-content;" />
          <button class="glass-button" style="width: fit-content; background: var(--primary-color);">업로드 시작</button>
        </div>
      </div>

      <div class="status-section" style="margin-top: 30px;">
        <h3>AI 처리 현황</h3>
        <div class="glass-container" style="padding: 15px;">
          <table style="width: 100%; border-collapse: collapse; color: white;">
            <thead>
              <tr style="border-bottom: 1px solid var(--glass-border);">
                <th style="padding: 10px; text-align: left;">강의명</th>
                <th style="padding: 10px; text-align: left;">STT 상태</th>
                <th style="padding: 10px; text-align: left;">임베딩 상태</th>
                <th style="padding: 10px; text-align: left;">작업</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td style="padding: 10px;">1강. Vue.js 기초</td>
                <td style="padding: 10px;"><span style="color: #4caf50;">완료</span></td>
                <td style="padding: 10px;"><span style="color: #4caf50;">완료</span></td>
                <td style="padding: 10px;"><button class="glass-button" style="padding: 5px 10px;">상세보기</button></td>
              </tr>
              <tr>
                <td style="padding: 10px;">2강. Pinia 상태관리</td>
                <td style="padding: 10px;"><span style="color: #ff9800;">진행중 (80%)</span></td>
                <td style="padding: 10px;"><span style="color: #9e9e9e;">대기중</span></td>
                <td style="padding: 10px;"><button class="glass-button" style="padding: 5px 10px;" disabled>대기</button></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.instructor-dashboard {
  max-width: 1000px;
  margin: 0 auto;
}

table tr:hover {
  background: rgba(255, 255, 255, 0.05);
}
</style>
