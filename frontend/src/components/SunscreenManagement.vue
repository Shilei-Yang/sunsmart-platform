<!--
  Sunscreen Management — Recommendations based on current UV index.
  Uses shared uvData (from hero dashboard) so recommendations update when UV changes.
-->
<script setup>
import { inject, computed } from 'vue'
import sunscreenBg from '@/assets/pexels-armin-rimoldi-5269653.jpg'

const uvData = inject('uvData', null)
const data = computed(() => uvData?.value ?? null)

const locationName = computed(() => data.value?.location_name ?? 'Your location')
// Use current UV for summary and SPF; fallback to max daily uv_index
const uvValue = computed(() => {
  const v = data.value?.current_uv ?? data.value?.uv_index
  return v != null ? Number(v) : null
})
const riskLevel = computed(() => data.value?.current_risk_level ?? data.value?.risk_level ?? null)
const riskColor = computed(() => data.value?.current_color ?? data.value?.color ?? null)

// UV → SPF mapping and explanation (based on current UV)
const spfRecommendation = computed(() => {
  const uv = uvValue.value != null ? uvValue.value : null
  if (uv == null) return { spf: null, label: null, explanation: null }
  if (uv <= 2) return { spf: '15+', label: 'Optional SPF 15+', explanation: 'UV is low. Sunscreen is optional; consider SPF 15+ for extended exposure.' }
  if (uv <= 5) return { spf: '30+', label: 'SPF 30+', explanation: 'Moderate UV. Use broad-spectrum SPF 30+ when spending time outdoors.' }
  if (uv <= 7) return { spf: '30–50+', label: 'SPF 30–50+', explanation: 'High UV. Use SPF 30–50+ and reapply regularly.' }
  if (uv <= 10) return { spf: '50+', label: 'SPF 50+', explanation: 'Very high UV. Use SPF 50+ and other protection (hat, shade).' }
  return { spf: '50+', label: 'SPF 50+', explanation: 'Extreme UV. Use SPF 50+ and minimise time in direct sun.' }
})

function uvColorToHex(color) {
  switch (color) {
    case 'green': return '#16a34a'
    case 'yellow': return '#ca8a04'
    case 'orange': return '#ea580c'
    case 'red': return '#D54E4E'
    case 'purple': return '#7c3aed'
    default: return '#6b7280'
  }
}

const uvColorHex = computed(() => uvColorToHex(riskColor.value))

const dosageItems = [
  { area: 'Face & neck', amount: '1 teaspoon' },
  { area: 'Each arm', amount: '1 teaspoon' },
  { area: 'Each leg', amount: '2 teaspoons' },
  { area: 'Torso & back', amount: '2 teaspoons' },
]

const uvBand = computed(() => {
  const uv = uvValue.value
  if (uv == null) return 'unknown'
  if (uv <= 2) return 'low'
  if (uv <= 5) return 'moderate'
  if (uv <= 7) return 'high'
  if (uv <= 10) return 'veryHigh'
  return 'extreme'
})

const dosageGuidance = computed(() => {
  const base = {
    intro: 'Apply approximately 35 ml (about a shot glass) of sunscreen to cover exposed skin.',
    note: 'Use enough sunscreen to fully cover exposed areas.',
  }
  if (uvBand.value === 'unknown') {
    return {
      ...base,
      reapplyEvery: '2 hours',
      reapplyNote: 'Reapply after swimming, sweating, or towel drying.',
    }
  }
  if (uvBand.value === 'low') {
    return {
      ...base,
      reapplyEvery: '2 hours',
      reapplyNote: 'Low UV now, but reapply if you stay outdoors for extended time.',
    }
  }
  if (uvBand.value === 'moderate') {
    return {
      ...base,
      reapplyEvery: '2 hours',
      reapplyNote: 'Moderate UV: keep regular reapplication and use shade where possible.',
    }
  }
  if (uvBand.value === 'high') {
    return {
      ...base,
      reapplyEvery: '90 minutes',
      reapplyNote: 'High UV: apply generously and avoid missing commonly exposed areas.',
    }
  }
  if (uvBand.value === 'veryHigh') {
    return {
      ...base,
      reapplyEvery: '60-90 minutes',
      reapplyNote: 'Very high UV: pair sunscreen with hat, clothing, and shade.',
    }
  }
  return {
    ...base,
    reapplyEvery: '60 minutes',
    reapplyNote: 'Extreme UV: minimise direct sun exposure and reapply very frequently.',
  }
})
</script>

