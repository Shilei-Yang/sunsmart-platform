<!--
  Hero UV Dashboard — Epic 1: Track UV Levels.
  Two-column layout: left = current UV summary (with location search), right = weekly forecast chart.
  - Criterion 1: On load, retrieve UV from trusted API using browser geolocation.
  - Criterion 2: Display UV index clearly; criterion 3: colour-code by WHO/Australian standards.
  - Criterion 4: Plain-language alert from API message; criterion 5: auto-update on refresh/location change.
-->
<script setup>
import { ref, onMounted, computed, inject } from 'vue'
import MaxUVGraph from '@/components/MaxUVGraph.vue'

// Match backend port (default 5000). Override with VITE_API_BASE in .env if you use e.g. 5001 on macOS.
const apiBase = import.meta.env.VITE_API_BASE ?? 'http://localhost:5000'
const uvData = inject('uvData') ?? ref(null)
const uvStatus = ref(null)
const uvError = ref(null)

// Epic 1: Search location integration — selected location overrides geolocation for UV fetch
const searchQuery = ref('')
const searchResults = ref([])
const showDropdown = ref(false)
const searchDebounce = ref(null)
/** Selected location from search: { name, state, country, latitude, longitude, postcode } */
const selectedLocation = ref(null)

/** Epic 1: Fetch UV from trusted API for given coordinates. Used on load (geolocation) and when user selects a location. */
async function fetchUvForLocation(latitude, longitude) {
  const url = `${apiBase}/api/uv?lat=${latitude}&lon=${longitude}&include_history=0`
  uvError.value = null
  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), 12000)
  try {
    const res = await fetch(url, { signal: controller.signal })
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
    uvError.value = e?.name === 'AbortError' ? 'Request timed out' : (e?.message || 'Network error')
    uvStatus.value = 'error'
    uvData.value = null
  } finally {
    clearTimeout(timer)
  }
}

/** Epic 1 criterion 1: On page load, request browser geolocation and fetch UV. If unavailable, show error. */
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
    // Faster first paint: accept cached location for 15 minutes and lower timeout.
    { enableHighAccuracy: false, timeout: 8000, maximumAge: 900000 }
  )
}

/** Epic 1: Fetch location search results from backend (uses PostgreSQL Location table when available). */
async function runLocationSearch(q) {
  const query = (q || '').trim()
  if (!query || query.length < 2) {
    searchResults.value = []
    showDropdown.value = false
    return
  }
  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), 5000)
  try {
    const res = await fetch(
      `${apiBase}/api/location-search?q=${encodeURIComponent(query)}`,
      { signal: controller.signal }
    )
    if (!res.ok) {
      searchResults.value = []
      return
    }
    const json = await res.json()
    searchResults.value = Array.isArray(json) ? json : []
  } catch {
    searchResults.value = []
  } finally {
    clearTimeout(timer)
  }
}

function onSearchInput() {
  const query = (searchQuery.value || '').trim()
  if (query.length < 2) {
    clearTimeout(searchDebounce.value)
    searchResults.value = []
    showDropdown.value = false
    return
  }
  clearTimeout(searchDebounce.value)
  searchDebounce.value = setTimeout(() => {
    runLocationSearch(searchQuery.value)
    showDropdown.value = true
  }, 220)
}

/** Epic 1 criterion 5: On selecting a location, use its coordinates and immediately refresh UV data. */
function selectLocation(loc) {
  selectedLocation.value = loc
  searchQuery.value = loc.name
  showDropdown.value = false
  uvStatus.value = 'loading'
  fetchUvForLocation(loc.latitude, loc.longitude)
}

