<template>
  <div class="auth-container">
    <router-link to="/" class="home-logo">RE BOOT</router-link>

    <div class="glass-container auth-box">
      <h2 style="text-align: center; margin-bottom: 25px; font-weight: 700;">회원가입</h2>
      
      <div class="tabs">
        <button 
          :class="['tab-btn', { active: role === 'STUDENT' }]" 
          @click="role = 'STUDENT'"
        >
          수강생
        </button>
        <button 
          :class="['tab-btn', { active: role === 'INSTRUCTOR' }]" 
          @click="role = 'INSTRUCTOR'"
        >
          강사
        </button>
      </div>

      <form @submit.prevent="handleSignup" style="display: flex; flex-direction: column; gap: 15px;">
        <div>
          <label class="label">아이디</label>
          <input v-model="username" type="text" class="glass-input" placeholder="사용할 아이디를 입력하세요" required />
        </div>

        <div>
          <label class="label">비밀번호</label>
          <input v-model="password" type="password" class="glass-input" placeholder="비밀번호를 입력하세요" required />
        </div>

        <div>
          <label class="label">닉네임</label>
          <input v-model="nickname" type="text" class="glass-input" placeholder="표시될 이름을 입력하세요" required />
        </div>

        <!-- Optional Email -->
        <div>
          <label class="label">이메일 (선택)</label>
          <input v-model="email" type="email" class="glass-input" placeholder="user@example.com" />
        </div>
      </form>

      <div class="button-group">
        <button @click="handleSignup" class="glass-button primary-btn">
          가입하기
        </button>
        <button @click="router.push('/login')" class="glass-button secondary-btn">
          뒤로가기
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const role = ref('STUDENT')
const username = ref('')
const password = ref('')
const nickname = ref('')
const email = ref('')

const handleSignup = async () => {
  // TODO: Implement actual API signup
  console.log(`Signing up as ${role.value} with ${username.value}`)
  
  try {
    // Mock signup success for now, or prepare for real API
    // const response = await axios.post('/api/users/register/', {
    //   username: username.value,
    //   password: password.value,
    //   nickname: nickname.value,
    //   email: email.value,
    //   role: role.value
    // })
    
    alert('계정이 생성되었습니다! 로그인해주세요.')
    router.push('/login')
  } catch (error) {
    console.error(error)
    alert('회원가입에 실패했습니다.')
  }
}
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  position: relative;
}

.home-logo {
  position: absolute;
  top: 30px;
  left: 40px;
  font-size: 1.5rem;
  font-weight: 900;
  text-decoration: none;
  color: white;
  letter-spacing: 2px;
  z-index: 10;
  transition: opacity 0.3s;
}

.home-logo:hover {
  opacity: 0.8;
  text-shadow: 0 0 10px rgba(255,255,255,0.5);
}

.auth-box {
  width: 100%;
  max-width: 450px;
  padding: 40px;
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.tabs {
  display: flex;
  margin-bottom: 25px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 5px;
}

.tab-btn {
  flex: 1;
  padding: 10px;
  border: none;
  background: transparent;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.3s ease;
  font-weight: 600;
}

.tab-btn.active {
  background: rgba(255, 255, 255, 0.25);
  color: white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.label {
  display: block; 
  margin-bottom: 6px; 
  font-size: 0.9rem; 
  font-weight: 500;
  color: #e5e7eb;
}

.glass-input {
  width: 100%;
  padding: 12px 15px;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.05);
  color: white;
  font-size: 1rem;
  outline: none;
  transition: all 0.3s;
}

.glass-input:focus {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.5);
  box-shadow: 0 0 10px rgba(255,255,255,0.1);
}

.button-group {
  display: flex;
  gap: 15px;
  margin-top: 25px;
  width: 100%;
}

.primary-btn {
  flex: 1;
  padding: 12px;
  background: linear-gradient(135deg, rgba(255,255,255,0.3) 0%, rgba(255,255,255,0.1) 100%);
  border: 1px solid rgba(255,255,255,0.4);
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 10px;
  cursor: pointer;
}

.primary-btn:hover {
  background: linear-gradient(135deg, rgba(255,255,255,0.4) 0%, rgba(255,255,255,0.2) 100%);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

.secondary-btn {
  flex: 1;
  padding: 12px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 10px;
  color: #ddd;
  cursor: pointer;
  transition: all 0.3s;
}

.secondary-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  transform: translateY(-2px);
}
</style>
