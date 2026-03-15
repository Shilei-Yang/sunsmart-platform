<!--
  MythFactCarousel — Immersive photo-backed carousel with per-slide imagery and color palettes.
-->
<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import imgForest from '@/assets/pexels-pixabay-209756.jpg'
import imgBeach from '@/assets/pexels-karola-g-5202466.jpg'
import imgOcean from '@/assets/pexels-sebastian-189349.jpg'

const entries = [
  {
    myth: '"It\'s not that hot today, so UV is probably low"',
    fact: 'UV radiation can still be high on cool or cloudy days. Temperature and UV levels are not the same thing.',
    image: imgForest,
    position: 'center 40%',
    theme: 'forest',
  },
  {
    myth: '"A tan means my skin is healthy"',
    fact: 'A tan is actually a sign of skin damage — your body\'s response to UV injury. There is no such thing as a safe tan.',
    image: imgBeach,
    position: 'center 30%',
    theme: 'sand',
  },
  {
    myth: '"I only need sunscreen at the beach"',
    fact: 'UV exposure happens during everyday activities — walking, driving, even sitting near windows. Protection matters everywhere.',
    image: imgOcean,
    position: 'center 50%',
    theme: 'ocean',
  },
]

const currentIndex = ref(0)
const transitioning = ref(false)
let intervalId = null

const currentEntry = computed(() => entries[currentIndex.value])

function goTo(index) {
  if (transitioning.value) return
  transitioning.value = true
  setTimeout(() => { transitioning.value = false }, 500)
  currentIndex.value = ((index % entries.length) + entries.length) % entries.length
}
function next() { goTo(currentIndex.value + 1) }
function startAutoRotate() { intervalId = setInterval(next, 6000) }
function stopAutoRotate() {
  if (intervalId) { clearInterval(intervalId); intervalId = null }
}

onMounted(startAutoRotate)
onUnmounted(stopAutoRotate)
</script>

<template>
  <section class="myth-fact">
    <div class="myth-fact__hero" :class="`myth-fact__hero--${currentEntry.theme}`">
      <!-- Background images — all rendered, only active one visible -->
      <img
        v-for="(entry, i) in entries"
        :key="entry.theme"
        :src="entry.image"
        :alt="`Background for slide ${i + 1}`"
        class="myth-fact__bg"
        :class="{ 'myth-fact__bg--active': i === currentIndex }"
        :style="{ objectPosition: entry.position }"
      />
      <div class="myth-fact__overlay" />

      <div class="myth-fact__content">
        <!-- Header -->
        <p class="myth-fact__eyebrow">Think you know?</p>
        <h2 class="myth-fact__title">Myths vs Facts</h2>

        <!-- Slide -->
        <div class="myth-fact__slide">
          <span class="myth-fact__tag myth-fact__tag--myth">Myth</span>
          <p class="myth-fact__myth-text">{{ currentEntry.myth }}</p>

          <div class="myth-fact__divider" />

          <span class="myth-fact__tag myth-fact__tag--fact">Fact</span>
          <p class="myth-fact__fact-text">{{ currentEntry.fact }}</p>
        </div>

        <!-- Dots -->
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
          />
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.myth-fact {
  margin-top: 2rem;
  margin-bottom: 0;
}

.myth-fact__hero {
  position: relative;
  overflow: hidden;
  border-radius: 20px;
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Background images — crossfade */
.myth-fact__bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0;
  transition: opacity 0.8s ease;
}
.myth-fact__bg--active {
  opacity: 1;
}

/* Overlay — themed via parent modifier */
.myth-fact__overlay {
  position: absolute;
  inset: 0;
  pointer-events: none;
  transition: background 0.8s ease;
}

