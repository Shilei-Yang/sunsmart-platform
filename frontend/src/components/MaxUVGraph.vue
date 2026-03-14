<!--
  Max UV Index graph — Prototype-style panel with soft UV gradient background.
  Today view: single visual bar or meter for today's max UV (no hourly data).
  7 Days view: bar per day. Scale 0–13. API provides daily max only.
-->
<script setup>
import { computed } from 'vue'

const props = defineProps({
  daily: { type: Array, default: () => [] },
  // Past 7 days history format: [{ date: 'YYYY-MM-DD', label: 'Mon', uv_index: 6.2 }, ...]
  history: { type: Array, default: () => [] },
  view: { type: String, default: 'today' },
  /** When true, use UVIBE dashboard styling: beige bars, muted grid, no inner title */
  dashboardStyle: { type: Boolean, default: false },
})

const MAX_UV_SCALE = 13

const bars = computed(() => {
  const list = props.daily.slice(0, props.view === 'today' ? 1 : 7)
  return list.map((d) => ({
    date: d.date,
    label: formatDayLabel(d.date),
    value: Math.min(MAX_UV_SCALE, Math.max(0, Number(d.uv_index_max) || 0)),
  }))
})

// Next 7 days forecast (for "7 Days" tab) from Open-Meteo daily forecast.
const forecast = computed(() => {
  const list = props.daily.slice(0, 7)
  return list.map((d) => {
    const iso = d.date
    const label = formatWeekday(iso)
    const uv = Math.min(MAX_UV_SCALE, Math.max(0, Number(d.uv_index_max) || 0))
    return { date: iso, label, uv_index: uv }
  })
})

// For "today" view: single value for the meter/bar
const todayValue = computed(() => {
  if (props.view !== 'today' || !bars.value.length) return 0
  return bars.value[0].value
})

const riskClass = computed(() => {
  const v = todayValue.value
  if (v <= 2) return 'low'
  if (v <= 5) return 'mod'
  if (v <= 7) return 'high'
  if (v <= 10) return 'veryhigh'
  return 'extreme'
})

function formatDayLabel(isoDate) {
  if (!isoDate) return ''
  const d = new Date(isoDate + 'T12:00:00')
  return d.toLocaleDateString('en-AU', { weekday: 'short', day: 'numeric', month: 'short' })
}

function formatWeekday(isoDate) {
  if (!isoDate) return ''
  const d = new Date(isoDate + 'T12:00:00')
  return d.toLocaleDateString('en-AU', { weekday: 'short' })
}

function barColorForUv(v) {
  if (v <= 2) return '#7bd77b'
  if (v <= 5) return '#f3df72'
  if (v <= 7) return '#f3a65a'
  if (v <= 10) return '#f16b6b'
  return '#a974e8'
}
</script>

