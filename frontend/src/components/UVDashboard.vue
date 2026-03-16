<!--
  Hero UV Dashboard — Epic 1: Track UV Levels.
  Two-column layout: left = current UV summary (with location search), right = weekly forecast chart.
  Redesigned: clean white card with accent stripe, dynamic risk-coloured UV values and borders.
-->
<script setup>
import { ref, onMounted, computed, inject } from 'vue'
import MaxUVGraph from '@/components/MaxUVGraph.vue'

const apiBase = import.meta.env.VITE_API_BASE ?? 'http://localhost:5000'
const uvData = inject('uvData') ?? ref(null)
const uvStatus = ref(null)
const uvError = ref(null)

const searchQuery = ref('')
const searchResults = ref([])
const showDropdown = ref(false)
const searchDebounce = ref(null)
const selectedLocation = ref(null)
const searchFeedback = ref(null)
const searchFeedbackType = ref('info')
const isBackToCurrentLoading = ref(false)

let currentUvController = null
let currentUvRequestId = 0

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

async function fetchUvForLocation(latitude, longitude) {
  const url = `${apiBase}/api/uv?lat=${latitude}&lon=${longitude}&include_history=0`
  uvError.value = null
  currentUvRequestId += 1
  const requestId = currentUvRequestId

  if (currentUvController) currentUvController.abort()
  const maxAttempts = 3

  for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
    const controller = new AbortController()
    currentUvController = controller
    const timer = setTimeout(() => controller.abort(), 15000)
    try {
      const res = await fetch(url, { signal: controller.signal })
      if (requestId !== currentUvRequestId) return

      if (!res.ok) {
        const retryable = [429, 502, 503, 504].includes(res.status)
        if (retryable && attempt < maxAttempts) {
          await sleep(attempt * 1000)
          continue
        }
        uvError.value = 'Unable to retrieve UV data at the moment. Please try again later.'
        uvStatus.value = 'error'
        uvData.value = null
        return
      }

      const json = await res.json()
      if (requestId !== currentUvRequestId) return
      uvData.value = json
      uvStatus.value = 'success'
      return
    } catch {
      if (requestId !== currentUvRequestId) return
      if (attempt < maxAttempts) {
        await sleep(attempt * 1000)
        continue
      }
      uvError.value = 'Unable to retrieve UV data at the moment. Please try again later.'
      uvStatus.value = 'error'
      uvData.value = null
      return
    } finally {
      clearTimeout(timer)
    }
  }
}

function startUvFlow({ resetSelected = false } = {}) {
  if (resetSelected) {
    selectedLocation.value = null
    searchQuery.value = ''
  }
  searchFeedback.value = null
  uvStatus.value = 'loading'
  uvData.value = null
  if (!navigator.geolocation) {
    uvStatus.value = 'denied'
    uvError.value = 'Location access was denied. Please enable location permission or search for a city manually.'
    return
  }
  navigator.geolocation.getCurrentPosition(
    (position) => {
      const { latitude, longitude } = position.coords
      fetchUvForLocation(latitude, longitude)
      isBackToCurrentLoading.value = false
    },
    (err) => {
      if (err?.code === 1) {
        uvStatus.value = 'denied'
        uvError.value = 'Location access was denied. Please enable location permission or search for a city manually.'
        isBackToCurrentLoading.value = false
        return
      }
      uvStatus.value = 'error'
      uvError.value = 'Unable to retrieve UV data at the moment. Please try again later.'
      isBackToCurrentLoading.value = false
    },
    { enableHighAccuracy: false, timeout: 8000, maximumAge: 900000 }
  )
}

async function runLocationSearch(q) {
  const query = (q || '').trim()
  if (!query || query.length < 2) {
    searchFeedback.value = null
    searchResults.value = []
    showDropdown.value = false
    return
  }
  searchFeedback.value = null
  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), 5000)
  try {
    const res = await fetch(
      `${apiBase}/api/location-search?q=${encodeURIComponent(query)}`,
      { signal: controller.signal }
    )
    if (!res.ok) {
      searchResults.value = []
      showDropdown.value = false
      searchFeedbackType.value = 'error'
      searchFeedback.value = 'Location search is temporarily unavailable. Please try again later.'
      return
    }
    const json = await res.json()
    searchResults.value = Array.isArray(json) ? json : []
    if (!searchResults.value.length) {
      showDropdown.value = false
      searchFeedbackType.value = 'info'
      searchFeedback.value = 'Please enter a valid city, suburb, or address. This platform currently supports locations within Australia only.'
      return
    }
    searchFeedback.value = null
  } catch {
    searchResults.value = []
    showDropdown.value = false
    searchFeedbackType.value = 'error'
    searchFeedback.value = 'Location search is temporarily unavailable. Please try again later.'
  }
  finally { clearTimeout(timer) }
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

