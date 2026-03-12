<script setup>
import { ref, onMounted } from 'vue'

const apiBase = import.meta.env.VITE_API_BASE ?? 'http://localhost:5000'
const health = ref(null)
const healthError = ref(null)

async function checkBackendHealth() {
  try {
    const res = await fetch(`${apiBase}/api/health`)
    health.value = await res.json()
    healthError.value = null
  } catch (err) {
    healthError.value = err.message
    health.value = null
  }
}

onMounted(checkBackendHealth)
</script>

<template>
  <h1>Sun Smart Platform</h1>
  <p>
    Visit <a href="https://vuejs.org/" target="_blank" rel="noopener">vuejs.org</a> to read the
    documentation
  </p>
  <section v-if="health" class="health">
    <strong>Backend:</strong> {{ health.status }} — {{ health.message }}
  </section>
  <section v-else-if="healthError" class="health error">
    <strong>Backend:</strong> {{ healthError }}
  </section>
  <section v-else class="health">Checking backend…</section>
</template>

<style scoped>
.health {
  margin-top: 1rem;
  padding: 0.5rem;
}
.health.error {
  color: #c00;
}
</style>
