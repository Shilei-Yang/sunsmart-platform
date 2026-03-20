<!--
  CancerVisualisation — Storytelling narrative about melanoma in young Australians.
  Data: AIHW Cancer Data in Australia 2025, Book 1c (actual 1982–2021, projections 2022–2025).
-->
<script setup>
import { ref, computed, inject } from 'vue'
import { Line, Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js'

ChartJS.register(
  CategoryScale, LinearScale, PointElement, LineElement,
  BarElement, Title, Tooltip, Legend, Filler,
)

// ── Raw data ──
const trendPersons = [
  { year: 1982, count: 425, rate: 11.0 }, { year: 1983, count: 449, rate: 11.5 },
  { year: 1984, count: 431, rate: 11.0 }, { year: 1985, count: 483, rate: 12.2 },
  { year: 1986, count: 472, rate: 11.7 }, { year: 1987, count: 608, rate: 14.9 },
  { year: 1988, count: 648, rate: 15.7 }, { year: 1989, count: 517, rate: 12.4 },
  { year: 1990, count: 512, rate: 12.2 }, { year: 1991, count: 534, rate: 12.8 },
  { year: 1992, count: 515, rate: 12.5 }, { year: 1993, count: 494, rate: 12.1 },
  { year: 1994, count: 547, rate: 13.5 }, { year: 1995, count: 622, rate: 15.3 },
  { year: 1996, count: 609, rate: 15.0 }, { year: 1997, count: 636, rate: 15.7 },
  { year: 1998, count: 489, rate: 12.1 }, { year: 1999, count: 540, rate: 13.4 },
  { year: 2000, count: 517, rate: 12.8 }, { year: 2001, count: 494, rate: 12.3 },
  { year: 2002, count: 504, rate: 12.5 }, { year: 2003, count: 448, rate: 11.0 },
  { year: 2004, count: 488, rate: 11.9 }, { year: 2005, count: 486, rate: 11.7 },
  { year: 2006, count: 448, rate: 10.6 }, { year: 2007, count: 378, rate: 8.7 },
  { year: 2008, count: 390, rate: 8.7 }, { year: 2009, count: 405, rate: 8.8 },
  { year: 2010, count: 367, rate: 7.8 }, { year: 2011, count: 354, rate: 7.5 },
  { year: 2012, count: 379, rate: 7.9 }, { year: 2013, count: 372, rate: 7.7 },
  { year: 2014, count: 345, rate: 7.1 }, { year: 2015, count: 350, rate: 7.1 },
  { year: 2016, count: 372, rate: 7.5 }, { year: 2017, count: 329, rate: 6.5 },
  { year: 2018, count: 355, rate: 7.0 }, { year: 2019, count: 354, rate: 6.9 },
  { year: 2020, count: 315, rate: 6.2 }, { year: 2021, count: 275, rate: 5.6 },
]
const projPersons = [
  { year: 2021, count: 275, rate: 5.6 }, { year: 2022, count: 285, rate: 5.7 },
  { year: 2023, count: 290, rate: 5.5 }, { year: 2024, count: 288, rate: 5.3 },
  { year: 2025, count: 283, rate: 5.0 },
]
const trendMales = [
  { year: 1982, count: 166, rate: 8.4 }, { year: 1983, count: 156, rate: 7.9 },
  { year: 1984, count: 183, rate: 9.2 }, { year: 1985, count: 193, rate: 9.6 },
  { year: 1986, count: 204, rate: 9.9 }, { year: 1987, count: 263, rate: 12.7 },
  { year: 1988, count: 309, rate: 14.7 }, { year: 1989, count: 213, rate: 10.1 },
  { year: 1990, count: 226, rate: 10.7 }, { year: 1991, count: 244, rate: 11.6 },
  { year: 1992, count: 245, rate: 11.7 }, { year: 1993, count: 236, rate: 11.4 },
  { year: 1994, count: 258, rate: 12.5 }, { year: 1995, count: 281, rate: 13.7 },
  { year: 1996, count: 278, rate: 13.5 }, { year: 1997, count: 276, rate: 13.4 },
  { year: 1998, count: 210, rate: 10.3 }, { year: 1999, count: 238, rate: 11.7 },
  { year: 2000, count: 236, rate: 11.6 }, { year: 2001, count: 229, rate: 11.3 },
  { year: 2002, count: 223, rate: 10.9 }, { year: 2003, count: 199, rate: 9.7 },
  { year: 2004, count: 226, rate: 10.9 }, { year: 2005, count: 212, rate: 10.1 },
  { year: 2006, count: 201, rate: 9.4 }, { year: 2007, count: 159, rate: 7.2 },
  { year: 2008, count: 168, rate: 7.3 }, { year: 2009, count: 176, rate: 7.4 },
  { year: 2010, count: 151, rate: 6.3 }, { year: 2011, count: 160, rate: 6.6 },
  { year: 2012, count: 166, rate: 6.8 }, { year: 2013, count: 154, rate: 6.2 },
  { year: 2014, count: 147, rate: 5.9 }, { year: 2015, count: 134, rate: 5.4 },
  { year: 2016, count: 140, rate: 5.5 }, { year: 2017, count: 145, rate: 5.7 },
  { year: 2018, count: 156, rate: 6.0 }, { year: 2019, count: 157, rate: 6.0 },
  { year: 2020, count: 120, rate: 4.6 }, { year: 2021, count: 106, rate: 4.2 },
]
const projMales = [
  { year: 2021, count: 106, rate: 4.2 }, { year: 2022, count: 114, rate: 4.5 },
  { year: 2023, count: 114, rate: 4.2 }, { year: 2024, count: 112, rate: 4.0 },
  { year: 2025, count: 109, rate: 3.8 },
]
const trendFemales = [
  { year: 1982, count: 259, rate: 13.6 }, { year: 1983, count: 293, rate: 15.3 },
  { year: 1984, count: 248, rate: 12.8 }, { year: 1985, count: 290, rate: 14.8 },
  { year: 1986, count: 268, rate: 13.5 }, { year: 1987, count: 345, rate: 17.1 },
  { year: 1988, count: 339, rate: 16.6 }, { year: 1989, count: 304, rate: 14.8 },
  { year: 1990, count: 286, rate: 13.9 }, { year: 1991, count: 290, rate: 14.1 },
  { year: 1992, count: 270, rate: 13.2 }, { year: 1993, count: 258, rate: 12.8 },
  { year: 1994, count: 289, rate: 14.4 }, { year: 1995, count: 341, rate: 17.0 },
  { year: 1996, count: 331, rate: 16.5 }, { year: 1997, count: 360, rate: 17.9 },
  { year: 1998, count: 279, rate: 13.9 }, { year: 1999, count: 302, rate: 15.1 },
  { year: 2000, count: 281, rate: 14.1 }, { year: 2001, count: 265, rate: 13.3 },
  { year: 2002, count: 281, rate: 14.1 }, { year: 2003, count: 249, rate: 12.4 },
  { year: 2004, count: 262, rate: 13.0 }, { year: 2005, count: 274, rate: 13.4 },
  { year: 2006, count: 247, rate: 11.9 }, { year: 2007, count: 219, rate: 10.3 },
  { year: 2008, count: 222, rate: 10.1 }, { year: 2009, count: 229, rate: 10.2 },
  { year: 2010, count: 216, rate: 9.4 }, { year: 2011, count: 194, rate: 8.4 },
  { year: 2012, count: 213, rate: 9.1 }, { year: 2013, count: 218, rate: 9.2 },
  { year: 2014, count: 198, rate: 8.2 }, { year: 2015, count: 216, rate: 8.9 },
  { year: 2016, count: 232, rate: 9.4 }, { year: 2017, count: 184, rate: 7.4 },
  { year: 2018, count: 199, rate: 8.0 }, { year: 2019, count: 197, rate: 7.8 },
  { year: 2020, count: 195, rate: 7.8 }, { year: 2021, count: 167, rate: 6.9 },
]
const projFemales = [
  { year: 2021, count: 167, rate: 6.9 }, { year: 2022, count: 171, rate: 7.0 },
  { year: 2023, count: 176, rate: 6.9 }, { year: 2024, count: 176, rate: 6.6 },
  { year: 2025, count: 174, rate: 6.4 },
]
const ageComparison = [
  { age_group: '0–14', count: 10, rate: 0.2 },
  { age_group: '15–29', count: 283, rate: 5.0 },
  { age_group: '30–44', count: 1462, rate: 24.4 },
  { age_group: '45–59', count: 3451, rate: 70.5 },
  { age_group: '60–74', count: 6474, rate: 157.0 },
  { age_group: '75–89', count: 5231, rate: 257.3 },
  { age_group: '90+', count: 532, rate: 238.0 },
]

// ── Navigation ──
const infoTab = inject('infoTab', ref('uv-impacts'))
function navigateTo(tab) {
  infoTab.value = tab
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// ── Derived storytelling numbers ──
const peakEntry = trendPersons.reduce((a, b) => a.count > b.count ? a : b)
const projLatest = projPersons[projPersons.length - 1]
const declinePercent = Math.round(((peakEntry.count - projLatest.count) / peakEntry.count) * 100)
const perWeek = Math.round(projLatest.count / 52)
const femalePercent = Math.round((projFemales[projFemales.length - 1].count / projLatest.count) * 100)

// ── Chart: merged series ──
function mergeSeries(actual, proj) { return [...actual, ...proj.slice(1)] }
const allPersons = mergeSeries(trendPersons, projPersons)
const allMales = mergeSeries(trendMales, projMales)
const allFemales = mergeSeries(trendFemales, projFemales)
const allYears = allPersons.map(d => d.year)
const projStartIndex = trendPersons.length - 1

const projSegment = (color) => ({
  borderDash: (ctx) => ctx.p0DataIndex >= projStartIndex ? [6, 4] : undefined,
  borderColor: (ctx) => ctx.p0DataIndex >= projStartIndex ? color + 'AA' : undefined,
})

// Legend state
const trendChartRef = ref(null)
const seriesConfig = [
  { key: 'total', label: 'Total', color: '#D8613C' },
  { key: 'males', label: 'Males', color: '#5B8DEF' },
  { key: 'females', label: 'Females', color: '#E577A0' },
]
const hiddenSeries = ref(new Set())
function toggleSeries(index) {
  const chart = trendChartRef.value?.chart
  if (!chart) return
  const s = new Set(hiddenSeries.value)
  if (s.has(index)) { s.delete(index); chart.show(index) }
  else { s.add(index); chart.hide(index) }
  hiddenSeries.value = s
}

const trendChartData = computed(() => ({
  labels: allYears,
  datasets: [
    {
      label: 'Total', data: allPersons.map(d => d.count),
      borderColor: '#D8613C', backgroundColor: 'rgba(216, 97, 60, 0.08)',
      fill: true, tension: 0.35, pointRadius: 0, pointHoverRadius: 5,
      pointHoverBackgroundColor: '#D8613C', borderWidth: 2.5,
      segment: projSegment('#D8613C'),
    },
    {
      label: 'Males', data: allMales.map(d => d.count),
      borderColor: '#5B8DEF', backgroundColor: 'transparent',
      tension: 0.35, pointRadius: 0, pointHoverRadius: 4,
      pointHoverBackgroundColor: '#5B8DEF', borderWidth: 1.8,
      segment: projSegment('#5B8DEF'),
    },
    {
      label: 'Females', data: allFemales.map(d => d.count),
      borderColor: '#E577A0', backgroundColor: 'transparent',
      tension: 0.35, pointRadius: 0, pointHoverRadius: 4,
      pointHoverBackgroundColor: '#E577A0', borderWidth: 1.8,
      segment: projSegment('#E577A0'),
    },
  ],
}))

const trendChartOptions = {
  responsive: true, maintainAspectRatio: false,
  interaction: { mode: 'index', intersect: false },
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: 'rgba(30,30,30,0.92)', titleFont: { size: 13, weight: '600' },
      bodyFont: { size: 12 }, padding: 12, cornerRadius: 8,
      callbacks: {
        title(items) { const yr = Number(items[0]?.label); return yr >= 2022 ? `${yr} (projected)` : `${yr}` },
        label(ctx) { return `${ctx.dataset.label}: ${ctx.parsed.y} cases` },
      },
    },
  },
  scales: {
    x: { grid: { display: false }, ticks: { font: { size: 11 }, color: '#9ca3af',
      callback(val, index) { const y = allYears[index]; return (y === 1982 || y === 2025 || y % 5 === 0) ? y : null },
    }},
    y: { beginAtZero: true, grid: { color: 'rgba(0,0,0,0.04)' },
      ticks: { font: { size: 11 }, color: '#9ca3af' },
      title: { display: true, text: 'Cases', font: { size: 12, weight: '500' }, color: '#9ca3af' },
    },
  },
}