/* ── Theme: Forest (green/golden) ── */
.myth-fact__hero--forest .myth-fact__overlay {
  background: linear-gradient(
    160deg,
    rgba(15, 30, 10, 0.88) 0%,
    rgba(20, 35, 15, 0.78) 50%,
    rgba(30, 45, 15, 0.68) 100%
  );
}
.myth-fact__hero--forest .myth-fact__eyebrow { color: rgba(180, 220, 140, 0.6); }
.myth-fact__hero--forest .myth-fact__title { color: #e8f5d4; }
.myth-fact__hero--forest .myth-fact__myth-text { color: rgba(240, 250, 220, 0.9); }
.myth-fact__hero--forest .myth-fact__fact-text { color: rgba(200, 230, 170, 0.75); }
.myth-fact__hero--forest .myth-fact__divider { background: rgba(180, 220, 140, 0.2); }
.myth-fact__hero--forest .myth-fact__tag--myth {
  background: rgba(212, 74, 74, 0.2);
  color: #ff9e9e;
  border-color: rgba(212, 74, 74, 0.25);
}
.myth-fact__hero--forest .myth-fact__tag--fact {
  background: rgba(100, 200, 100, 0.2);
  color: #90ee90;
  border-color: rgba(100, 200, 100, 0.25);
}

/* ── Theme: Sand (warm beach) ── */
.myth-fact__hero--sand .myth-fact__overlay {
  background: linear-gradient(
    160deg,
    rgba(60, 40, 20, 0.88) 0%,
    rgba(70, 50, 25, 0.78) 50%,
    rgba(80, 55, 30, 0.65) 100%
  );
}
.myth-fact__hero--sand .myth-fact__eyebrow { color: rgba(255, 220, 170, 0.55); }
.myth-fact__hero--sand .myth-fact__title { color: #fff3e0; }
.myth-fact__hero--sand .myth-fact__myth-text { color: rgba(255, 245, 230, 0.9); }
.myth-fact__hero--sand .myth-fact__fact-text { color: rgba(255, 225, 185, 0.75); }
.myth-fact__hero--sand .myth-fact__divider { background: rgba(255, 200, 140, 0.2); }
.myth-fact__hero--sand .myth-fact__tag--myth {
  background: rgba(220, 80, 60, 0.22);
  color: #ffb0a0;
  border-color: rgba(220, 80, 60, 0.25);
}
.myth-fact__hero--sand .myth-fact__tag--fact {
  background: rgba(80, 190, 180, 0.2);
  color: #80ddd5;
  border-color: rgba(80, 190, 180, 0.25);
}

/* ── Theme: Ocean (deep amber/blue) ── */
.myth-fact__hero--ocean .myth-fact__overlay {
  background: linear-gradient(
    160deg,
    rgba(15, 20, 40, 0.9) 0%,
    rgba(25, 30, 50, 0.8) 50%,
    rgba(40, 35, 45, 0.68) 100%
  );
}
.myth-fact__hero--ocean .myth-fact__eyebrow { color: rgba(180, 200, 240, 0.5); }
.myth-fact__hero--ocean .myth-fact__title { color: #ffecd2; }
.myth-fact__hero--ocean .myth-fact__myth-text { color: rgba(255, 240, 220, 0.9); }
.myth-fact__hero--ocean .myth-fact__fact-text { color: rgba(190, 210, 240, 0.75); }
.myth-fact__hero--ocean .myth-fact__divider { background: rgba(200, 180, 150, 0.2); }
.myth-fact__hero--ocean .myth-fact__tag--myth {
  background: rgba(255, 140, 100, 0.2);
  color: #ffb89e;
  border-color: rgba(255, 140, 100, 0.25);
}
.myth-fact__hero--ocean .myth-fact__tag--fact {
  background: rgba(100, 180, 255, 0.18);
  color: #a0d0ff;
  border-color: rgba(100, 180, 255, 0.22);
}

/* Content layer — centered */
.myth-fact__content {
  position: relative;
  z-index: 1;
  padding: 2.25rem 2.5rem 2rem;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  gap: 0.5rem;
}

/* Header */
.myth-fact__eyebrow {
  margin: 0;
  font-size: 0.6875rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  transition: color 0.8s ease;
}
.myth-fact__title {
  margin: 0 0 0.75rem;
  font-size: 1.5rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  line-height: 1.2;
  text-shadow: 0 2px 16px rgba(0, 0, 0, 0.35);
  transition: color 0.8s ease;
}

/* Slide content */
.myth-fact__slide {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.4rem;
  max-width: 540px;
}

/* Tags */
.myth-fact__tag {
  display: inline-flex;
  padding: 0.2rem 0.65rem;
  font-size: 0.625rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  border-radius: 999px;
  border: 1px solid transparent;
  transition: background 0.8s ease, color 0.8s ease, border-color 0.8s ease;
}

.myth-fact__myth-text {
  margin: 0;
  font-size: 1.15rem;
  font-weight: 600;
  font-style: italic;
  line-height: 1.4;
  transition: color 0.8s ease;
}

.myth-fact__divider {
  width: 40px;
  height: 2px;
  border-radius: 1px;
  margin: 0.5rem 0;
  transition: background 0.8s ease;
}

.myth-fact__fact-text {
  margin: 0;
  font-size: 0.9375rem;
  font-weight: 500;
  line-height: 1.55;
  transition: color 0.8s ease;
}

/* Dots */
.myth-fact__dots {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}
.myth-fact__dot {
  width: 8px;
  height: 8px;
  padding: 0;
  border: none;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.25);
  cursor: pointer;
  transition: background 0.3s, transform 0.3s;
}
.myth-fact__dot:hover {
  background: rgba(255, 255, 255, 0.5);
}
.myth-fact__dot--active {
  background: #fff;
  transform: scale(1.25);
}

/* Mobile */
@media (max-width: 600px) {
  .myth-fact__hero { min-height: 360px; }
  .myth-fact__content { padding: 1.75rem 1.5rem 1.5rem; }
  .myth-fact__title { font-size: 1.25rem; }
  .myth-fact__myth-text { font-size: 1rem; }
}
</style>
