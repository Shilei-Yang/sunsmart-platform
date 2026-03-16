<!--
  Homepage — UVIBE dashboard layout.
  Warm neutral background, top nav, hero with UV dashboard,
  below-hero: Why UV Protection + tab content (Impact, Personalised Experience, Sunscreen Management, etc.).
  Skin types live on the Personalised Experience page. Backend /api/uv unchanged.
-->
<script setup>
import { ref, provide } from 'vue'
import UVDashboard from '@/components/UVDashboard.vue'
import UVImpacts from '@/components/UVImpacts.vue'
import CancerVisualisation from '@/components/CancerVisualisation.vue'
import MythFactCarousel from '@/components/MythFactCarousel.vue'
import PersonalisedExperience from '@/components/PersonalisedExperience.vue'
import SunscreenManagement from '@/components/SunscreenManagement.vue'
import whyPhoto from '@/assets/pexels-jacub-gomez-447561-1168750.jpg'

const infoTab = ref('uv-impacts')
const uvData = ref(null)
provide('uvData', uvData)
provide('infoTab', infoTab)

const protectionTips = [
  { text: 'Seek shade' },
  { text: 'Protective clothing' },
  { text: 'Broad-spectrum sunscreen' },
  { text: 'Sunglasses' },
  { text: 'Wide-brim hat' },
]
</script>

<template>
  <div class="homepage">
    <header class="homepage__header" aria-label="Main navigation">
      <div class="homepage__header-inner">
        <div class="homepage__brand">
          <div class="homepage__brand-mark">
            <span class="homepage__brand-text">UVibe</span>
            <span class="homepage__brand-icon" aria-hidden="true">☀</span>
          </div>
          <p class="homepage__brand-tagline">
            Know the sun before it knows your skin
          </p>
        </div>
        <nav class="homepage__nav" aria-label="Information sections">
          <button type="button" class="homepage__nav-tab" :class="{ 'homepage__nav-tab--active': infoTab === 'uv-impacts' }" @click="infoTab = 'uv-impacts'">Impact</button>
          <button type="button" class="homepage__nav-tab" :class="{ 'homepage__nav-tab--active': infoTab === 'personalised' }" @click="infoTab = 'personalised'">Personalised Experience</button>
          <button type="button" class="homepage__nav-tab" :class="{ 'homepage__nav-tab--active': infoTab === 'sunscreen' }" @click="infoTab = 'sunscreen'">Sunscreen Management</button>
          <button type="button" class="homepage__nav-tab" :class="{ 'homepage__nav-tab--active': infoTab === 'clothing' }" @click="infoTab = 'clothing'">Sun-smart Clothing</button>
          <button type="button" class="homepage__nav-tab" :class="{ 'homepage__nav-tab--active': infoTab === 'resources' }" @click="infoTab = 'resources'">Resources</button>
        </nav>
      </div>
    </header>

    <main class="homepage__main">
      <div class="homepage__container">
        <section class="homepage__hero" aria-label="UV dashboard">
          <UVDashboard />
        </section>

        <div class="homepage__columns">
          <div class="homepage__col homepage__col--left">
            <template v-if="infoTab === 'uv-impacts'">
              <section class="why-hero">
                <img :src="whyPhoto" alt="Person walking on the beach at sunset" class="why-hero__bg" />
                <div class="why-hero__overlay" />
                <div class="why-hero__content">
                  <h2 class="why-hero__title">Why UV Protection Matters</h2>
                  <p class="why-hero__text">
                    Australia has some of the highest UV levels in the world. Prolonged exposure
                    to ultraviolet radiation can damage your skin and eyes and increase the risk
                    of skin cancer.
                  </p>
                  <div class="why-hero__tips">
                    <span v-for="tip in protectionTips" :key="tip.text" class="why-hero__tip">
                      <span class="why-hero__tip-dot" aria-hidden="true" />
                      {{ tip.text }}
                    </span>
                  </div>
                </div>
              </section>
              <UVImpacts />
              <CancerVisualisation />
              <MythFactCarousel />
            </template>
            <section v-else-if="infoTab === 'personalised'">
              <PersonalisedExperience />
            </section>
            <section v-else-if="infoTab === 'sunscreen'">
              <SunscreenManagement />
            </section>
            <section v-else class="homepage__coming-wrap">
              <p class="homepage__coming">Content for this section is coming soon.</p>
            </section>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.homepage {
  min-height: 100vh;
  --uv-bg: #F4F1EC;
  --uv-primary: #D8613C;
  --uv-hero-blue: #CFE4F0;
  --uv-hero-sun: #F4E1B6;
  --uv-danger: #D44A4A;
  --uv-value: #D54E4E;
  --uv-chart-bar: #E9D5B5;
  --uv-grid: #E6E1DA;
  --uv-text: #4A4A4A;
  --uv-text-muted: #8A8A8A;
  --uv-card: #FFFFFF;
  background: var(--uv-bg);
  color: var(--uv-text);
}