const ageBarData = computed(() => ({
  labels: ageComparison.map(d => d.age_group),
  datasets: [{
    label: 'Cases (2025 est.)', data: ageComparison.map(d => d.count),
    backgroundColor: ageComparison.map(d => d.age_group === '15–29' ? '#D8613C' : '#E9D5B5'),
    borderRadius: 6, borderSkipped: false, maxBarThickness: 48,
  }],
}))
const ageBarOptions = {
  responsive: true, maintainAspectRatio: false,
  plugins: { legend: { display: false },
    tooltip: { backgroundColor: 'rgba(30,30,30,0.92)', titleFont: { size: 13, weight: '600' },
      bodyFont: { size: 12 }, padding: 12, cornerRadius: 8 },
  },
  scales: {
    x: { grid: { display: false }, ticks: { font: { size: 11 }, color: '#9ca3af' } },
    y: { beginAtZero: true, grid: { color: 'rgba(0,0,0,0.04)' }, ticks: { font: { size: 11 }, color: '#9ca3af' } },
  },
}
</script>

<template>
  <section class="story">
    <!-- ━━ Chapter 1: The Hook ━━ -->
    <div class="story__hook">
      <p class="story__eyebrow">The reality for young Australians</p>
      <h2 class="story__headline">
        Every week, <span class="story__accent">{{ perWeek }}</span> young Australians
        aged 15–29 are diagnosed with melanoma.
      </h2>
    </div>

    <!-- ━━ Chapter 2: The Good News ━━ -->
    <div class="story__chapter">
      <div class="story__narrative">
        <span class="story__chapter-tag story__chapter-tag--green">The good news</span>
        <h3 class="story__chapter-title">Awareness works. It already saved thousands.</h3>
        <p class="story__chapter-text">
          Cases down
          <strong class="story__highlight story__highlight--green">{{ declinePercent }}%</strong>
          since {{ peakEntry.year }}. Slip, Slop, Slap made the difference.
        </p>
      </div>

      <div class="story__chart-card uv-card">
        <div class="story__chart-header">
          <span class="story__chart-label">Melanoma cases, ages 15–29 (1982–2025)</span>
          <div class="story__legend">
            <button
              v-for="(s, i) in seriesConfig" :key="s.key" type="button"
              class="story__legend-item"
              :class="{ 'story__legend-item--hidden': hiddenSeries.has(i) }"
              @click="toggleSeries(i)"
            >
              <span class="story__legend-dot" :style="{
                backgroundColor: hiddenSeries.has(i) ? 'transparent' : s.color,
                borderColor: s.color,
              }" />
              <span class="story__legend-label">{{ s.label }}</span>
            </button>
          </div>
        </div>
        <div class="story__chart-wrap">
          <Line ref="trendChartRef" :data="trendChartData" :options="trendChartOptions" />
        </div>
      </div>
    </div>

    <!-- ━━ Chapter 3: The Wake-Up Call ━━ -->
    <div class="story__chapter">
      <span class="story__chapter-tag story__chapter-tag--amber">But here's the catch</span>
      <h3 class="story__chapter-title">
        A tan isn't a sign of health - it's your skin crying for help.
      </h3>

      <div class="story__callout-grid">
        <div class="story__callout uv-card">
          <span class="story__callout-number story__callout-number--red">{{ projLatest.count }}</span>
          <span class="story__callout-desc">
            young Australians estimated to be diagnosed with melanoma in {{ projLatest.year }}
          </span>
        </div>
        <div class="story__callout uv-card">
          <span class="story__callout-number story__callout-number--pink">{{ femalePercent }}%</span>
          <span class="story__callout-desc">
            of cases are young women - the demographic most influenced by tanning trends
          </span>
        </div>
      </div>
    </div>

    <!-- ━━ Chapter 4: Age Context ━━ -->
    <div class="story__chapter">
      <span class="story__chapter-tag">It starts young</span>
      <h3 class="story__chapter-title">
        UV damage in your 20s shows up as cancer in your 40s, 50s and beyond.
      </h3>

      <div class="story__chart-card uv-card">
        <span class="story__chart-label">Melanoma cases by age group (2025 est.)</span>
        <div class="story__chart-wrap story__chart-wrap--bar">
          <Bar :data="ageBarData" :options="ageBarOptions" />
        </div>
      </div>
    </div>

    <!-- ━━ Chapter 5: Call to Action ━━ -->
    <div class="story__cta">
      <h3 class="story__cta-title">This is why UVibe exists.</h3>
      <p class="story__cta-text">
        Enjoy the sun. Just do it smarter.
      </p>
      <div class="story__cta-actions">
        <button type="button" class="story__cta-pill" @click="navigateTo('uv-impacts')">Check today's UV</button>
        <button type="button" class="story__cta-pill" @click="navigateTo('personalised')">See your skin type</button>
        <button type="button" class="story__cta-pill" @click="navigateTo('sunscreen')">Sunscreen guide</button>
      </div>
    </div>

    <p class="story__source">
      Data: AIHW Cancer Data in Australia 2025, Book 1c. Actual data 1982–2021; projections 2022–2025.
    </p>
  </section>