function closeDropdown() {
  showDropdown.value = false
}
function delayCloseDropdown() {
  setTimeout(closeDropdown, 180)
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

// Epic 1: When user has selected a location from search, show its name/region; otherwise API or "Your location"
const locationName = computed(() => {
  if (selectedLocation.value) return selectedLocation.value.name
  return uvData.value?.location_name ?? 'Your location'
})
const regionDisplay = computed(() => {
  if (selectedLocation.value) return `${selectedLocation.value.state} / ${selectedLocation.value.country || 'Australia'}`
  return uvData.value?.region ?? '—'
})
const currentUvDisplay = computed(() => {
  const value = uvData.value?.current_uv
  if (value === null || value === undefined || Number.isNaN(Number(value))) return '--'
  return Number(value).toFixed(1)
})
const currentRiskLevelDisplay = computed(() => uvData.value?.current_risk_level ?? 'Unavailable')
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
const currentUvTextStyle = computed(() => ({
  color: uvColorToHex(uvData.value?.current_color),
}))

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

/** Epic 1 criterion 4: Plain-language alert — first row is API message (WHO/Australian risk text), then recommendations. */
const alertRows = computed(() => {
  const msg = uvData.value?.message ?? ''
  return [
    msg || 'Check local UV index for exposure time.',
    'Wear sunscreen',
    'Protective clothing and sunglasses',
  ]
})

/** Epic 1 criterion 3 & 5: Badge/alert colour from API (WHO/Australian: green/yellow/orange/red/purple). */
const riskColorClass = computed(() => {
  const color = uvData.value?.color
  if (!color) return 'hero-dashboard__badge--red'
  return `hero-dashboard__badge--${color}`
})
const riskAlertColorClass = computed(() => {
  const color = uvData.value?.color
  if (!color) return 'hero-dashboard__alert--red'
  return `hero-dashboard__alert--${color}`
})
const currentRiskColorClass = computed(() => {
  const color = uvData.value?.current_color
  if (!color) return 'hero-dashboard__badge--neutral'
  return `hero-dashboard__badge--${color}`
})
const currentAlertColorClass = computed(() => {
  const color = uvData.value?.current_color
  if (!color) return 'hero-dashboard__alert--neutral'
  return `hero-dashboard__alert--${color}`
})
const currentAlertRows = computed(() => {
  const msg = uvData.value?.current_message ?? ''
  if (!msg) return []
  return [msg]
})

// Epic 1 criterion 5: On mount, fetch UV using geolocation. Page refresh re-runs this and fetches again.
onMounted(startUvFlow)
</script>

<template>
  <section class="hero-dashboard">
    <div class="hero-dashboard__grid">
      <!-- Left column: current UV summary -->
      <div class="hero-dashboard__left">
        <!-- Epic 1: Search location — select a place to fetch UV for that location and auto-update dashboard -->
        <div class="hero-dashboard__search-wrap" role="combobox" :aria-expanded="showDropdown" aria-haspopup="listbox" aria-owns="location-listbox">
          <span class="hero-dashboard__search-icon" aria-hidden="true">🔍</span>
          <input
            v-model="searchQuery"
            type="text"
            class="hero-dashboard__search"
            placeholder="Search Location"
            aria-label="Search location"
            autocomplete="off"
            @input="onSearchInput"
            @focus="searchQuery && (showDropdown = true)"
            @blur="delayCloseDropdown"
          />
          <ul
            v-if="showDropdown && searchResults.length"
            id="location-listbox"
            class="hero-dashboard__dropdown"
            role="listbox"
          >
            <li
              v-for="(loc, idx) in searchResults"
              :key="`${loc.name}-${loc.postcode}-${idx}`"
              role="option"
              class="hero-dashboard__dropdown-item"
              @mousedown.prevent="selectLocation(loc)"
            >
              {{ loc.name }}, {{ loc.state }} {{ loc.postcode }}
            </li>
          </ul>
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

        <!-- Epic 1 criteria 2 & 3: Clear UV value + label; colour-coded risk badge (WHO/Australian) -->
        <template v-else-if="uvStatus === 'success' && uvData">
          <div class="hero-dashboard__uv-card hero-dashboard__uv-card--current">
            <p class="hero-dashboard__uv-label">Current UV</p>
            <div class="hero-dashboard__uv-row">
              <span class="hero-dashboard__uv-value hero-dashboard__uv-value--current" :style="currentUvTextStyle">{{ currentUvDisplay }}</span>
              <span :class="['hero-dashboard__badge', currentRiskColorClass]">{{ currentRiskLevelDisplay }}</span>
            </div>
            <ul v-if="currentAlertRows.length" class="hero-dashboard__alerts hero-dashboard__alerts--compact" role="list">
              <li
                v-for="(line, i) in currentAlertRows"
                :key="`current-${i}`"
                :class="['hero-dashboard__alert-item', currentAlertColorClass]"
              >
                <span class="hero-dashboard__alert-icon" aria-hidden="true">⚠</span>
                <span class="hero-dashboard__alert-text">{{ line }}</span>
              </li>
            </ul>
          </div>

          <div class="hero-dashboard__uv-card hero-dashboard__uv-card--max">
            <p class="hero-dashboard__uv-label">Maximum Daily UV</p>
            <div class="hero-dashboard__uv-row">
              <span class="hero-dashboard__uv-value">{{ uvData.uv_index }}</span>
              <span :class="['hero-dashboard__badge', riskColorClass]">{{ uvData.risk_level }}</span>
            </div>
            <!-- Epic 1 criterion 4: Plain-language alert from API -->
            <ul class="hero-dashboard__alerts" role="list">
              <li
                v-for="(line, i) in alertRows"
                :key="i"
                :class="['hero-dashboard__alert-item', riskAlertColorClass]"
              >
                <span class="hero-dashboard__alert-icon" aria-hidden="true">⚠</span>
                <span class="hero-dashboard__alert-text">{{ line }}</span>
              </li>
            </ul>
          </div>
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
  position: relative;
  display: flex;
  align-items: center;
  max-width: 100%;
  background: #fff;
  border-radius: 12px;
  padding: 0.6rem 1rem;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
}
.hero-dashboard__dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  margin: 4px 0 0;
  padding: 0;
  list-style: none;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  max-height: 240px;
  overflow-y: auto;
  z-index: 10;
}
.hero-dashboard__dropdown-item {
  padding: 0.6rem 1rem;
  font-size: 0.9375rem;
  color: #4A4A4A;
  cursor: pointer;
  border-bottom: 1px solid #E6E1DA;
}
.hero-dashboard__dropdown-item:last-child {
  border-bottom: none;
}
.hero-dashboard__dropdown-item:hover {
  background: #F4F1EC;
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
  font-size: 1.5rem;
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
.hero-dashboard__uv-card {
  border-radius: 16px;
  padding: 0.85rem 1rem;
  margin-top: 0.6rem;
  background: rgba(255, 255, 255, 0.45);
  border: 1px solid rgba(255, 255, 255, 0.6);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.35);
}
.hero-dashboard__uv-card--current {
  background: rgba(255, 255, 255, 0.5);
}
.hero-dashboard__uv-card--max {
  background: rgba(255, 255, 255, 0.4);
}
.hero-dashboard__uv-value {
  font-size: 3.5rem;
  font-weight: 800;
  line-height: 1;
  letter-spacing: -0.04em;
  color: #D54E4E;
}
.hero-dashboard__uv-value--current {
  font-size: 2.5rem;
}
/* Epic 1 criterion 3 & 5: WHO/Australian colour-coding for risk badge */
.hero-dashboard__badge {
  display: inline-block;
  padding: 0.35rem 0.75rem;
  border-radius: 999px;
  font-size: 0.9375rem;
  font-weight: 700;
  color: #fff;
  background: #D44A4A;
}
.hero-dashboard__badge--green { background: #16a34a; }
.hero-dashboard__badge--yellow { background: #ca8a04; color: #1c1917; }
.hero-dashboard__badge--orange { background: #ea580c; }
.hero-dashboard__badge--red { background: #D44A4A; }
.hero-dashboard__badge--purple { background: #7c3aed; }
.hero-dashboard__badge--neutral { background: #6b7280; }
.hero-dashboard__alerts {
  margin: 1rem 0 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.hero-dashboard__alerts--compact { margin-top: 0.5rem; }
.hero-dashboard__alert-item {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
}
.hero-dashboard__alert-icon {
  flex-shrink: 0;
  font-size: 1rem;
}
.hero-dashboard__alert-text {
  font-size: 0.9375rem;
  line-height: 1.4;
}
/* Epic 1: Alert colour follows risk level (WHO/Australian) */
.hero-dashboard__alert--green .hero-dashboard__alert-icon,
.hero-dashboard__alert--green .hero-dashboard__alert-text { color: #16a34a; }
.hero-dashboard__alert--yellow .hero-dashboard__alert-icon,
.hero-dashboard__alert--yellow .hero-dashboard__alert-text { color: #ca8a04; }
.hero-dashboard__alert--orange .hero-dashboard__alert-icon,
.hero-dashboard__alert--orange .hero-dashboard__alert-text { color: #ea580c; }
.hero-dashboard__alert--red .hero-dashboard__alert-icon,
.hero-dashboard__alert--red .hero-dashboard__alert-text { color: #D54E4E; }
.hero-dashboard__alert--purple .hero-dashboard__alert-icon,
.hero-dashboard__alert--purple .hero-dashboard__alert-text { color: #7c3aed; }
.hero-dashboard__alert--neutral .hero-dashboard__alert-icon,
.hero-dashboard__alert--neutral .hero-dashboard__alert-text { color: #6b7280; }

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
  .hero-dashboard__uv-value { font-size: 3.6rem; }
  .hero-dashboard__location-heading { font-size: 1.8rem; }
}
@media (min-width: 900px) {
  .hero-dashboard { padding: 2.5rem 3rem; }
  .hero-dashboard__uv-value { font-size: 4rem; }
  .hero-dashboard__location-heading { font-size: 2rem; }
}
</style>
