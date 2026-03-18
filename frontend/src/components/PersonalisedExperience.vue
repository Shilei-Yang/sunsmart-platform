<script setup>
import { ref, computed, inject } from 'vue'

const uvData = inject('uvData', ref(null))
const selectedId = ref(null)

const fitzpatrick = [
  {
    id: 1,
    label: 'Type I',
    name: 'Very Fair',
    hex: '#FDDCB5',
    description: 'Light blue or green eyes, red or blond hair, freckles common',
    reaction: 'Always burns, never tans',
    baseBurn: 10,
    riskLevel: 'Very High',
    riskColor: '#D44A4A',
    spf: '50+',
    tips: [
      'Reapply SPF 50+ every 60–80 minutes when outdoors',
      'Wear UPF-rated clothing and a wide-brim hat',
      'Avoid direct sun between 10 am and 4 pm',
    ],
    melanomaNotes: 'Highest melanoma risk. 1 in 50 Australians with very fair skin will be diagnosed.',
  },
  {
    id: 2,
    label: 'Type II',
    name: 'Fair',
    hex: '#F5C8A0',
    description: 'Blue or hazel eyes, blond or light brown hair',
    reaction: 'Burns easily, tans minimally',
    baseBurn: 15,
    riskLevel: 'High',
    riskColor: '#E07B3A',
    spf: '50+',
    tips: [
      'Use SPF 50+ and reapply after swimming or sweating',
      'Sunglasses with UV400 protection are essential',
      'Seek shade during peak UV hours',
    ],
    melanomaNotes: 'High melanoma risk. Fair skin and freckling increase vulnerability significantly.',
  },
  {
    id: 3,
    label: 'Type III',
    name: 'Medium',
    hex: '#D4A57B',
    description: 'Hazel or brown eyes, brown hair',
    reaction: 'Sometimes burns, tans gradually',
    baseBurn: 20,
    riskLevel: 'Moderate',
    riskColor: '#D4A017',
    spf: '30+',
    tips: [
      'Apply SPF 30+ generously, even on cloudy days',
      'Monitor moles and freckles for changes regularly',
      'UV damage accumulates even when you tan',
    ],
    melanomaNotes: 'Moderate risk, but UV damage is cumulative. A tan does not equal protection.',
  },
  {
    id: 4,
    label: 'Type IV',
    name: 'Olive',
    hex: '#A67C52',
    description: 'Brown eyes, dark brown hair',
    reaction: 'Rarely burns, tans easily',
    baseBurn: 30,
    riskLevel: 'Moderate',
    riskColor: '#B8960C',
    spf: '30',
    tips: [
      'SPF 30 is your minimum, even if you rarely burn',
      'Check for skin changes in less-exposed areas too',
      'Tanning does not mean you are protected from DNA damage',
    ],
    melanomaNotes: 'Lower incidence, but melanoma can still occur. Stay vigilant with self-checks.',
  },
  {
    id: 5,
    label: 'Type V',
    name: 'Brown',
    hex: '#7B5438',
    description: 'Dark brown eyes and hair',
    reaction: 'Very rarely burns, tans profusely',
    baseBurn: 40,
    riskLevel: 'Lower',
    riskColor: '#3A9E5C',
    spf: '15–30',
    tips: [
      'Sunscreen is still important: use SPF 15–30 daily',
      'Melanoma in darker skin is often found late, on palms, soles, or nails',
      'Regular skin checks matter for every skin tone',
    ],
    melanomaNotes: 'Melanoma is rarer but often diagnosed at a later, more dangerous stage.',
  },
  {
    id: 6,
    label: 'Type VI',
    name: 'Very Dark',
    hex: '#4A3228',
    description: 'Dark brown or black eyes and hair',
    reaction: 'Never burns',
    baseBurn: 60,
    riskLevel: 'Lower',
    riskColor: '#3A9E5C',
    spf: '15–30',
    tips: [
      'SPF 15–30 protects against photoaging and long-term UV damage',
      'Watch for unusual patches on palms, soles, and under nails',
      'Late diagnosis is the biggest risk — stay aware, stay checked',
    ],
    melanomaNotes: 'Lowest incidence, but acral melanoma (palms, soles, nails) is a real concern.',
  },
]

const selected = computed(() => fitzpatrick.find(t => t.id === selectedId.value) ?? null)

const currentUV = computed(() => {
  const raw = uvData.value?.current_uv ?? uvData.value?.uv_index
  const val = Number(raw)
  return Number.isFinite(val) && val >= 0 ? val : null
})

