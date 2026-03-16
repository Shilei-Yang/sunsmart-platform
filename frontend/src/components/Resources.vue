<script setup>
import heroBg from '@/assets/pexels-rpnickson-2647973.jpg'
import bannerBg from '@/assets/pexels-kindelmedia-7862532.jpg'
import advicePhoto from '@/assets/pexels-rdne-12169028.jpg'

const organisations = [
  {
    name: 'Cancer Council Australia',
    desc: 'Sun safety education and skin cancer prevention resources.',
    url: 'https://www.cancer.org.au/',
    color: '#D8613C',
  },
  {
    name: 'ARPANSA',
    desc: 'UV index data and radiation safety information from the Australian Radiation Protection and Nuclear Safety Agency.',
    url: 'https://www.arpansa.gov.au/our-services/monitoring/ultraviolet-radiation-monitoring',
    color: '#2563eb',
  },
  {
    name: 'Bureau of Meteorology',
    desc: 'Official UV index forecasts and weather updates for Australia.',
    url: 'http://www.bom.gov.au/uv/',
    color: '#16a34a',
  },
]

const helplines = [
  {
    name: 'Cancer Council Information Line',
    number: '13 11 20',
    desc: 'Free support on cancer prevention, screening, and treatment.',
    url: 'https://www.cancer.org.au/about-us/how-we-can-help/cancer-council-13-11-20',
  },
  {
    name: 'Healthdirect Australia',
    number: '1800 022 222',
    desc: '24/7 health advice from registered nurses.',
    url: 'https://www.healthdirect.gov.au/',
  },
  {
    name: 'Lifeline Australia',
    number: '13 11 14',
    desc: 'Confidential support for mental health and wellbeing.',
    url: 'https://www.lifeline.org.au/',
  },
]

const warningSignsLeft = [
  'New or changing moles',
  'Unusual skin spots or lesions',
]
const warningSignsRight = [
  'Severe sunburn or blistering',
  'Skin changes that persist over time',
]
</script>

<template>
  <section class="res">
    <!-- Hero -->
    <div class="res__hero">
      <img :src="heroBg" alt="Group of young people enjoying the beach" class="res__hero-bg" />
      <div class="res__hero-overlay" />
      <div class="res__hero-content">
        <span class="res__eyebrow">Resources</span>
        <h2 class="res__headline">
          Your sun safety <span class="res__accent">toolkit</span>
        </h2>
        <p class="res__hero-text">
          Trusted organisations, helplines, and guidance to help you
          and the people you care about stay safe under the Australian sun.
        </p>
      </div>
    </div>

    <!-- Trusted Organisations -->
    <div class="res__block">
      <span class="res__eyebrow">Trusted Sun Safety Organisations</span>
      <h3 class="res__block-title">Reliable sources you can count on</h3>
      <div class="res__org-grid">
        <a
          v-for="org in organisations"
          :key="org.name"
          :href="org.url"
          target="_blank"
          rel="noopener noreferrer"
          class="res__org-card uv-card"
        >
          <span class="res__org-dot" :style="{ background: org.color }" />
          <h4 class="res__org-name">{{ org.name }}</h4>
          <p class="res__org-desc">{{ org.desc }}</p>
          <span class="res__org-link">
            Visit website
            <span aria-hidden="true">&rarr;</span>
          </span>
        </a>
      </div>
    </div>

    <!-- Photo banner -->
    <div class="res__banner">
      <img :src="bannerBg" alt="Children playing on a sunny beach" class="res__banner-bg" />
      <div class="res__banner-overlay" />
      <p class="res__banner-text">
        The habits we build today protect the people we love tomorrow.
      </p>
    </div>

    <!-- Helplines -->
    <div class="res__block">
      <span class="res__eyebrow">Helplines and Support</span>
      <h3 class="res__block-title">Someone is always here to help</h3>
      <div class="res__help-grid">
        <a
          v-for="line in helplines"
          :key="line.name"
          :href="line.url"
          target="_blank"
          rel="noopener noreferrer"
          class="res__help-card uv-card"
        >
          <h4 class="res__help-name">{{ line.name }}</h4>
          <span class="res__help-number">{{ line.number }}</span>
          <p class="res__help-desc">{{ line.desc }}</p>
        </a>
      </div>
    </div>

    <!-- When to seek medical advice -->
    <div class="res__advice uv-card">
      <div class="res__advice-content">
        <span class="res__eyebrow">When to Seek Medical Advice</span>
        <h3 class="res__block-title">Consult a healthcare professional if you notice</h3>
        <div class="res__signs">
          <ul class="res__signs-list">
            <li v-for="sign in warningSignsLeft" :key="sign" class="res__signs-item">{{ sign }}</li>
          </ul>
          <ul class="res__signs-list">
            <li v-for="sign in warningSignsRight" :key="sign" class="res__signs-item">{{ sign }}</li>
          </ul>
        </div>
        <p class="res__advice-note">
          Early detection saves lives. If in doubt, book a skin check with your GP or dermatologist.
        </p>
      </div>
      <div class="res__advice-photo-wrap">
        <img :src="advicePhoto" alt="Young people playing beach volleyball outdoors" class="res__advice-photo" />
      </div>
    </div>

    <!-- Bottom callout -->
    <div class="res__callout">
      <p class="res__callout-text">
        <strong>Knowledge is your best protection.</strong>
        Share these resources with friends and family to keep everyone sun-safe.
      </p>
    </div>
  </section>
</template>