function selectLocation(loc) {
  selectedLocation.value = loc
  searchQuery.value = loc.name
  showDropdown.value = false
  searchFeedback.value = null
  uvStatus.value = 'loading'
  fetchUvForLocation(loc.latitude, loc.longitude)
}

function backToCurrentLocation() {
  showDropdown.value = false
  searchResults.value = []
  isBackToCurrentLoading.value = true
  startUvFlow({ resetSelected: true })
}

function closeDropdown() { showDropdown.value = false }
function delayCloseDropdown() { setTimeout(closeDropdown, 180) }

const formattedDateTime = computed(() => {
  const d = new Date()
  return d.toLocaleDateString('en-AU', {
    weekday: 'long', day: 'numeric', month: 'long', year: 'numeric',
    hour: 'numeric', minute: '2-digit',
  })
})

const coordinatesDisplay = computed(() => {
  if (!uvData.value) return null
  const { latitude, longitude } = uvData.value
  const latDir = latitude >= 0 ? 'N' : 'S'
  const lonDir = longitude >= 0 ? 'E' : 'W'
  return `${Math.abs(latitude).toFixed(4)}° ${latDir}, ${Math.abs(longitude).toFixed(4)}° ${lonDir}`
})

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

function uvGlowShadow(color) {
  const hex = uvColorToHex(color)
  return `0 0 18px ${hex}40, 0 0 6px ${hex}25`
}
const currentUvTextStyle = computed(() => ({
  color: uvColorToHex(uvData.value?.current_color),
  textShadow: uvGlowShadow(uvData.value?.current_color),
}))
const maxUvTextStyle = computed(() => ({
  color: uvColorToHex(uvData.value?.color),
  textShadow: uvGlowShadow(uvData.value?.color),
}))
const currentUvBorderStyle = computed(() => ({ borderLeftColor: uvColorToHex(uvData.value?.current_color) }))
const maxUvBorderStyle = computed(() => ({ borderLeftColor: uvColorToHex(uvData.value?.color) }))

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

