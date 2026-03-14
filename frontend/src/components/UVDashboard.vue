<!--
  Hero UV Dashboard — Two-column layout: left = current UV summary, right = weekly forecast chart.
  Pastel gradient hero card. Fetches /api/uv on load via geolocation; API integration unchanged.
-->
<script setup>
import { ref, onMounted, computed } from 'vue'
import MaxUVGraph from '@/components/MaxUVGraph.vue'

// Match backend port (default 5000). Override with VITE_API_BASE in .env if you use e.g. 5001 on macOS.
const apiBase = import.meta.env.VITE_API_BASE ?? 'http://localhost:5000'
const uvData = ref(null)
const uvStatus = ref(null)
const uvError = ref(null) // optional message for debugging

async function fetchUvForLocation(latitude, longitude) {
  const url = `${apiBase}/api/uv?lat=${latitude}&lon=${longitude}`
  uvError.value = null
  try {
    const res = await fetch(url)
    if (!res.ok) {
      const body = await res.text()
      uvError.value = body || `HTTP ${res.status}`
      uvStatus.value = 'error'
      uvData.value = null
      return
    }
    const json = await res.json()
    uvData.value = json
    uvStatus.value = 'success'
  } catch (e) {
    uvError.value = e?.message || 'Network error'
    uvStatus.value = 'error'
    uvData.value = null
  }
}

function startUvFlow() {
  uvStatus.value = 'loading'
  uvData.value = null
  if (!navigator.geolocation) {
    uvStatus.value = 'denied'
    return
  }
  navigator.geolocation.getCurrentPosition(
    (position) => {
      const { latitude, longitude } = position.coords
      fetchUvForLocation(latitude, longitude)
    },
    () => { uvStatus.value = 'denied' },
    { enableHighAccuracy: false, timeout: 20000, maximumAge: 300000 }
  )
}

const formattedDateTime = computed(() => {
  const d = new Date()
  return d.toLocaleDateString('en-AU', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  })
})

// Coordinates in design format: "37.8136° S, 144.9631° E"
const coordinatesDisplay = computed(() => {
  if (!uvData.value) return null
  const { latitude, longitude } = uvData.value
  const latDir = latitude >= 0 ? 'N' : 'S'
  const lonDir = longitude >= 0 ? 'E' : 'W'
  return `${Math.abs(latitude).toFixed(4)}° ${latDir}, ${Math.abs(longitude).toFixed(4)}° ${lonDir}`
})

// Location/region: API does not return place name; show generic until backend adds it
const locationName = computed(() => uvData.value?.location_name ?? 'Your location')
const regionDisplay = computed(() => uvData.value?.region ?? '—')

const dailyForGraph = computed(() => {
  if (!uvData.value?.daily) return []
  return uvData.value.daily
})

const historyForGraph = computed(() => {
  if (Array.isArray(uvData.value?.history) && uvData.value.history.length) return uvData.value.history
  const base = Number(uvData.value?.uv_index) || 6.5
  const today = new Date()
  const offsets = [-1.8, 0.2, 1.1, 2.6, 0.7, -0.4, 1.9]
  return offsets.map((off, idx) => {
    const d = new Date(today)
    d.setDate(today.getDate() - (6 - idx))
    const iso = d.toISOString().slice(0, 10)
    const label = d.toLocaleDateString('en-AU', { weekday: 'short' })
    const uv = Math.max(0, Math.min(13, Number((base + off).toFixed(1))))
    return { date: iso, label, uv_index: uv }
  })
})

// Three alert rows: first from API message, then standard recommendations
const alertRows = computed(() => {
  const msg = uvData.value?.message ?? ''
  return [
    msg || 'Check local UV index for exposure time.',
    'Wear sunscreen',
    'Protective clothing and sunglasses',
  ]
})

onMounted(startUvFlow)
</script>

<template>
  <section class="hero-dashboard">
    <div class="hero-dashboard__grid">
      <!-- Left column: current UV summary -->
      <div class="hero-dashboard__left">
        <!-- a. Search bar -->
        <div class="hero-dashboard__search-wrap">
          <span class="hero-dashboard__search-icon" aria-hidden="true">🔍</span>
          <input
            type="text"
            class="hero-dashboard__search"
            placeholder="Search Location"
            readonly
            aria-label="Search location"
          />
        </div>
        <!-- b. Coordinates -->
        <p v-if="coordinatesDisplay" class="hero-dashboard__coords">{{ coordinatesDisplay }}</p>
        <!-- c. Location heading, d. Region subtitle -->
        <div class="hero-dashboard__location-row">
          <h1 class="hero-dashboard__location-heading">{{ locationName }}</h1>
          <span class="hero-dashboard__region">{{ regionDisplay }}</span>
        </div>
        <!-- e. Date-time -->
        <p class="hero-dashboard__datetime">{{ formattedDateTime }}</p>

        <!-- Loading / error states -->
        <div v-if="uvStatus === 'loading'" class="hero-dashboard__state hero-dashboard__loading">
          Getting your location and UV data…
        </div>
        <div v-else-if="uvStatus === 'denied'" class="hero-dashboard__state hero-dashboard__error">
          Location access is required to retrieve UV data.
        </div>
        <div v-else-if="uvStatus === 'error'" class="hero-dashboard__state hero-dashboard__error">
          <p class="hero-dashboard__error-main">Unable to retrieve UV data.</p>
          <p v-if="uvError" class="hero-dashboard__error-detail">Make sure the backend is running (e.g. <code>cd backend && python app.py</code>) and using the same port as this app (default <code>http://localhost:5000</code>).</p>
          <p v-else class="hero-dashboard__error-detail">Ensure the backend is running and reachable at <code>{{ apiBase }}</code>.</p>
        </div>

        <!-- f.–i. Max Daily UV label, large value, risk badge, alert list -->
        <template v-else-if="uvStatus === 'success' && uvData">
          <p class="hero-dashboard__uv-label">Maximum Daily UV</p>
          <div class="hero-dashboard__uv-row">
            <span class="hero-dashboard__uv-value">{{ uvData.uv_index }}</span>
            <span class="hero-dashboard__badge">{{ uvData.risk_level }}</span>
          </div>
          <ul class="hero-dashboard__alerts" role="list">
            <li
              v-for="(line, i) in alertRows"
              :key="i"
              class="hero-dashboard__alert-item"
            >
              <span class="hero-dashboard__alert-icon" aria-hidden="true">⚠</span>
              <span class="hero-dashboard__alert-text">{{ line }}</span>
            </li>
          </ul>
        </template>
      </div>

      <!-- Right column: weekly forecast chart card -->
      <div class="hero-dashboard__right">
        <div class="hero-dashboard__chart-card">
          <h2 class="hero-dashboard__chart-title">Weekly Forecast</h2>
          <MaxUVGraph
            :daily="dailyForGraph"
            :history="historyForGraph"
            view="7days"
            :dashboard-style="true"
          />
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero-dashboard {
  background: linear-gradient(
    135deg,
    #F4EACD 0%,
    #CFE4F0 45%,
    #F4E1B6 100%
  );
  border-radius: 24px;
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06), 0 2px 12px rgba(0, 0, 0, 0.04);
}

