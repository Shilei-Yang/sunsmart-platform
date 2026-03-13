<!--
  Hero UV Dashboard — Large, prototype-style section with blue gradient.
  Fetches /api/uv on load via geolocation; displays location, date/time, large UV value,
  risk badge, graph panel, and warning banner. API integration unchanged.
-->
<script setup>
import { ref, onMounted, computed } from 'vue'
import MaxUVGraph from '@/components/MaxUVGraph.vue'

const apiBase = import.meta.env.VITE_API_BASE ?? 'http://localhost:5001'
const uvData = ref(null)
const uvStatus = ref(null)
const timeFrame = ref('today')

async function fetchUvForLocation(latitude, longitude) {
  const url = `${apiBase}/api/uv?lat=${latitude}&lon=${longitude}`
  try {
    const res = await fetch(url)
    if (!res.ok) {
      uvStatus.value = 'error'
      uvData.value = null
      return
    }
    const json = await res.json()
    uvData.value = json
    uvStatus.value = 'success'
  } catch {
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

// Clean coordinate display for hero location heading
const locationDisplay = computed(() => {
  if (!uvData.value) return null
  const { latitude, longitude } = uvData.value
  return `${latitude.toFixed(2)}°, ${longitude.toFixed(2)}°`
})

const dailyForGraph = computed(() => {
  if (!uvData.value?.daily) return []
  return uvData.value.daily
})

// Past 7 days history (backend provides uvData.history); fallback to mock if not available yet.
const historyForGraph = computed(() => {
  if (Array.isArray(uvData.value?.history) && uvData.value.history.length) return uvData.value.history

  // Temporary mock data for styling if backend history is unavailable.
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

onMounted(startUvFlow)
</script>

<template>
  <section class="hero-dashboard">
    <!-- Top bar: search + user avatar -->
    <header class="hero-dashboard__top">
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
      <div class="hero-dashboard__avatar" aria-hidden="true">M</div>
    </header>

    <!-- Location as main heading + subtitle -->
    <div class="hero-dashboard__location-block">
      <h1 class="hero-dashboard__location-heading">
        {{ locationDisplay ?? 'Your location' }}
      </h1>
      <p class="hero-dashboard__location-sub">Your location</p>
    </div>

    <!-- Timeframe tabs + date/time -->
    <div class="hero-dashboard__tabs-row">
      <div class="hero-dashboard__tabs">
        <button
          type="button"
          class="hero-dashboard__tab"
          :class="{ 'hero-dashboard__tab--active': timeFrame === 'today' }"
          @click="timeFrame = 'today'"
        >
          Today
        </button>
        <button
          type="button"
          class="hero-dashboard__tab"
          :class="{ 'hero-dashboard__tab--active': timeFrame === '7days' }"
          @click="timeFrame = '7days'"
        >
          7 Days
        </button>
        <button
          type="button"
          class="hero-dashboard__tab"
          :class="{ 'hero-dashboard__tab--active': timeFrame === 'past' }"
          @click="timeFrame = 'past'"
        >
          Past
        </button>
      </div>
      <p class="hero-dashboard__datetime">{{ formattedDateTime }}</p>
    </div>

    <!-- Loading / error states -->
    <div v-if="uvStatus === 'loading'" class="hero-dashboard__state hero-dashboard__loading">
      Getting your location and UV data…
    </div>
    <div v-else-if="uvStatus === 'denied'" class="hero-dashboard__state hero-dashboard__error">
      Location access is required to retrieve UV data.
    </div>
    <div v-else-if="uvStatus === 'error'" class="hero-dashboard__state hero-dashboard__error">
      Unable to retrieve UV data.
    </div>

    <!-- Success: large UV value + badge, graph, warning banner -->
    <template v-else-if="uvStatus === 'success' && uvData">
      <div class="hero-dashboard__uv-row">
        <span class="hero-dashboard__uv-value">{{ uvData.uv_index }}</span>
        <span :class="['hero-dashboard__badge', `hero-dashboard__badge--${uvData.color}`]">
          {{ uvData.risk_level }}
        </span>
      </div>
      <p class="hero-dashboard__uv-label">Max UV Index</p>

      <!-- Graph panel (prototype-style; daily max only) -->
      <div class="hero-dashboard__graph-panel">
        <MaxUVGraph
          :daily="dailyForGraph"
          :history="historyForGraph"
          :view="timeFrame === 'past' ? 'past' : timeFrame === '7days' ? '7days' : 'today'"
        />
      </div>

      <!-- Warning banner below graph -->
      <div class="hero-dashboard__warning" role="alert">
        <span class="hero-dashboard__warning-icon" aria-hidden="true">⚠</span>
        <span class="hero-dashboard__warning-text">{{ uvData.message }}</span>
      </div>
    </template>
  </section>
</template>

<style scoped>
.hero-dashboard {
  background: linear-gradient(165deg, #0ea5e9 0%, #38bdf8 25%, #7dd3fc 50%, #bae6fd 100%);
  border-radius: 20px;
  padding: 2rem 2rem 2.5rem;
  box-shadow: 0 10px 40px -10px rgba(14, 165, 233, 0.35), 0 4px 12px -4px rgba(0, 0, 0, 0.08);
  color: #0f172a;
}

.hero-dashboard__top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.hero-dashboard__search-wrap {
  display: flex;
  align-items: center;
  flex: 1;
  max-width: 320px;
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  padding: 0.6rem 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}
.hero-dashboard__search-icon { margin-right: 0.5rem; font-size: 1rem; }
.hero-dashboard__search {
  border: none;
  background: none;
  width: 100%;
  font-size: 0.9375rem;
  color: #1e293b;
  outline: none;
}
.hero-dashboard__avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: rgba(30, 41, 59, 0.85);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.hero-dashboard__location-block {
  margin-bottom: 1rem;
}
.hero-dashboard__location-heading {
  margin: 0;
  font-size: 1.75rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  color: #0f172a;
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.5);
}
.hero-dashboard__location-sub {
  margin: 0.25rem 0 0;
  font-size: 0.875rem;
  color: rgba(15, 23, 42, 0.75);
}

.hero-dashboard__tabs-row {
  margin-bottom: 1.25rem;
}
.hero-dashboard__tabs {
  display: flex;
  gap: 0.25rem;
  margin-bottom: 0.5rem;
}
.hero-dashboard__tab {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: rgba(15, 23, 42, 0.8);
  background: rgba(255, 255, 255, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.4);
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s;
}
.hero-dashboard__tab:hover {
  background: rgba(255, 255, 255, 0.4);
  border-color: rgba(255, 255, 255, 0.6);
}
.hero-dashboard__tab--active {
  background: #fff;
  border-color: #fff;
  color: #0369a1;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}
.hero-dashboard__datetime {
  margin: 0;
  font-size: 0.8125rem;
  color: rgba(15, 23, 42, 0.75);
}

.hero-dashboard__state {
  padding: 1.5rem;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.9);
  font-size: 0.9375rem;
}
.hero-dashboard__loading { color: #475569; }
.hero-dashboard__error { color: #b91c1c; font-weight: 600; }

.hero-dashboard__uv-row {
  display: flex;
  align-items: baseline;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 0.25rem;
}
.hero-dashboard__uv-value {
  font-size: 4rem;
  font-weight: 800;
  line-height: 1;
  letter-spacing: -0.04em;
  color: #0f172a;
  text-shadow: 0 2px 4px rgba(255, 255, 255, 0.4);
}
.hero-dashboard__badge {
  display: inline-block;
  padding: 0.4rem 0.85rem;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}
.hero-dashboard__badge--green { background: #dcfce7; color: #166534; }
.hero-dashboard__badge--yellow { background: #fef9c3; color: #854d0e; }
.hero-dashboard__badge--orange { background: #ffedd5; color: #c2410c; }
.hero-dashboard__badge--red { background: #fee2e2; color: #b91c1c; }
.hero-dashboard__badge--purple { background: #ede9fe; color: #5b21b6; }
.hero-dashboard__uv-label {
  margin: 0 0 1.25rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: rgba(15, 23, 42, 0.8);
}

.hero-dashboard__graph-panel {
  margin-bottom: 1.25rem;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.5);
}

.hero-dashboard__warning {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 1.25rem 1.5rem;
  background: #fff;
  border-radius: 12px;
  border-left: 5px solid #dc2626;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}
.hero-dashboard__warning-icon {
  flex-shrink: 0;
  font-size: 1.5rem;
}
.hero-dashboard__warning-text {
  font-size: 1rem;
  line-height: 1.55;
  color: #374151;
  font-weight: 500;
}

@media (min-width: 640px) {
  .hero-dashboard__uv-value { font-size: 4.5rem; }
  .hero-dashboard__location-heading { font-size: 2rem; }
}
@media (min-width: 900px) {
  .hero-dashboard { padding: 2.5rem 3rem 3rem; }
  .hero-dashboard__uv-value { font-size: 5rem; }
  .hero-dashboard__location-heading { font-size: 2.25rem; }
}
</style>
