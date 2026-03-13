<!--
  Homepage — Desktop layout aligned with Hi-Fi prototype.
  Hero UV dashboard (blue gradient), nav tabs, Why UV Protection, UV Impacts, Skin Types.
  Backend integration to /api/uv unchanged; no personalised experience logic.
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
    <header class="homepage__header">
      <div class="homepage__header-inner">
        <h1 class="homepage__title">Sun Smart Platform</h1>
        <p class="homepage__tagline">UV protection awareness</p>
      </div>
    </header>

    <main class="homepage__main">
      <div class="homepage__container">
        <!-- Hero: large UV dashboard (blue gradient, full width within container) -->
        <section class="homepage__hero" aria-label="UV dashboard">
          <UVDashboard />
        </section>

        <!-- Navigation tabs (prototype-style; other tabs not functional yet) -->
        <nav class="homepage__nav" aria-label="Information sections">
          <button
            type="button"
            class="homepage__nav-tab"
            :class="{ 'homepage__nav-tab--active': infoTab === 'uv-impacts' }"
            @click="infoTab = 'uv-impacts'"
          >
            UV Impacts
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

        <!-- Two-column content: left = Why + tab content, right = Skin Types -->
        <div class="homepage__columns">
          <div class="homepage__col homepage__col--left">
            <!-- Why UV Protection Matters — stronger heading, balanced layout -->
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
  background: #f8fafc;
  color: #1e293b;
}
.homepage__header {
  padding: 1.5rem 1.5rem 1rem;
  border-bottom: 1px solid #e2e8f0;
  background: linear-gradient(180deg, #e0f2fe 0%, #f0f9ff 40%, #fff 100%);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}
.homepage__header-inner {
  max-width: 1280px;
  margin: 0 auto;
}
.homepage__title {
  margin: 0;
  font-size: 1.625rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  color: #0f172a;
}
.homepage__tagline {
  margin: 0.25rem 0 0;
  font-size: 0.9375rem;
  color: #0369a1;
  font-weight: 500;
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

.homepage__nav {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e2e8f0;
}
.homepage__nav-tab {
  padding: 0.6rem 1rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #64748b;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  cursor: pointer;
  transition: color 0.2s, border-color 0.2s, background 0.2s;
}
.homepage__nav-tab:hover {
  color: #0369a1;
  border-color: #bae6fd;
  background: #f0f9ff;
}
.homepage__nav-tab--active {
  color: #0369a1;
  border-color: #0ea5e9;
  background: #e0f2fe;
  box-shadow: 0 2px 6px rgba(14, 165, 233, 0.15);
}

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
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
}
.homepage__why-title {
  margin: 0 0 1rem;
  font-size: 1.375rem;
  font-weight: 700;
  color: #0369a1;
  letter-spacing: -0.02em;
}
.homepage__why-text {
  margin: 0 0 0.75rem;
  font-size: 1rem;
  line-height: 1.65;
  color: #475569;
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
  color: #94a3b8;
  font-size: 0.9375rem;
  border-radius: 16px;
  background: #fff;
  border: 2px dashed #e2e8f0;
}

@media (min-width: 900px) {
  .homepage__title {
    font-size: 1.875rem;
  }
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