/* Top navigation */
.homepage__header {
  padding: 1rem 1.5rem;
  background: var(--uv-bg);
  border-bottom: 1px solid var(--uv-grid);
}
.homepage__header-inner {
  max-width: 1280px;
  margin: 0 auto;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1.5rem;
  flex-wrap: wrap;
}
.homepage__brand {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}
.homepage__brand-mark {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.homepage__brand-text {
  font-weight: 800;
  font-size: 2rem;
  letter-spacing: 0.04em;
  color: var(--uv-primary);
}
.homepage__brand-icon {
  font-size: 1.25rem;
  color: var(--uv-primary);
}
.homepage__brand-tagline {
  margin: 0;
  font-size: 0.78rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--uv-text-muted);
}
.homepage__nav {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
  align-items: center;
}
.homepage__nav-tab {
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--uv-text-muted);
  background: transparent;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: color 0.2s;
  position: relative;
}
.homepage__nav-tab:hover { color: var(--uv-text); }
.homepage__nav-tab--active {
  color: var(--uv-primary);
  font-weight: 600;
}
.homepage__nav-tab--active::after {
  content: '';
  position: absolute;
  left: 0.75rem;
  right: 0.75rem;
  bottom: 0.25rem;
  height: 2px;
  background: var(--uv-primary);
  border-radius: 1px;
}

.homepage__main { padding: 2rem 1.5rem 3rem; }
.homepage__container { max-width: 1280px; margin: 0 auto; }
.homepage__hero { margin-bottom: 1.25rem; }

.homepage__columns {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}
.homepage__col { min-width: 0; }

/* Why UV Protection — immersive photo hero card */
.why-hero {
  position: relative;
  overflow: hidden;
  border-radius: 20px;
  min-height: 320px;
  margin-bottom: 0;
  display: flex;
  align-items: flex-end;
}
.why-hero__bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 40%;
}
.why-hero__overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to top,
    rgba(30, 20, 12, 0.88) 0%,
    rgba(30, 20, 12, 0.65) 40%,
    rgba(30, 20, 12, 0.25) 70%,
    transparent 100%
  );
  pointer-events: none;
}
.why-hero__content {
  position: relative;
  z-index: 1;
  padding: 2rem 2rem 1.75rem;
  width: 100%;
}
.why-hero__title {
  margin: 0 0 0.75rem;
  font-size: 1.5rem;
  font-weight: 800;
  color: #fff;
  letter-spacing: -0.02em;
  line-height: 1.3;
  text-shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
}
.why-hero__text {
  margin: 0 0 1.25rem;
  font-size: 0.9375rem;
  line-height: 1.65;
  color: rgba(255, 255, 255, 0.85);
  max-width: 56ch;
  text-shadow: 0 1px 6px rgba(0, 0, 0, 0.2);
}
.why-hero__tips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.why-hero__tip {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.4rem 0.85rem;
  font-size: 0.8125rem;
  font-weight: 600;
  color: #fff;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 999px;
}
.why-hero__tip-dot {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.7);
  flex-shrink: 0;
}

.homepage__coming-wrap { padding-top: 0.5rem; }
.homepage__coming {
  margin: 0;
  padding: 2rem;
  text-align: center;
  color: var(--uv-text-muted);
  font-size: 0.9375rem;
  border-radius: 16px;
  background: #fff;
  border: 2px dashed var(--uv-grid);
}

@media (min-width: 900px) {
  .homepage__main { padding: 2.5rem 2rem 3.5rem; }
  .homepage__columns {
    flex-direction: row;
    align-items: flex-start;
    gap: 2.5rem;
  }
  .homepage__col--left { flex: 1; min-width: 0; }
}
</style>