const uvLabel = computed(() => {
  if (currentUV.value === null) return null
  return `UV ${currentUV.value.toFixed(1)}`
})

function burnTime(type) {
  if (currentUV.value === null) return null
  if (currentUV.value === 0) return Number.POSITIVE_INFINITY
  return Math.round(type.baseBurn * 6 / currentUV.value)
}

function burnTimeDisplay(type) {
  const mins = burnTime(type)
  if (mins === null) return 'UV data unavailable'
  if (!Number.isFinite(mins)) return '~No immediate burn risk'
  if (mins >= 120) return `~${Math.round(mins / 60)} hrs`
  return `~${mins} min`
}

function selectType(id) {
  selectedId.value = selectedId.value === id ? null : id
}
</script>

<template>
  <section class="skin">
    <!-- Intro -->
    <div class="skin__intro uv-card">
      <span class="skin__eyebrow">Skin Tone Awareness</span>
      <h2 class="skin__headline">
        How does <span class="skin__accent">your skin</span> respond to UV?
      </h2>
      <p class="skin__subtext">
        Select your skin tone to see your personalised UV risk profile.
      </p>

      <!-- Swatch picker -->
      <div class="skin__picker">
        <button
          v-for="type in fitzpatrick"
          :key="type.id"
          type="button"
          class="skin__swatch"
          :class="{ 'skin__swatch--active': selectedId === type.id }"
          :style="{ '--swatch': type.hex }"
          :aria-label="`Select ${type.label}: ${type.name}`"
          :aria-pressed="selectedId === type.id"
          @click="selectType(type.id)"
        >
          <span class="skin__swatch-circle" />
          <span class="skin__swatch-label">{{ type.label }}</span>
        </button>
      </div>
    </div>

    <!-- Personalised risk card (visible when a type is selected) -->
    <transition name="skin-fade">
      <div v-if="selected" class="skin__risk uv-card" :style="{ '--risk': selected.riskColor }">
        <div class="skin__risk-header">
          <div class="skin__risk-swatch" :style="{ background: selected.hex }" />
          <div>
            <h3 class="skin__risk-title">{{ selected.label }}: {{ selected.name }}</h3>
            <p class="skin__risk-desc">{{ selected.description }}</p>
          </div>
          <span class="skin__risk-badge" :style="{ background: selected.riskColor }">
            {{ selected.riskLevel }} Risk
          </span>
        </div>

        <p class="skin__risk-reaction">
          <strong>Sun reaction:</strong> {{ selected.reaction }}
        </p>

        <div class="skin__risk-stats">
          <div class="skin__stat">
            <span class="skin__stat-value">{{ burnTimeDisplay(selected) }}</span>
            <span class="skin__stat-label">
              Estimated burn time
              <template v-if="uvLabel">(at {{ uvLabel }})</template>
            </span>
          </div>
          <div class="skin__stat">
            <span class="skin__stat-value">SPF {{ selected.spf }}</span>
            <span class="skin__stat-label">Recommended sunscreen</span>
          </div>
        </div>

        <div class="skin__tips">
          <h4 class="skin__tips-title">Your protection checklist</h4>
          <ul class="skin__tips-list">
            <li v-for="(tip, i) in selected.tips" :key="i" class="skin__tips-item">
              {{ tip }}
            </li>
          </ul>
        </div>

        <div class="skin__melanoma-note">
          <span class="skin__melanoma-icon" aria-hidden="true">⚠</span>
          <p>{{ selected.melanomaNotes }}</p>
        </div>
      </div>
    </transition>

    <!-- Educational comparison grid -->
    <div class="skin__compare uv-card">
      <span class="skin__eyebrow">How All Skin Types Compare</span>
      <h3 class="skin__compare-title">UV affects everyone differently</h3>
      <p class="skin__compare-disclaimer">
        Disclaimer: This section is for informational purposes only and does not replace professional medical advice.
      </p>
      <p class="skin__subtext">
        Burn time and risk across all six skin types.<template v-if="selected"> Yours is highlighted.</template>
      </p>

      <div class="skin__grid">
        <div
          v-for="type in fitzpatrick"
          :key="type.id"
          class="skin__card"
          :class="{ 'skin__card--selected': selectedId === type.id }"
        >
          <div class="skin__card-swatch" :style="{ background: type.hex }" />
          <span class="skin__card-label">{{ type.label }}</span>
          <span class="skin__card-name">{{ type.name }}</span>
          <span class="skin__card-burn">{{ burnTimeDisplay(type) }}</span>
          <span
            class="skin__card-risk"
            :style="{ color: type.riskColor, borderColor: type.riskColor }"
          >
            {{ type.riskLevel }}
          </span>
          <span class="skin__card-reaction">{{ type.reaction }}</span>
        </div>
      </div>
    </div>

    <!-- Awareness callout -->
    <div class="skin__callout">
      <p class="skin__callout-text">
        <strong>All skin types can develop skin cancer.</strong>
        Darker tones are often diagnosed later — early awareness matters for everyone.
      </p>
    </div>
  </section>