const maxUvPlanningMessage = computed(() => {
  const uvIndex = Number(uvData.value?.uv_index ?? NaN)
  if (Number.isNaN(uvIndex)) return null
  if (uvIndex <= 2) return 'Low peak UV; protection mainly for long outdoor time or near water.'
  if (uvIndex <= 5) return 'Moderate peak UV; use sun protection, especially around midday.'
  if (uvIndex <= 7) return 'High peak UV; favour early/late outings and use full protection.'
  if (uvIndex <= 10) return 'Very high peak UV; limit midday sun and use full protection.'
  return 'Extreme peak UV; avoid midday sun and use maximum protection.'
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

onMounted(startUvFlow)
</script>

<template>
  <section class="hero-dashboard">
    <div class="hero-dashboard__grid">
      <!-- Left column -->
      <div class="hero-dashboard__left">
        <!-- Search -->
        <div class="hero-dashboard__search-row">
          <div class="hero-dashboard__search-wrap" role="combobox" :aria-expanded="showDropdown" aria-haspopup="listbox" aria-owns="location-listbox">
            <svg class="hero-dashboard__search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <circle cx="11" cy="11" r="8" /><path d="m21 21-4.3-4.3" />
            </svg>
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
            <ul v-if="showDropdown && searchResults.length" id="location-listbox" class="hero-dashboard__dropdown" role="listbox">
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
          <button type="button" class="hero-dashboard__back-btn" :disabled="isBackToCurrentLoading || uvStatus === 'loading'" @click="backToCurrentLocation">
            {{ isBackToCurrentLoading || uvStatus === 'loading' ? 'Loading…' : 'Back to Current' }}
          </button>
        </div>
        <p
          v-if="searchFeedback"
          :class="['hero-dashboard__search-feedback', `hero-dashboard__search-feedback--${searchFeedbackType}`]"
        >
          {{ searchFeedback }}
        </p>

        <p v-if="coordinatesDisplay" class="hero-dashboard__coords">{{ coordinatesDisplay }}</p>

        <div class="hero-dashboard__location-block">
          <h1 class="hero-dashboard__location-heading">{{ locationName }}</h1>
          <span class="hero-dashboard__region">{{ regionDisplay }}</span>
        </div>

        <p class="hero-dashboard__datetime">{{ formattedDateTime }}</p>

        <!-- States -->
        <div v-if="uvStatus === 'loading'" class="hero-dashboard__state hero-dashboard__loading">Getting your location and UV data…</div>
        <div v-else-if="uvStatus === 'denied'" class="hero-dashboard__state hero-dashboard__error">
          <p class="hero-dashboard__error-main">Location access was denied.</p>
          <p class="hero-dashboard__error-detail">Please enable location permission or search for a city manually.</p>
        </div>
        <div v-else-if="uvStatus === 'error'" class="hero-dashboard__state hero-dashboard__error">
          <p class="hero-dashboard__error-main">Unable to retrieve UV data at the moment.</p>
          <p class="hero-dashboard__error-detail">{{ uvError || 'Please try again later.' }}</p>
        </div>

        <!-- UV readings -->
        <template v-else-if="uvStatus === 'success' && uvData">
          <div class="hero-dashboard__uv-card hero-dashboard__uv-card--accented" :style="currentUvBorderStyle">
            <div class="hero-dashboard__uv-card-header">
              <span class="hero-dashboard__uv-card-dot hero-dashboard__uv-card-dot--live" />
              <p class="hero-dashboard__uv-label">Current UV</p>
            </div>
            <div class="hero-dashboard__uv-row">
              <span class="hero-dashboard__uv-value hero-dashboard__uv-value--current" :style="currentUvTextStyle">{{ currentUvDisplay }}</span>
              <span :class="['hero-dashboard__badge', currentRiskColorClass]">{{ currentRiskLevelDisplay }}</span>
            </div>
            <div v-if="currentAlertRows.length" class="hero-dashboard__alert-wrap">
              <p v-for="(line, i) in currentAlertRows" :key="`current-${i}`" :class="['hero-dashboard__alert-text', currentAlertColorClass]">{{ line }}</p>
            </div>
          </div>

          <div class="hero-dashboard__uv-card hero-dashboard__uv-card--accented" :style="maxUvBorderStyle">
            <div class="hero-dashboard__uv-card-header">
              <span class="hero-dashboard__uv-card-dot" />
              <p class="hero-dashboard__uv-label">Maximum Daily UV</p>
            </div>
            <div class="hero-dashboard__uv-row">
              <span class="hero-dashboard__uv-value" :style="maxUvTextStyle">{{ uvData.uv_index }}</span>
              <span :class="['hero-dashboard__badge', riskColorClass]">{{ uvData.risk_level }}</span>
            </div>
            <p v-if="maxUvPlanningMessage" :class="['hero-dashboard__planning', riskAlertColorClass]">{{ maxUvPlanningMessage }}</p>
          </div>
        </template>
      </div>

      <!-- Right column: chart -->
      <div class="hero-dashboard__right">
        <div class="hero-dashboard__chart-card">
          <p class="hero-dashboard__chart-eyebrow">7-Day Outlook</p>
          <h2 class="hero-dashboard__chart-title">Weekly Forecast</h2>
          <MaxUVGraph :daily="dailyForGraph" :history="historyForGraph" view="7days" :dashboard-style="true" />
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
/* ─── Main container ─── */
.hero-dashboard {
  position: relative;
  background: linear-gradient(
    135deg,
    #F4EACD 0%,
    #CFE4F0 45%,
    #F4E1B6 100%
  );
  border-radius: 24px;
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06), 0 2px 12px rgba(0, 0, 0, 0.04);
  overflow: hidden;
}

/* ─── Grid ─── */
.hero-dashboard__grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
  min-height: 200px;
}

