<!--
  MythFactCarousel — Myth vs fact cards with auto-rotate and dot pagination.
  Challenges common sun safety misconceptions.
-->
<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const entries = [
  {
    myth: 'IT\'S NOT THAT HOT TODAY, SO UV IS PROBABLY LOW',
    fact: 'UV radiation can still be high on cool or cloudy days',
  },
  {
    myth: 'A TAN MEANS MY SKIN IS HEALTHY',
    fact: 'A tan is a sign of skin damage caused by UV exposure',
  },
  {
    myth: 'I ONLY NEED SUNSCREEN AT THE BEACH',
    fact: 'UV exposure can damage skin during everyday outdoor activities too',
  },
]

const currentIndex = ref(0)
let intervalId = null

function goTo(index) {
  currentIndex.value = ((index % entries.length) + entries.length) % entries.length
}

function next() {
  goTo(currentIndex.value + 1)
}

function startAutoRotate() {
  intervalId = setInterval(next, 5000)
}
function stopAutoRotate() {
  if (intervalId) {
    clearInterval(intervalId)
    intervalId = null
  }
}

onMounted(startAutoRotate)
onUnmounted(stopAutoRotate)
</script>

<template>
  <section class="myth-fact">
    <h2 class="myth-fact__title">Skin Misconceptions vs Facts</h2>
    <p class="myth-fact__subtitle">
      Young adults are often influenced by social media trends that promote tanning.
      This section helps challenge common misconceptions.
    </p>
    <div class="myth-fact__card uv-card">
      <div class="myth-fact__content">
        <p class="myth-fact__label myth-fact__label--myth">Myth</p>
        <p class="myth-fact__myth">{{ entries[currentIndex].myth }}</p>
        <p class="myth-fact__label myth-fact__label--fact">Fact</p>
        <p class="myth-fact__fact">{{ entries[currentIndex].fact }}</p>
      </div>
      <div class="myth-fact__dots" role="tablist" aria-label="Carousel pagination">
        <button
          v-for="(entry, i) in entries"
          :key="i"
          type="button"
          class="myth-fact__dot"
          :class="{ 'myth-fact__dot--active': i === currentIndex }"
          :aria-label="`Go to slide ${i + 1}`"
          :aria-selected="i === currentIndex"
          @click="goTo(i); stopAutoRotate(); startAutoRotate()"
        >
          <span class="myth-fact__dot-inner" />
        </button>
      </div>
    </div>
  </section>
</template>

<style scoped>
.myth-fact {
  margin-top: 2rem;
  margin-bottom: 0;
}
.myth-fact__title {
  margin: 0 0 0.5rem;
  font-size: 1.375rem;
  font-weight: 700;
  color: var(--uv-primary, #D8613C);
  letter-spacing: -0.02em;
}
.myth-fact__subtitle {
  margin: 0 0 1.5rem;
  font-size: 1rem;
  line-height: 1.65;
  color: var(--uv-text-muted, #8A8A8A);
}
 .myth-fact__card {
  padding: 2rem 1.75rem;
}
.myth-fact__content {
  margin-bottom: 1.5rem;
  text-align: center;
}
.myth-fact__label {
  margin: 0 0 0.35rem;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}
.myth-fact__label--myth {
  color: var(--uv-danger, #D44A4A);
}
.myth-fact__label--fact {
  color: var(--uv-primary, #D8613C);
  margin-top: 1rem;
}
.myth-fact__myth {
  margin: 0 0 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--uv-danger, #D44A4A);
  line-height: 1.4;
  letter-spacing: 0.02em;
}
.myth-fact__fact {
  margin: 0;
  font-size: 1rem;
  color: var(--uv-text-muted, #8A8A8A);
  line-height: 1.55;
}
.myth-fact__dots {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
}
.myth-fact__dot {
  width: 10px;
  height: 10px;
  padding: 0;
  border: none;
  border-radius: 50%;
  background: var(--uv-grid, #E6E1DA);
  cursor: pointer;
  transition: background 0.2s;
}
.myth-fact__dot:hover {
  background: var(--uv-text-muted, #8A8A8A);
}
.myth-fact__dot--active {
  background: var(--uv-primary, #D8613C);
}
.myth-fact__dot-inner {
  display: block;
  width: 100%;
  height: 100%;
}
</style>