</template>

<style scoped>
.skin {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

/* Intro card */
.skin__intro {
  text-align: center;
  padding: 2rem 1.5rem 1.75rem;
}
.skin__eyebrow {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--uv-primary, #D8613C);
  margin-bottom: 0.5rem;
}
.skin__headline {
  margin: 0 0 0.6rem;
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--uv-text, #4A4A4A);
  letter-spacing: -0.02em;
  line-height: 1.3;
}
.skin__accent {
  color: var(--uv-primary, #D8613C);
}
.skin__subtext {
  margin: 0 0 1.25rem;
  font-size: 0.9375rem;
  line-height: 1.6;
  color: var(--uv-text-muted, #8A8A8A);
  max-width: 52ch;
  margin-left: auto;
  margin-right: auto;
}

/* Swatch picker */
.skin__picker {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}
.skin__swatch {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.4rem;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  transition: transform 0.2s ease;
}
.skin__swatch:hover {
  transform: translateY(-3px);
}
.skin__swatch-circle {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: var(--swatch);
  border: 3px solid transparent;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: border-color 0.25s ease, box-shadow 0.25s ease, transform 0.25s ease;
}
.skin__swatch:hover .skin__swatch-circle {
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.18);
}
.skin__swatch--active .skin__swatch-circle {
  border-color: var(--uv-primary, #D8613C);
  box-shadow: 0 0 0 3px rgba(216, 97, 60, 0.25), 0 4px 14px rgba(0, 0, 0, 0.15);
  transform: scale(1.1);
}
.skin__swatch-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--uv-text-muted, #8A8A8A);
  transition: color 0.2s;
}
.skin__swatch--active .skin__swatch-label {
  color: var(--uv-primary, #D8613C);
}

/* Risk card */
.skin__risk {
  padding: 1.75rem;
  border-left: 4px solid var(--risk);
  animation: skin-slideIn 0.35s ease;
}
.skin__risk-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}
.skin__risk-swatch {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
}
.skin__risk-title {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--uv-text, #4A4A4A);
}
.skin__risk-desc {
  margin: 0.15rem 0 0;
  font-size: 0.8125rem;
  color: var(--uv-text-muted, #8A8A8A);
}
.skin__risk-badge {
  margin-left: auto;
  padding: 0.3rem 0.85rem;
  font-size: 0.75rem;
  font-weight: 700;
  color: #fff;
  border-radius: 999px;
  letter-spacing: 0.03em;
  white-space: nowrap;
}
.skin__risk-reaction {
  margin: 0 0 1.25rem;
  font-size: 0.9375rem;
  color: var(--uv-text, #4A4A4A);
  line-height: 1.5;
}

/* Stats row */
.skin__risk-stats {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}
.skin__stat {
  flex: 1;
  min-width: 140px;
  padding: 1rem;
  background: var(--uv-bg, #F4F1EC);
  border-radius: 12px;
  text-align: center;
}
.skin__stat-value {
  display: block;
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--uv-primary, #D8613C);
  margin-bottom: 0.2rem;
}
.skin__stat-label {
  font-size: 0.8125rem;
  color: var(--uv-text-muted, #8A8A8A);
  line-height: 1.4;
}

/* Tips */
.skin__tips {
  margin-bottom: 1.25rem;
}
.skin__tips-title {
  margin: 0 0 0.6rem;
  font-size: 0.9375rem;
  font-weight: 700;
  color: var(--uv-text, #4A4A4A);
}
.skin__tips-list {
  margin: 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.skin__tips-item {
  position: relative;
  padding-left: 1.25rem;
  font-size: 0.875rem;
  color: var(--uv-text, #4A4A4A);
  line-height: 1.55;
}
.skin__tips-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0.5em;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--risk);
}

/* Melanoma note */
.skin__melanoma-note {
  display: flex;
  align-items: flex-start;
  gap: 0.6rem;
  padding: 0.85rem 1rem;
  background: rgba(212, 74, 74, 0.06);
  border: 1px solid rgba(212, 74, 74, 0.15);
  border-radius: 10px;
}
.skin__melanoma-icon {
  font-size: 1.1rem;
  flex-shrink: 0;
  line-height: 1.5;
}
.skin__melanoma-note p {
  margin: 0;
  font-size: 0.8125rem;
  color: var(--uv-text, #4A4A4A);
  line-height: 1.55;
}

/* Comparison grid */
.skin__compare {
  padding: 1.75rem 1.5rem;
}
.skin__compare-title {
  margin: 0 0 0.4rem;
  font-size: 1.1875rem;
  font-weight: 700;
  color: var(--uv-text, #4A4A4A);
}
.skin__compare-disclaimer {
  margin: 0 0 0.8rem;
  padding: 0.55rem 0.75rem;
  font-size: 0.8125rem;
  line-height: 1.45;
  color: #8a4a36;
  background: rgba(216, 97, 60, 0.1);
  border: 1px solid rgba(216, 97, 60, 0.2);
  border-radius: 10px;
}
.skin__grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 0.75rem;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  padding-bottom: 0.25rem;
  scrollbar-width: thin;
}
.skin__card {
  min-width: 130px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 0.35rem;
  padding: 1.25rem 0.75rem;
  background: var(--uv-bg, #F4F1EC);
  border-radius: 14px;
  border: 2px solid transparent;
  transition: border-color 0.25s, box-shadow 0.25s, transform 0.25s;
  scroll-snap-align: start;
}
.skin__card--selected {
  border-color: var(--uv-primary, #D8613C);
  box-shadow: 0 4px 18px rgba(216, 97, 60, 0.15);
  transform: translateY(-4px);
}
.skin__card-swatch {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 0.25rem;
}
.skin__card-label {
  font-size: 0.8125rem;
  font-weight: 700;
  color: var(--uv-text, #4A4A4A);
}
.skin__card-name {
  font-size: 0.75rem;
  color: var(--uv-text-muted, #8A8A8A);
}
.skin__card-burn {
  font-size: 0.9375rem;
  font-weight: 800;
  color: var(--uv-primary, #D8613C);
  margin: 0.25rem 0;
}
.skin__card-risk {
  font-size: 0.6875rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  border: 1.5px solid;
  border-radius: 999px;
  padding: 0.15rem 0.6rem;
}
.skin__card-reaction {
  font-size: 0.6875rem;
  color: var(--uv-text-muted, #8A8A8A);
  line-height: 1.4;
  margin-top: 0.2rem;
}

/* Awareness callout */
.skin__callout {
  padding: 1.25rem 1.5rem;
  background: linear-gradient(135deg, #D8613C 0%, #c44e2c 100%);
  border-radius: 14px;
  text-align: center;
}
.skin__callout-text {
  margin: 0;
  font-size: 0.9375rem;
  color: #fff;
  line-height: 1.6;
}
.skin__callout-text strong {
  display: block;
  font-size: 1rem;
  margin-bottom: 0.25rem;
}

/* Transition */
.skin-fade-enter-active,
.skin-fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.skin-fade-enter-from,
.skin-fade-leave-to {
  opacity: 0;
  transform: translateY(12px);
}

@keyframes skin-slideIn {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* Tablet & mobile: keep horizontal row with swipe */
@media (max-width: 1024px) {
  .skin__grid {
    grid-template-columns: none;
    grid-auto-flow: column;
    grid-auto-columns: minmax(150px, 160px);
    overflow-x: auto;
    overflow-y: hidden;
    scroll-snap-type: x proximity;
    -webkit-overflow-scrolling: touch;
    padding: 0.2rem 0.15rem 0.35rem;
    gap: 0.65rem;
  }
  .skin__risk-badge {
    margin-left: 0;
  }
}
@media (max-width: 540px) {
  .skin__picker {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    justify-items: center;
    gap: 0.65rem 0.45rem;
    max-width: 320px;
    margin: 0 auto;
  }
  .skin__swatch {
    width: 100%;
    max-width: 92px;
    padding: 0.2rem 0;
  }
  .skin__swatch-circle {
    width: 44px;
    height: 44px;
  }
  .skin__intro {
    padding: 1.5rem 1rem;
  }
  .skin__risk {
    padding: 1.25rem;
  }
  .skin__compare {
    padding: 1.25rem 1rem;
  }
}
</style>