<template>
  <div class="max-uv-graph" :class="{ 'max-uv-graph--dashboard': dashboardStyle && view === '7days' }">
    <!-- Soft UV gradient panel (prototype-style); transparent when in dashboard card -->
    <div class="max-uv-graph__panel">
      <!-- Today: single visual "meter" for max UV -->
      <template v-if="view === 'today' && bars.length">
        <div class="max-uv-graph__today">
          <!-- UV index scale labels: 0, 3, 6, 8, 11+ -->
          <div class="max-uv-graph__scale-labels">
            <span>0</span>
            <span>3</span>
            <span>6</span>
            <span>8</span>
            <span>11+</span>
          </div>
          <!-- Gradient UV scale bar: green → yellow → orange → red → purple -->
          <div class="max-uv-graph__meter-track">
            <div class="max-uv-graph__meter-gradient" />
            <div
              class="max-uv-graph__meter-marker"
              :style="{ left: `${(todayValue / MAX_UV_SCALE) * 100}%` }"
              :title="`Max UV: ${todayValue}`"
            >
              <span class="max-uv-graph__marker-value">{{ todayValue }}</span>
            </div>
          </div>
          <p class="max-uv-graph__today-label">Today’s max UV index</p>
        </div>
      </template>
      <!-- 7 Days: next 7 days UV forecast bar chart (weekly forecast / dashboard style) -->
      <template v-else-if="view === '7days'">
        <div class="forecast-chart" :class="{ 'forecast-chart--dashboard': dashboardStyle }">
          <div v-if="!dashboardStyle" class="forecast-chart__header">
            <h3 class="forecast-chart__title">Max UV Index – Next 7 Days</h3>
          </div>

          <div class="forecast-chart__plot">
            <!-- light grid lines -->
            <div class="forecast-chart__grid">
              <span v-for="n in 5" :key="n" class="forecast-chart__grid-line" />
            </div>

            <!-- Danger threshold (11+) - hidden in dashboard style for softer look -->
            <div
              v-if="!dashboardStyle"
              class="forecast-chart__threshold"
              :style="{ top: `${(1 - 11 / MAX_UV_SCALE) * 100}%` }"
            >
              <span class="forecast-chart__threshold-line" />
              <span class="forecast-chart__threshold-label">Danger Threshold (11+)</span>
            </div>

            <!-- Bars: dashboard uses single beige; otherwise risk-based colors -->
            <div class="forecast-chart__bars">
              <div
                v-for="item in forecast"
                :key="item.date"
                class="forecast-chart__bar-col"
              >
                <div class="forecast-chart__bar-wrap">
                  <div
                    class="forecast-chart__bar"
                    :class="{ 'forecast-chart__bar--dashboard': dashboardStyle }"
                    :style="{
                      height: `${(item.uv_index / MAX_UV_SCALE) * 100}%`,
                      background: dashboardStyle ? undefined : barColorForUv(item.uv_index),
                    }"
                    :title="`${item.label}: ${item.uv_index}`"
                  />
                </div>
                <div class="forecast-chart__x-label">{{ item.label }}</div>
                <div class="forecast-chart__value">{{ item.uv_index.toFixed(1) }}</div>
              </div>
            </div>
          </div>
        </div>
      </template>
      <!-- Past: 7-day history bar chart (light pastel theme) -->
      <template v-else>
        <div class="past-chart">
          <div class="past-chart__header">
            <h3 class="past-chart__title">Max UV Index – Past 7 Days</h3>
          </div>

          <div class="past-chart__plot">
            <!-- grid lines -->
            <div class="past-chart__grid">
              <span v-for="n in 5" :key="n" class="past-chart__grid-line" />
            </div>

            <!-- Danger threshold (11+) -->
            <div class="past-chart__threshold" :style="{ top: `${(1 - 11 / MAX_UV_SCALE) * 100}%` }">
              <span class="past-chart__threshold-line" />
              <span class="past-chart__threshold-label">Danger Threshold (11+)</span>
            </div>

            <div class="past-chart__bars">
              <div
                v-for="item in history.slice(-7)"
                :key="item.date"
                class="past-chart__bar-col"
              >
                <div class="past-chart__bar-wrap">
                  <div
                    class="past-chart__bar"
                    :style="{
                      height: `${(Math.min(MAX_UV_SCALE, Math.max(0, Number(item.uv_index) || 0)) / MAX_UV_SCALE) * 100}%`,
                      background: barColorForUv(Number(item.uv_index) || 0),
                    }"
                    :title="`${item.label}: ${item.uv_index}`"
                  />
                </div>
                <div class="past-chart__x-label">{{ item.label }}</div>
                <div class="past-chart__peak">Peak: {{ Number(item.uv_index || 0).toFixed(1) }}</div>
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>
    <p v-if="view !== '7days' || !dashboardStyle" class="max-uv-graph__legend">Max UV Index (daily)</p>
  </div>
</template>

