<!--
  Homepage — UVIBE dashboard layout.
  Warm neutral background, top nav (Impact active), hero with two-column UV dashboard,
  below-hero: Why UV Protection, UV Impacts, Skin Types. Backend /api/uv unchanged.
-->
<script setup>
import { ref } from 'vue'
import UVDashboard from '@/components/UVDashboard.vue'
import UVImpacts from '@/components/UVImpacts.vue'
import SkinTypes from '@/components/SkinTypes.vue'

const infoTab = ref('uv-impacts')
</script>

<template>
  <div class="homepage">
    <!-- Top navigation: brand left, nav items right, Impact active with orange underline -->
    <header class="homepage__header" aria-label="Main navigation">
      <div class="homepage__header-inner">
        <div class="homepage__brand">
          <span class="homepage__brand-text">UVIBE</span>
          <span class="homepage__brand-icon" aria-hidden="true">☀</span>
        </div>
        <nav class="homepage__nav" aria-label="Information sections">
          <button
            type="button"
            class="homepage__nav-tab"
            :class="{ 'homepage__nav-tab--active': infoTab === 'uv-impacts' }"
            @click="infoTab = 'uv-impacts'"
          >
            Impact
          </button>
          <button
            type="button"
            class="homepage__nav-tab"
            :class="{ 'homepage__nav-tab--active': infoTab === 'personalised' }"
            @click="infoTab = 'personalised'"
          >
            Personalised Experience
          </button>
          <button
            type="button"
            class="homepage__nav-tab"
            :class="{ 'homepage__nav-tab--active': infoTab === 'sunscreen' }"
            @click="infoTab = 'sunscreen'"
          >
            Sunscreen Management
          </button>
          <button
            type="button"
            class="homepage__nav-tab"
            :class="{ 'homepage__nav-tab--active': infoTab === 'clothing' }"
            @click="infoTab = 'clothing'"
          >
            Sun-smart Clothing
          </button>
          <button
            type="button"
            class="homepage__nav-tab"
            :class="{ 'homepage__nav-tab--active': infoTab === 'resources' }"
            @click="infoTab = 'resources'"
          >
            Resources
          </button>
        </nav>
      </div>
    </header>

    <main class="homepage__main">
      <div class="homepage__container">
        <!-- Hero: two-column UV dashboard (pastel gradient card) -->
        <section class="homepage__hero" aria-label="UV dashboard">
          <UVDashboard />
        </section>

        <!-- Below-hero: tab content (Impact = UV Impacts + Why; others coming soon) -->
        <div class="homepage__columns">
          <div class="homepage__col homepage__col--left">
            <section class="homepage__why">
              <h2 class="homepage__why-title">Why UV Protection Matters</h2>
              <p class="homepage__why-text">
                Australia has some of the highest UV levels in the world. Prolonged exposure to
                ultraviolet radiation can damage your skin and eyes and increase the risk of skin
                cancer. Understanding UV impacts helps you make informed choices about sun protection.
              </p>
              <p class="homepage__why-text">
                Check the max UV index for your location and take simple steps: seek shade when the
                UV is high, wear protective clothing and a hat, use broad-spectrum sunscreen, and
                wear sunglasses.
              </p>
            </section>

            <section v-if="infoTab === 'uv-impacts'">
              <UVImpacts />
            </section>
            <section v-else class="homepage__coming-wrap">
              <p class="homepage__coming">Content for this section is coming soon.</p>
            </section>
          </div>

          <aside class="homepage__col homepage__col--right" aria-label="Skin types">
            <SkinTypes />
          </aside>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.homepage {
  min-height: 100vh;
  /* Design system colours */
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
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  flex-wrap: wrap;
}
.homepage__brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.homepage__brand-text {
  font-weight: 700;
  font-size: 1.25rem;
  letter-spacing: 0.02em;
  color: var(--uv-primary);
}
.homepage__brand-icon {
  font-size: 1.1rem;
  color: var(--uv-primary);
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
.homepage__nav-tab:hover {
  color: var(--uv-text);
}
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

.homepage__main {
  padding: 2rem 1.5rem 3rem;
}
.homepage__container {
  max-width: 1280px;
  margin: 0 auto;
}
.homepage__hero {
  margin-bottom: 2rem;
}

/* Below-hero: soft white cards, design system */
.homepage__columns {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}
.homepage__col {
  min-width: 0;
}
.homepage__why {
  margin-bottom: 2rem;
  padding: 1.5rem 1.75rem;
  background: #fff;
  border-radius: 16px;
  border: 1px solid var(--uv-grid);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
}
.homepage__why-title {
  margin: 0 0 1rem;
  font-size: 1.375rem;
  font-weight: 700;
  color: var(--uv-primary);
  letter-spacing: -0.02em;
}
.homepage__why-text {
  margin: 0 0 0.75rem;
  font-size: 1rem;
  line-height: 1.65;
  color: var(--uv-text-muted);
}
.homepage__why-text:last-child {
  margin-bottom: 0;
}
.homepage__coming-wrap {
  padding-top: 0.5rem;
}
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
  .homepage__main {
    padding: 2.5rem 2rem 3.5rem;
  }
  .homepage__columns {
    flex-direction: row;
    align-items: flex-start;
    gap: 2.5rem;
  }
  .homepage__col--left {
    flex: 2;
    min-width: 0;
  }
  .homepage__col--right {
    flex: 1.2;
    min-width: 320px;
  }
}
</style>