<style scoped>
.res {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

/* Hero */
.res__hero {
  position: relative;
  overflow: hidden;
  border-radius: 20px;
  min-height: 340px;
  display: flex;
  align-items: flex-end;
}
.res__hero-bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 55%;
}
.res__hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to top,
    rgba(30, 20, 12, 0.9) 0%,
    rgba(30, 20, 12, 0.55) 50%,
    rgba(30, 20, 12, 0.15) 80%,
    transparent 100%
  );
  pointer-events: none;
}
.res__hero-content {
  position: relative;
  z-index: 1;
  padding: 2rem 2rem 1.75rem;
  width: 100%;
}
.res__eyebrow {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--uv-primary, #D8613C);
  margin-bottom: 0.4rem;
}
.res__headline {
  margin: 0 0 0.6rem;
  font-size: 1.5rem;
  font-weight: 800;
  color: #fff;
  letter-spacing: -0.02em;
  line-height: 1.3;
  text-shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
}
.res__accent {
  color: #ffb088;
}
.res__hero-text {
  margin: 0;
  font-size: 0.9375rem;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.8);
  max-width: 52ch;
  text-shadow: 0 1px 6px rgba(0, 0, 0, 0.2);
}

/* Block headings */
.res__block {
  padding: 0;
}
.res__block-title {
  margin: 0 0 0.75rem;
  font-size: 1.1875rem;
  font-weight: 700;
  color: var(--uv-text, #4A4A4A);
  letter-spacing: -0.01em;
}

/* Organisation cards */
.res__org-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 0.85rem;
}
.res__org-card {
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
  text-decoration: none;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.res__org-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
}
.res__org-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-bottom: 0.75rem;
  flex-shrink: 0;
}
.res__org-name {
  margin: 0 0 0.35rem;
  font-size: 1rem;
  font-weight: 700;
  color: var(--uv-text, #4A4A4A);
}
.res__org-desc {
  margin: 0 0 0.85rem;
  font-size: 0.8125rem;
  color: var(--uv-text-muted, #8A8A8A);
  line-height: 1.55;
  flex: 1;
}
.res__org-link {
  font-size: 0.8125rem;
  font-weight: 700;
  color: var(--uv-primary, #D8613C);
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
}

/* Photo banner */
.res__banner {
  position: relative;
  overflow: hidden;
  border-radius: 16px;
  min-height: 160px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.res__banner-bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 45%;
}
.res__banner-overlay {
  position: absolute;
  inset: 0;
  background: rgba(30, 20, 12, 0.5);
  pointer-events: none;
}
.res__banner-text {
  position: relative;
  z-index: 1;
  margin: 0;
  padding: 1.5rem 2rem;
  font-size: 1.125rem;
  font-weight: 700;
  color: #fff;
  text-align: center;
  line-height: 1.5;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  max-width: 44ch;
}

/* Helpline cards */
.res__help-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 0.85rem;
}
.res__help-card {
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
  text-decoration: none;
  border-left: 4px solid var(--uv-primary, #D8613C);
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.res__help-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
}
.res__help-name {
  margin: 0 0 0.4rem;
  font-size: 0.9375rem;
  font-weight: 700;
  color: var(--uv-text, #4A4A4A);
}
.res__help-number {
  display: inline-block;
  font-size: 1.375rem;
  font-weight: 800;
  color: var(--uv-primary, #D8613C);
  margin-bottom: 0.5rem;
  letter-spacing: 0.02em;
}
.res__help-desc {
  margin: 0;
  font-size: 0.8125rem;
  color: var(--uv-text-muted, #8A8A8A);
  line-height: 1.55;
}

/* Medical advice */
.res__advice {
  display: flex;
  gap: 1.5rem;
  overflow: hidden;
  padding: 0;
}
.res__advice-content {
  flex: 1;
  padding: 1.75rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.res__signs {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}
.res__signs-list {
  margin: 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex: 1;
  min-width: 160px;
}
.res__signs-item {
  position: relative;
  padding-left: 1.25rem;
  font-size: 0.875rem;
  color: var(--uv-text, #4A4A4A);
  line-height: 1.5;
}
.res__signs-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0.45em;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #D44A4A;
}
.res__advice-note {
  margin: 0;
  font-size: 0.8125rem;
  color: var(--uv-text-muted, #8A8A8A);
  line-height: 1.55;
  font-style: italic;
}
.res__advice-photo-wrap {
  flex: 0 0 38%;
  max-width: 300px;
  min-height: 240px;
}
.res__advice-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Bottom callout */
.res__callout {
  padding: 1.25rem 1.5rem;
  background: linear-gradient(135deg, #D8613C 0%, #c44e2c 100%);
  border-radius: 14px;
  text-align: center;
}
.res__callout-text {
  margin: 0;
  font-size: 0.9375rem;
  color: #fff;
  line-height: 1.6;
}
.res__callout-text strong {
  display: block;
  font-size: 1rem;
  margin-bottom: 0.25rem;
}

/* Mobile */
@media (max-width: 640px) {
  .res__hero {
    min-height: 280px;
  }
  .res__hero-content {
    padding: 1.5rem 1.25rem;
  }
  .res__headline {
    font-size: 1.25rem;
  }
  .res__org-grid,
  .res__help-grid {
    grid-template-columns: 1fr;
  }
  .res__advice {
    flex-direction: column;
  }
  .res__advice-photo-wrap {
    flex: none;
    max-width: 100%;
    min-height: 180px;
    max-height: 200px;
    order: -1;
  }
  .res__advice-content {
    padding: 1.25rem;
  }
}
</style>