<style scoped>
.max-uv-graph {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.max-uv-graph__panel {
  min-height: 200px;
  padding: 1.25rem 1.5rem;
  background: linear-gradient(
    180deg,
    #dbeafe 0%,
    #e0f2fe 20%,
    #fef9c3 45%,
    #fed7aa 70%,
    #fecaca 100%
  );
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.7);
}
.max-uv-graph--dashboard .max-uv-graph__panel {
  background: transparent;
  padding: 0;
  min-height: 0;
  border: none;
}
.max-uv-graph__today {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  height: 100%;
  min-height: 160px;
}
.max-uv-graph__scale-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  font-weight: 600;
  color: #475569;
}
.max-uv-graph__meter-track {
  position: relative;
  flex: 1;
  min-height: 40px;
  background: transparent;
  border-radius: 20px;
  overflow: visible;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}
.max-uv-graph__meter-gradient {
  position: absolute;
  inset: 0;
  border-radius: 20px;
  background: linear-gradient(
    to right,
    #6EDC6E,
    #F4E36C,
    #F7A64A,
    #F45B69,
    #A569E6
  );
  border: 1px solid rgba(255, 255, 255, 0.85);
}
.max-uv-graph__meter-marker {
  position: absolute;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: #fff;
  border: 3px solid #111827;
  box-shadow: 0 3px 10px rgba(15, 23, 42, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
}
.max-uv-graph__marker-value {
  font-size: 0.8125rem;
  font-weight: 800;
  color: #0f172a;
}
.max-uv-graph__today-label {
  margin: 0;
  font-size: 0.8125rem;
  font-weight: 600;
  color: #475569;
}
.max-uv-graph__chart {
  display: flex;
  align-items: flex-end;
  gap: 0.5rem;
  min-height: 160px;
}
.max-uv-graph__bar-wrap {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: flex-end;
  min-height: 160px;
}
.max-uv-graph__bar {
  width: 100%;
  max-width: 56px;
  min-height: 4px;
  border-radius: 8px 8px 0 0;
  transition: height 0.3s ease;
}
.max-uv-graph__bar--low { background: #22c55e; }
.max-uv-graph__bar--mod { background: #eab308; }
.max-uv-graph__bar--high { background: #f97316; }
.max-uv-graph__bar--veryhigh { background: #ef4444; }
.max-uv-graph__bar--extreme { background: #a855f7; }
.max-uv-graph__x-axis {
  display: flex;
  justify-content: space-around;
  gap: 0.25rem;
  padding-top: 0.5rem;
  font-size: 0.7rem;
  color: #475569;
  font-weight: 500;
}
.max-uv-graph__x-tick {
  flex: 1;
  text-align: center;
  max-width: 56px;
}
.max-uv-graph__legend {
  margin: 0;
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 500;
}

/* Forecast (Next 7 Days) chart styles (light pastel theme) */
.forecast-chart__header {
  margin-bottom: 0.75rem;
}
.forecast-chart__title {
  margin: 0;
  font-size: 1rem;
  font-weight: 700;
  color: #1f5f99;
}
.forecast-chart__plot {
  position: relative;
  background: #eef7ff;
  border: 1px solid #cfe3f5;
  border-radius: 18px;
  box-shadow: 0 6px 18px rgba(31, 95, 153, 0.08);
  padding: 1rem 1rem 0.75rem;
}
.forecast-chart__grid {
  position: absolute;
  inset: 1rem 1rem 2.2rem 1rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  pointer-events: none;
}
.forecast-chart__grid-line {
  height: 1px;
  background: #dbe8f4;
}
.forecast-chart__threshold {
  position: absolute;
  left: 1rem;
  right: 1rem;
  transform: translateY(-50%);
  pointer-events: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.forecast-chart__threshold-line {
  flex: 1;
  height: 0;
  border-top: 2px dashed #f28b82;
  opacity: 0.95;
}
.forecast-chart__threshold-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #1f5f99;
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid #cfe3f5;
  border-radius: 999px;
  padding: 0.2rem 0.5rem;
}
.forecast-chart__bars {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 0.75rem;
  align-items: end;
  min-height: 240px;
  padding-top: 0.5rem;
}
.forecast-chart__bar-col {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.35rem;
}
.forecast-chart__bar-wrap {
  height: 180px;
  width: 100%;
  display: flex;
  align-items: flex-end;
  justify-content: center;
}
.forecast-chart__bar {
  width: 100%;
  max-width: 42px;
  border-radius: 12px 12px 10px 10px;
  box-shadow: 0 8px 16px rgba(15, 23, 42, 0.08);
}
.forecast-chart__x-label {
  font-size: 0.75rem;
  font-weight: 700;
  color: #4f6f8f;
}
.forecast-chart__value {
  font-size: 0.7rem;
  color: #4f6f8f;
}

/* UVIBE dashboard style: beige bars, muted grid, soft weather chart */
.forecast-chart--dashboard .forecast-chart__plot {
  background: #fff;
  border: 1px solid #E6E1DA;
  box-shadow: none;
}
.forecast-chart--dashboard .forecast-chart__grid-line {
  background: #E6E1DA;
}
.forecast-chart__bar--dashboard {
  background: #E9D5B5 !important;
  border-radius: 10px 10px 0 0;
  box-shadow: none;
}
.forecast-chart--dashboard .forecast-chart__x-label,
.forecast-chart--dashboard .forecast-chart__value {
  color: #8A8A8A;
}

@media (max-width: 700px) {
  .forecast-chart__bars {
    gap: 0.5rem;
  }
  .forecast-chart__bar {
    max-width: 34px;
  }
}

/* Past 7 Days chart styles (light pastel theme) */
.past-chart__header {
  margin-bottom: 0.75rem;
}
.past-chart__title {
  margin: 0;
  font-size: 1rem;
  font-weight: 700;
  color: #1f5f99;
}
.past-chart__plot {
  position: relative;
  background: #eef7ff;
  border: 1px solid #cfe3f5;
  border-radius: 18px;
  box-shadow: 0 6px 18px rgba(31, 95, 153, 0.08);
  padding: 1rem 1rem 0.75rem;
}
.past-chart__grid {
  position: absolute;
  inset: 1rem 1rem 2.2rem 1rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  pointer-events: none;
}
.past-chart__grid-line {
  height: 1px;
  background: #dbe8f4;
}
.past-chart__threshold {
  position: absolute;
  left: 1rem;
  right: 1rem;
  transform: translateY(-50%);
  pointer-events: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.past-chart__threshold-line {
  flex: 1;
  height: 0;
  border-top: 2px dashed #f28b82;
  opacity: 0.95;
}
.past-chart__threshold-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #1f5f99;
  background: rgba(255, 255, 255, 0.7);
  border: 1px solid #cfe3f5;
  border-radius: 999px;
  padding: 0.2rem 0.5rem;
}
.past-chart__bars {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 0.75rem;
  align-items: end;
  min-height: 240px;
  padding-top: 0.5rem;
}
.past-chart__bar-col {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.35rem;
}
.past-chart__bar-wrap {
  height: 180px;
  width: 100%;
  display: flex;
  align-items: flex-end;
  justify-content: center;
}
.past-chart__bar {
  width: 100%;
  max-width: 42px;
  border-radius: 12px 12px 10px 10px;
  box-shadow: 0 8px 16px rgba(15, 23, 42, 0.08);
}
.past-chart__x-label {
  font-size: 0.75rem;
  font-weight: 700;
  color: #4f6f8f;
}
.past-chart__peak {
  font-size: 0.7rem;
  color: #4f6f8f;
}

@media (max-width: 700px) {
  .past-chart__bars {
    gap: 0.5rem;
  }
  .past-chart__bar {
    max-width: 34px;
  }
}
</style>