<template>
  <section class="sunscreen">
    <img :src="sunscreenBg" alt="" class="sunscreen__bg" aria-hidden="true" />
    <div class="sunscreen__overlay" />

    <div class="sunscreen__body">
      <div class="sunscreen__header">
        <h2 class="sunscreen__title">Sunscreen Management</h2>
        <p class="sunscreen__intro">
          Recommendations based on the current UV index for your location.
        </p>
      </div>

      <!-- 1. Current UV Summary Card -->
      <div class="sunscreen__card sunscreen__card--glass sunscreen__card--uv" :style="data ? { borderLeftColor: uvColorHex } : {}">
        <h3 class="sunscreen__card-title">Current UV Summary</h3>
        <div v-if="data" class="sunscreen__uv-summary">
          <p class="sunscreen__location">{{ locationName }}</p>
          <div class="sunscreen__uv-row">
            <span class="sunscreen__uv-value" :style="{ color: uvColorHex }">{{ uvValue }}</span>
            <span class="sunscreen__risk-badge" :class="riskColor ? `sunscreen__risk-badge--${riskColor}` : ''">
              {{ riskLevel }}
            </span>
          </div>
        </div>
        <p v-else class="sunscreen__no-data">Load the dashboard above to see UV for your location.</p>
      </div>

      <!-- 2. Recommended Protection Card -->
      <div class="sunscreen__card sunscreen__card--glass">
        <h3 class="sunscreen__card-title">Recommended Protection</h3>
        <div v-if="spfRecommendation.spf" class="sunscreen__spf-block">
          <p class="sunscreen__spf-value">{{ spfRecommendation.label }}</p>
          <p class="sunscreen__spf-explanation">{{ spfRecommendation.explanation }}</p>
        </div>
        <p v-else class="sunscreen__no-data">UV data is needed to recommend SPF.</p>
      </div>

      <!-- 3. Sunscreen Dosage Card -->
      <div class="sunscreen__card sunscreen__card--glass">
        <h3 class="sunscreen__card-title">Sunscreen Dosage</h3>
        <p class="sunscreen__dosage-intro">
          {{ dosageGuidance.intro }}
        </p>
        <p class="sunscreen__dosage-note">{{ dosageGuidance.note }}</p>
        <ul class="sunscreen__dosage-list" role="list">
          <li
            v-for="item in dosageItems"
            :key="item.area"
            class="sunscreen__dosage-item"
          >
            <span class="sunscreen__dosage-area">{{ item.area }}</span>
            <span class="sunscreen__dosage-amount">{{ item.amount }}</span>
          </li>
        </ul>
      </div>

      <!-- 4. Reapplication Reminder Card -->
      <div class="sunscreen__card sunscreen__card--glass">
        <h3 class="sunscreen__card-title">Reapplication</h3>
        <p class="sunscreen__reapply-text">
          Reapply every <strong>{{ dosageGuidance.reapplyEvery }}</strong> when outdoors.
        </p>
        <p class="sunscreen__reapply-note">{{ dosageGuidance.reapplyNote }}</p>
      </div>
    </div>
  </section>
</template>

<style scoped>
/* ── Section wrapper — immersive photo background ── */
.sunscreen {
  position: relative;
  overflow: hidden;
  border-radius: 20px;
  margin-bottom: 0;
}

.sunscreen__bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 35%;
}

.sunscreen__overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    170deg,
    rgba(35, 25, 18, 0.72) 0%,
    rgba(40, 30, 20, 0.62) 35%,
    rgba(45, 32, 22, 0.52) 65%,
    rgba(50, 35, 25, 0.42) 100%
  );
  pointer-events: none;
}