</template>

<style scoped>
.story {
  margin-top: 2rem;
  margin-bottom: 2rem;
}

/* ── Hook ── */
.story__hook {
  margin-bottom: 2.5rem;
}
.story__eyebrow {
  margin: 0 0 0.75rem;
  font-size: 0.6875rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: var(--uv-primary, #D8613C);
}
.story__headline {
  margin: 0 0 1rem;
  font-size: 1.625rem;
  font-weight: 800;
  line-height: 1.3;
  letter-spacing: -0.02em;
  color: var(--uv-text, #4A4A4A);
}
.story__accent {
  color: var(--uv-primary, #D8613C);
  font-size: 2rem;
}
.story__subtext {
  margin: 0;
  font-size: 1rem;
  line-height: 1.65;
  color: var(--uv-text-muted, #8A8A8A);
}
.story__subtext strong {
  color: var(--uv-text, #4A4A4A);
}

/* ── Chapters ── */
.story__chapter {
  margin-bottom: 2.5rem;
}
.story__chapter-tag {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  font-size: 0.6875rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  border-radius: 999px;
  margin-bottom: 0.75rem;
  background: rgba(216, 97, 60, 0.1);
  color: var(--uv-primary, #D8613C);
}
.story__chapter-tag--green {
  background: rgba(22, 163, 74, 0.1);
  color: #16a34a;
}
.story__chapter-tag--amber {
  background: rgba(217, 119, 6, 0.1);
  color: #b45309;
}
.story__chapter-title {
  margin: 0 0 0.75rem;
  font-size: 1.25rem;
  font-weight: 700;
  line-height: 1.35;
  color: var(--uv-text, #4A4A4A);
}
.story__chapter-text {
  margin: 0 0 0.75rem;
  font-size: 0.9375rem;
  line-height: 1.7;
  color: var(--uv-text-muted, #8A8A8A);
  max-width: 64ch;
}
.story__chapter-text:last-of-type {
  margin-bottom: 1.25rem;
}
.story__chapter-text strong {
  color: var(--uv-text, #4A4A4A);
}
.story__highlight--red { color: #D44A4A; }
.story__highlight--green { color: #16a34a; }

/* ── Callout cards ── */
.story__callout-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
}
.story__callout {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  padding: 1.5rem 1.25rem;
}
.story__callout-number {
  font-size: 2.25rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  line-height: 1;
}
.story__callout-number--red { color: #D44A4A; }
.story__callout-number--pink { color: #E577A0; }
.story__callout-desc {
  font-size: 0.875rem;
  line-height: 1.5;
  color: var(--uv-text-muted, #8A8A8A);
}

/* ── Chart cards ── */
.story__chart-card {
  margin-top: 0.25rem;
}
.story__chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}
.story__chart-label {
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--uv-text-muted, #8A8A8A);
}
.story__chart-wrap {
  position: relative;
  height: 300px;
}
.story__chart-wrap--bar {
  height: 260px;
}

/* ── Custom legend (same as before) ── */
.story__legend {
  display: flex;
  gap: 0.35rem;
  flex-shrink: 0;
}
.story__legend-item {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.3rem 0.7rem;
  border: 1px solid var(--uv-grid, #E6E1DA);
  border-radius: 999px;
  background: #fff;
  cursor: pointer;
  transition: all 0.25s ease;
}
.story__legend-item:hover {
  border-color: #ccc;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
}
.story__legend-item--hidden {
  background: var(--uv-bg, #F4F1EC);
  border-color: transparent;
}
.story__legend-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  border: 2px solid;
  flex-shrink: 0;
  transition: background-color 0.25s ease;
}
.story__legend-label {
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.02em;
  color: var(--uv-text, #4A4A4A);
  transition: color 0.25s ease;
}
.story__legend-item--hidden .story__legend-label {
  color: var(--uv-text-muted, #8A8A8A);
}

/* ── Call to Action ── */
.story__cta {
  background: var(--uv-card, #FFFFFF);
  border-radius: 16px;
  border: 1px solid var(--uv-grid, #E6E1DA);
  padding: 2rem 1.75rem;
  text-align: center;
  margin-bottom: 1rem;
}
.story__cta-title {
  margin: 0 0 0.5rem;
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--uv-primary, #D8613C);
}
.story__cta-text {
  margin: 0 auto 1.25rem;
  font-size: 0.9375rem;
  line-height: 1.65;
  color: var(--uv-text-muted, #8A8A8A);
  max-width: 52ch;
}
.story__cta-actions {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.story__cta-pill {
  display: inline-flex;
  padding: 0.5rem 1rem;
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--uv-primary, #D8613C);
  background: rgba(216, 97, 60, 0.08);
  border: 1px solid rgba(216, 97, 60, 0.15);
  border-radius: 999px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.story__cta-pill:hover {
  background: rgba(216, 97, 60, 0.15);
  border-color: rgba(216, 97, 60, 0.3);
}

.story__source {
  margin: 0;
  font-size: 0.75rem;
  color: var(--uv-text-muted, #8A8A8A);
  font-style: italic;
}

/* ── Mobile ── */
@media (max-width: 600px) {
  .story__headline { font-size: 1.375rem; }
  .story__accent { font-size: 1.625rem; }
  .story__callout-grid { grid-template-columns: 1fr; }
  .story__chart-wrap { height: 240px; }
  .story__chart-wrap--bar { height: 220px; }
  .story__legend { flex-wrap: wrap; }
}
</style>