/* ─── Left column ─── */
.hero-dashboard__left {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

/* Search */
.hero-dashboard__search-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.hero-dashboard__search-wrap {
  position: relative;
  display: flex;
  align-items: center;
  flex: 1;
  background: #fff;
  border: 1px solid rgba(255, 255, 255, 0.7);
  border-radius: 12px;
  padding: 0.55rem 0.9rem;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
  transition: border-color 0.2s, box-shadow 0.2s;
}
.hero-dashboard__search-wrap:focus-within {
  border-color: var(--uv-primary, #D8613C);
  box-shadow: 0 0 0 3px rgba(216, 97, 60, 0.1);
}
.hero-dashboard__search-icon {
  flex-shrink: 0;
  margin-right: 0.5rem;
  color: var(--uv-text-muted, #8A8A8A);
  width: 16px; height: 16px;
}
.hero-dashboard__search {
  border: none; background: none;
  flex: 1; min-width: 0;
  font-size: 0.875rem;
  color: var(--uv-text, #4A4A4A);
  outline: none;
}
.hero-dashboard__search::placeholder { color: var(--uv-text-muted, #8A8A8A); }
.hero-dashboard__back-btn {
  border: 1px solid rgba(216, 97, 60, 0.35);
  background: rgba(255, 255, 255, 0.85);
  color: #B75233;
  border-radius: 10px;
  padding: 0.5rem 0.75rem;
  font-size: 0.78rem;
  font-weight: 700;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s ease;
}
.hero-dashboard__back-btn:hover {
  background: #fff;
  border-color: rgba(216, 97, 60, 0.55);
}
.hero-dashboard__search-feedback {
  margin: 0.2rem 0 0;
  font-size: 0.8rem;
  line-height: 1.4;
  padding: 0.5rem 0.65rem;
  border-radius: 10px;
}
.hero-dashboard__search-feedback--info {
  color: #7A3E28;
  background: rgba(216, 97, 60, 0.12);
}
.hero-dashboard__search-feedback--error {
  color: #B42318;
  background: rgba(180, 35, 24, 0.1);
}

/* Dropdown */
.hero-dashboard__dropdown {
  position: absolute;
  top: calc(100% + 4px); left: 0; right: 0;
  margin: 0; padding: 0.25rem 0; list-style: none;
  background: var(--uv-card, #fff);
  border: 1px solid var(--uv-grid, #E6E1DA);
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  max-height: 240px; overflow-y: auto; z-index: 10;
}
.hero-dashboard__dropdown-item {
  padding: 0.55rem 0.9rem;
  font-size: 0.875rem;
  color: var(--uv-text, #4A4A4A);
  cursor: pointer;
  transition: background 0.15s;
}
.hero-dashboard__dropdown-item:hover { background: var(--uv-bg, #F4F1EC); }

/* Coordinates */
.hero-dashboard__coords {
  margin: 0.15rem 0 0;
  font-size: 0.75rem; font-weight: 600;
  letter-spacing: 0.04em;
  color: var(--uv-primary, #D8613C);
}

/* Location */
.hero-dashboard__location-block {
  display: flex; align-items: baseline; gap: 0.5rem; flex-wrap: wrap;
}
.hero-dashboard__location-heading {
  margin: 0;
  font-size: 1.5rem; font-weight: 800;
  letter-spacing: -0.02em;
  color: var(--uv-text, #4A4A4A);
}
.hero-dashboard__region {
  font-size: 0.875rem;
  color: var(--uv-text-muted, #8A8A8A);
}

/* Date-time */
.hero-dashboard__datetime {
  margin: 0;
  font-size: 0.8125rem; font-weight: 600;
  color: var(--uv-primary, #D8613C);
  letter-spacing: 0.01em;
}

/* ─── UV cards ─── */
.hero-dashboard__uv-card {
  border-radius: 16px;
  padding: 0.85rem 1.15rem;
  margin-top: 0.35rem;
  background: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.6);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.35);
  transition: box-shadow 0.2s;
}
.hero-dashboard__uv-card:hover { box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06); }
.hero-dashboard__uv-card--accented { border-left: 3px solid rgba(255, 255, 255, 0.6); }

.hero-dashboard__uv-card-header {
  display: flex; align-items: center; gap: 0.4rem; margin-bottom: 0.15rem;
}
.hero-dashboard__uv-card-dot {
  width: 7px; height: 7px; border-radius: 50%;
  background: var(--uv-grid, #ccc); flex-shrink: 0;
}
.hero-dashboard__uv-card-dot--live {
  background: #16a34a;
  box-shadow: 0 0 0 2px rgba(22, 163, 74, 0.2);
}

.hero-dashboard__uv-label {
  margin: 0;
  font-size: 0.75rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.08em;
  color: var(--uv-text-muted, #8A8A8A);
}
.hero-dashboard__uv-row {
  display: flex; align-items: baseline; gap: 0.75rem; flex-wrap: wrap;
}
.hero-dashboard__uv-value {
  font-size: 3rem; font-weight: 800;
  line-height: 1.1; letter-spacing: -0.04em;
  color: var(--uv-text, #4A4A4A);
}
.hero-dashboard__uv-value--current { font-size: 2.5rem; }

/* Badge */
.hero-dashboard__badge {
  display: inline-flex; align-items: center;
  padding: 0.25rem 0.7rem; border-radius: 999px;
  font-size: 0.75rem; font-weight: 700; letter-spacing: 0.02em;
  color: #fff; background: #D44A4A;
}
.hero-dashboard__badge--green  { background: #16a34a; }
.hero-dashboard__badge--yellow { background: #ca8a04; color: #1c1917; }
.hero-dashboard__badge--orange { background: #ea580c; }
.hero-dashboard__badge--red    { background: #D44A4A; }
.hero-dashboard__badge--purple { background: #7c3aed; }
.hero-dashboard__badge--neutral { background: #6b7280; }

/* Alert text */
.hero-dashboard__alert-wrap { margin-top: 0.5rem; }
.hero-dashboard__alert-text {
  margin: 0; font-size: 0.8125rem; line-height: 1.5;
  color: var(--uv-text-muted, #8A8A8A);
}
.hero-dashboard__alert--green  { color: #16a34a; }
.hero-dashboard__alert--yellow { color: #ca8a04; }
.hero-dashboard__alert--orange { color: #ea580c; }
.hero-dashboard__alert--red    { color: #D54E4E; }
.hero-dashboard__alert--purple { color: #7c3aed; }
.hero-dashboard__alert--neutral { color: #6b7280; }

/* Planning */
.hero-dashboard__planning {
  margin: 0.5rem 0 0; font-size: 0.8125rem; line-height: 1.5;
  color: var(--uv-text-muted, #8A8A8A);
}

/* States */
.hero-dashboard__state {
  padding: 1.25rem; border-radius: 14px;
  background: rgba(255, 255, 255, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.6);
  font-size: 0.875rem; margin-top: 0.5rem;
}
.hero-dashboard__loading { color: var(--uv-text, #4A4A4A); }
.hero-dashboard__error   { color: var(--uv-danger, #D44A4A); }
.hero-dashboard__error-main   { margin: 0 0 0.5rem; font-weight: 600; }
.hero-dashboard__error-detail { margin: 0; font-size: 0.8125rem; font-weight: 400; opacity: 0.9; }
.hero-dashboard__error-detail code {
  background: rgba(0, 0, 0, 0.05); padding: 0.15rem 0.35rem;
  border-radius: 4px; font-size: 0.8em;
}

/* ─── Right column ─── */
.hero-dashboard__right {
  min-width: 0; display: flex; flex-direction: column;
}
.hero-dashboard__chart-card {
  flex: 1;
  background: #fff;
  border-radius: 20px;
  padding: 1.25rem 1.25rem 1rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  display: flex; flex-direction: column; justify-content: center;
}
.hero-dashboard__chart-eyebrow {
  margin: 0 0 0.1rem;
  font-size: 0.6875rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.12em;
  color: var(--uv-primary, #D8613C); text-align: center;
}
.hero-dashboard__chart-title {
  margin: 0 0 0.5rem;
  font-size: 1.1rem; font-weight: 800;
  color: var(--uv-text, #4A4A4A);
  text-align: center; letter-spacing: -0.02em;
}

/* ─── Responsive ─── */
@media (min-width: 640px) {
  .hero-dashboard__uv-value { font-size: 3.25rem; }
  .hero-dashboard__location-heading { font-size: 1.75rem; }
}
@media (min-width: 900px) {
  .hero-dashboard { padding: 2.5rem 3rem; }
  .hero-dashboard__grid {
    grid-template-columns: 0.9fr 1.2fr;
    gap: 2.5rem;
  }
  .hero-dashboard__uv-value { font-size: 3.5rem; }
  .hero-dashboard__location-heading { font-size: 2rem; }
}
</style>
