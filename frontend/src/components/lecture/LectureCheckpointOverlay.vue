<template>
  <div v-if="activeCheckpoint" class="checkpoint-overlay">
    <div class="checkpoint-card">
      <h3>Quiz Time!</h3>
      <p class="question">{{ activeCheckpoint.question }}</p>
      
      <div v-if="activeCheckpoint.options" class="options">
        <button 
          v-for="(option, index) in activeCheckpoint.options" 
          :key="index"
          @click="submitAnswer(index)"
          class="option-btn"
        >
          {{ option }}
        </button>
      </div>
      
      <div v-else class="confirmation">
        <button @click="submitAnswer(true)" class="confirm-btn">확인했습니다</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, defineProps, defineEmits } from 'vue';

const props = defineProps({
  currentTime: {
    type: Number,
    required: true
  },
  checkpoints: {
    type: Array, // [{time_point: 120, question: "...", options: []}]
    default: () => []
  }
});

const emit = defineEmits(['checkpoint-resolved', 'video-pause', 'video-resume']);

const activeCheckpoint = ref(null);
const resolvedCheckpoints = ref(new Set());

watch(() => props.currentTime, (newTime) => {
  // Find a checkpoint that matches current time (within 1 sec) and hasn't been resolved
  const cp = props.checkpoints.find(cp => 
    Math.abs(cp.time_point - newTime) < 1.0 && 
    !resolvedCheckpoints.value.has(cp.id)
  );

  if (cp && !activeCheckpoint.value) {
    activeCheckpoint.value = cp;
    emit('video-pause');
  }
});

const submitAnswer = (answer) => {
  // Logic to verify answer could go here or in parent
  // For now, we assume success for prototype
  if (activeCheckpoint.value) {
    resolvedCheckpoints.value.add(activeCheckpoint.value.id);
    const result = {
      checkpointId: activeCheckpoint.value.id,
      answer: answer,
      timestamp: new Date().toISOString()
    };
    emit('checkpoint-resolved', result);
    activeCheckpoint.value = null;
    emit('video-resume');
  }
};
</script>

<style scoped>
.checkpoint-overlay {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.checkpoint-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  max-width: 500px;
  width: 90%;
  text-align: center;
}

.question {
  font-size: 1.2rem;
  margin-bottom: 1.5rem;
  color: #333;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.option-btn {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #f9f9f9;
  cursor: pointer;
  transition: all 0.2s;
}

.option-btn:hover {
  background: #eef;
  border-color: #aaf;
}
</style>
