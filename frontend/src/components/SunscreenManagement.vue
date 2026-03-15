<!--
  Sunscreen Management — Recommendations based on current UV index.
  Uses shared uvData (from hero dashboard) so recommendations update when UV changes.
-->
<script setup>
import { inject, computed } from 'vue'

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

const dosageItems = [
  { area: 'Face & neck', amount: '1 teaspoon' },
  { area: 'Each arm', amount: '1 teaspoon' },
  { area: 'Each leg', amount: '2 teaspoons' },
  { area: 'Torso & back', amount: '2 teaspoons' },
]
</script>

<template>
  <section class="sunscreen">
    <h2 class="sunscreen__title">Sunscreen Management</h2>
    <p class="sunscreen__intro">
      Recommendations based on the current UV index for your location.
    </p>

    <!-- 1. Current UV Summary Card -->
    <div class="sunscreen__card uv-card">
      <h3 class="sunscreen__card-title">Current UV Summary</h3>
      <div v-if="data" class="sunscreen__uv-summary">
        <p class="sunscreen__location">{{ locationName }}</p>
        <div class="sunscreen__uv-row">
          <span class="sunscreen__uv-value">{{ uvValue }}</span>
          <span class="sunscreen__risk-badge" :class="riskColor ? `sunscreen__risk-badge--${riskColor}` : ''">
            {{ riskLevel }}
          </span>
        </div>
      </div>
      <p v-else class="sunscreen__no-data">Load the dashboard above to see UV for your location.</p>
    </div>

    <!-- 2. Recommended Protection Card -->
    <div class="sunscreen__card uv-card">
      <h3 class="sunscreen__card-title">Recommended Protection</h3>
      <div v-if="spfRecommendation.spf" class="sunscreen__spf-block">
        <p class="sunscreen__spf-value">{{ spfRecommendation.label }}</p>
        <p class="sunscreen__spf-explanation">{{ spfRecommendation.explanation }}</p>
      </div>
      <p v-else class="sunscreen__no-data">UV data is needed to recommend SPF.</p>
    </div>

    <!-- 3. Sunscreen Dosage Card -->
    <div class="sunscreen__card uv-card">
      <h3 class="sunscreen__card-title">Sunscreen Dosage</h3>
      <p class="sunscreen__dosage-intro">
        Apply approximately <strong>35 ml</strong> (about a shot glass) of sunscreen to cover exposed skin.
      </p>
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
    <div class="sunscreen__card uv-card">
      <h3 class="sunscreen__card-title">Reapplication</h3>
      <p class="sunscreen__reapply-text">
        Reapply every <strong>2 hours</strong> when outdoors and after swimming or sweating.
      </p>
    </div>
  </section>
</template>

<style scoped>
.sunscreen {
  margin-bottom: 0;
}
.sunscreen__title {
  margin: 0 0 0.5rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--uv-primary, #D8613C);
  letter-spacing: -0.02em;
}
.sunscreen__intro {
  margin: 0 0 1.25rem;
  font-size: 0.9375rem;
  color: var(--uv-text-muted, #8A8A8A);
  line-height: 1.55;
}

.sunscreen__card {
  margin-bottom: 1.25rem;
}
.sunscreen__card:last-child {
  margin-bottom: 0;
}
.sunscreen__card-title {
  margin: 0 0 0.75rem;
  font-size: 1.0625rem;
  font-weight: 700;
  color: var(--uv-text, #4A4A4A);
}

.sunscreen__uv-summary {
  margin: 0;
}
.sunscreen__location {
  margin: 0 0 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  color: var(--uv-value, #D54E4E);
}
.sunscreen__uv-row {
  display: flex;
  align-items: baseline;
  gap: 0.75rem;
  flex-wrap: wrap;
}
.sunscreen__uv-value {
  font-size: 2rem;
  font-weight: 800;
  color: var(--uv-value, #D54E4E);
  letter-spacing: -0.02em;
}
.sunscreen__risk-badge {
  display: inline-block;
  padding: 0.25rem 0.6rem;
  border-radius: 999px;
  font-size: 0.875rem;
  font-weight: 700;
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
  color: var(--uv-text-muted, #8A8A8A);
}

.sunscreen__spf-block {
  margin: 0;
}
.sunscreen__spf-value {
  margin: 0 0 0.5rem;
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--uv-primary, #D8613C);
  letter-spacing: -0.02em;
}
.sunscreen__spf-explanation {
  margin: 0;
  font-size: 0.9375rem;
  color: var(--uv-text-muted, #8A8A8A);
  line-height: 1.5;
}

.sunscreen__dosage-intro {
  margin: 0 0 1rem;
  font-size: 0.9375rem;
  color: var(--uv-text, #4A4A4A);
  line-height: 1.5;
}
.sunscreen__dosage-intro strong {
  color: var(--uv-primary, #D8613C);
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
  padding: 0.4rem 0;
  border-bottom: 1px solid var(--uv-grid, #E6E1DA);
  font-size: 0.9375rem;
}
.sunscreen__dosage-item:last-child {
  border-bottom: none;
}
.sunscreen__dosage-area {
  color: var(--uv-text, #4A4A4A);
}
.sunscreen__dosage-amount {
  font-weight: 600;
  color: var(--uv-primary, #D8613C);
}

.sunscreen__reapply-text {
  margin: 0;
  font-size: 0.9375rem;
  color: var(--uv-text, #4A4A4A);
  line-height: 1.5;
}
.sunscreen__reapply-text strong {
  color: var(--uv-primary, #D8613C);
}
</style>