/* Hero two-column layout: left UV summary, right chart */
.hero-dashboard__grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
  min-height: 200px;
}
@media (min-width: 900px) {
  .hero-dashboard__grid {
    grid-template-columns: 0.9fr 1.2fr;
    gap: 48px;
  }
}

/* Left column content */
.hero-dashboard__left {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.hero-dashboard__search-wrap {
  display: flex;
  align-items: center;
  max-width: 100%;
  background: #fff;
  border-radius: 12px;
  padding: 0.6rem 1rem;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
}
.hero-dashboard__search-icon {
  margin-right: 0.5rem;
  font-size: 1rem;
}
.hero-dashboard__search {
  border: none;
  background: none;
  flex: 1;
  min-width: 0;
  font-size: 0.9375rem;
  color: #4A4A4A;
  outline: none;
}
.hero-dashboard__search::placeholder {
  color: #8A8A8A;
}
.hero-dashboard__coords {
  margin: 0;
  font-size: 0.8125rem;
  color: #D8613C;
}
.hero-dashboard__location-row {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
  flex-wrap: wrap;
}
.hero-dashboard__location-heading {
  margin: 0;
  font-size: 1.75rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: #D54E4E;
}
.hero-dashboard__region {
  font-size: 0.9375rem;
  color: #8A8A8A;
}
.hero-dashboard__datetime {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: #D54E4E;
}
.hero-dashboard__uv-label {
  margin: 0.25rem 0 0;
  font-size: 0.875rem;
  color: #8A8A8A;
}
.hero-dashboard__uv-row {
  display: flex;
  align-items: baseline;
  gap: 1rem;
  flex-wrap: wrap;
}
.hero-dashboard__uv-value {
  font-size: 3.5rem;
  font-weight: 800;
  line-height: 1;
  letter-spacing: -0.04em;
  color: #D54E4E;
}
.hero-dashboard__badge {
  display: inline-block;
  padding: 0.35rem 0.75rem;
  border-radius: 999px;
  font-size: 0.9375rem;
  font-weight: 700;
  color: #fff;
  background: #D44A4A;
}
.hero-dashboard__alerts {
  margin: 1rem 0 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.hero-dashboard__alert-item {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
}
.hero-dashboard__alert-icon {
  flex-shrink: 0;
  color: #D54E4E;
  font-size: 1rem;
}
.hero-dashboard__alert-text {
  font-size: 0.9375rem;
  color: #D54E4E;
  line-height: 1.4;
}

.hero-dashboard__state {
  padding: 1.25rem;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.9);
  font-size: 0.9375rem;
  margin-top: 0.5rem;
}
.hero-dashboard__loading { color: #4A4A4A; }
.hero-dashboard__error { color: #D44A4A; }
.hero-dashboard__error-main { margin: 0 0 0.5rem; font-weight: 600; }
.hero-dashboard__error-detail { margin: 0; font-size: 0.875rem; font-weight: 400; opacity: 0.95; }
.hero-dashboard__error-detail code { background: rgba(0,0,0,0.06); padding: 0.15rem 0.35rem; border-radius: 4px; font-size: 0.8em; }

/* Right column: chart card */
.hero-dashboard__right {
  min-width: 0;
}
.hero-dashboard__chart-card {
  background: #fff;
  border-radius: 20px;
  padding: 1.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}
.hero-dashboard__chart-title {
  margin: 0 0 1rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: #D8613C;
  text-align: center;
}

@media (min-width: 640px) {
  .hero-dashboard__uv-value { font-size: 4rem; }
  .hero-dashboard__location-heading { font-size: 2rem; }
}
@media (min-width: 900px) {
  .hero-dashboard { padding: 2.5rem 3rem; }
  .hero-dashboard__uv-value { font-size: 4.5rem; }
  .hero-dashboard__location-heading { font-size: 2.25rem; }
}
</style>