/* ── Content layer ── */
.sunscreen__body {
  position: relative;
  z-index: 1;
  padding: 2.25rem 2rem 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.sunscreen__header {
  margin-bottom: 0.25rem;
}
.sunscreen__title {
  margin: 0 0 0.5rem;
  font-size: 1.5rem;
  font-weight: 800;
  color: #fff;
  letter-spacing: -0.02em;
  text-shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
}
.sunscreen__intro {
  margin: 0;
  font-size: 0.9375rem;
  color: rgba(255, 255, 255, 0.65);
  line-height: 1.55;
}

/* ── Frosted glass cards ── */
.sunscreen__card {
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 16px;
  padding: 1.5rem 1.75rem;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.12);
}
.sunscreen__card-title {
  margin: 0 0 0.75rem;
  font-size: 1.0625rem;
  font-weight: 700;
  color: #fff;
}

/* UV summary card — accent border on left */
.sunscreen__card--uv {
  border-left: 4px solid rgba(255, 255, 255, 0.25);
  transition: border-left-color 0.4s ease;
}

.sunscreen__uv-summary {
  margin: 0;
}
.sunscreen__location {
  margin: 0 0 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.8);
}
.sunscreen__uv-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}
.sunscreen__uv-value {
  font-size: 2.25rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  line-height: 1;
  transition: color 0.4s ease;
}
.sunscreen__risk-badge {
  display: inline-block;
  padding: 0.25rem 0.7rem;
  border-radius: 999px;
  font-size: 0.8125rem;
  font-weight: 700;
  letter-spacing: 0.03em;
  color: #fff;
  background: var(--uv-danger, #D44A4A);
}
.sunscreen__risk-badge--green { background: #16a34a; }
.sunscreen__risk-badge--yellow { background: #ca8a04; color: #1c1917; }
.sunscreen__risk-badge--orange { background: #ea580c; }
.sunscreen__risk-badge--red { background: #D44A4A; }
.sunscreen__risk-badge--purple { background: #7c3aed; }

.sunscreen__no-data {
  margin: 0;
  font-size: 0.9375rem;
  color: rgba(255, 255, 255, 0.55);
}

/* SPF recommendation */
.sunscreen__spf-block {
  margin: 0;
}
.sunscreen__spf-value {
  margin: 0 0 0.5rem;
  font-size: 1.5rem;
  font-weight: 800;
  color: #ffb088;
  letter-spacing: -0.02em;
}
.sunscreen__spf-explanation {
  margin: 0;
  font-size: 0.9375rem;
  color: rgba(255, 255, 255, 0.6);
  line-height: 1.5;
}

/* Dosage */
.sunscreen__dosage-intro {
  margin: 0 0 1rem;
  font-size: 0.9375rem;
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.5;
}
.sunscreen__dosage-note {
  margin: -0.35rem 0 0.85rem;
  font-size: 0.8125rem;
  color: rgba(255, 255, 255, 0.65);
  line-height: 1.5;
}
.sunscreen__dosage-list {
  margin: 0;
  padding: 0;
  list-style: none;
}
.sunscreen__dosage-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.55rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  font-size: 0.9375rem;
}
.sunscreen__dosage-item:last-child {
  border-bottom: none;
}
.sunscreen__dosage-area {
  color: rgba(255, 255, 255, 0.8);
}
.sunscreen__dosage-amount {
  font-weight: 600;
  color: #ffb088;
}

/* Reapplication */
.sunscreen__reapply-text {
  margin: 0;
  font-size: 0.9375rem;
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.5;
}
.sunscreen__reapply-text strong {
  color: #ffb088;
}
.sunscreen__reapply-note {
  margin: 0.45rem 0 0;
  font-size: 0.8125rem;
  color: rgba(255, 255, 255, 0.65);
  line-height: 1.5;
}

/* ── Mobile ── */
@media (max-width: 600px) {
  .sunscreen__body {
    padding: 1.75rem 1.25rem 1.5rem;
    gap: 1rem;
  }
  .sunscreen__title { font-size: 1.25rem; }
  .sunscreen__card { padding: 1.25rem 1.25rem; }
}
</style>
