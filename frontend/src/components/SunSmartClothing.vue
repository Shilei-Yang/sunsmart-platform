<script setup>
import heroBg from '@/assets/pexels-cottonbro-5263493.jpg'
import hatPhoto from '@/assets/pexels-jude-stevens-270399-984619.jpg'
import bannerPhoto from '@/assets/pexels-busranur-aydin-3800407-33694952.jpg'

const essentials = [
  {
    icon: '👒',
    title: 'Wide-Brim Hat',
    desc: 'Shields face, ears & neck. Aim for 7.5 cm+ brim.',
  },
  {
    icon: '👕',
    title: 'UPF-Rated Clothing',
    desc: 'Look for UPF 30+ or 50+ labels on the tag.',
  },
  {
    icon: '🕶️',
    title: 'UV-Protective Sunglasses',
    desc: 'Wraparound + UV400 protection for eyes and surrounding skin.',
  },
  {
    icon: '🧥',
    title: 'Long Sleeves & Pants',
    desc: 'Lightweight, breathable fabrics that cover more skin.',
  },
  {
    icon: '⛱️',
    title: 'Seek Shade',
    desc: 'Trees, umbrellas or shelters — especially 10 am to 4 pm.',
  },
]

const upfRatings = [
  { rating: 'UPF 15-24', label: 'Good', blocks: '93-95%', color: '#ca8a04' },
  { rating: 'UPF 25-39', label: 'Very Good', blocks: '96-97%', color: '#ea580c' },
  { rating: 'UPF 40-50+', label: 'Excellent', blocks: '97.5%+', color: '#16a34a' },
]
</script>

<template>
  <section class="clothing">
    <!-- Hero with background image -->
    <div class="clothing__hero">
      <img :src="heroBg" alt="Two people walking on sand in sun-protective long clothing" class="clothing__hero-bg" />
      <div class="clothing__hero-overlay" />
      <div class="clothing__hero-content">
        <span class="clothing__eyebrow">Sun-Smart Clothing</span>
        <h2 class="clothing__headline">
          Dress smart. <span class="clothing__accent">Stay protected.</span>
        </h2>
        <p class="clothing__hero-text">
          The right clothing is your first line of defence against UV.
        </p>
      </div>
    </div>

    <!-- Essentials grid -->
    <div class="clothing__section">
      <h3 class="clothing__section-title">5 Essentials for UV Protection</h3>
      <div class="clothing__grid">
        <div
          v-for="item in essentials"
          :key="item.title"
          class="clothing__card"
        >
          <span class="clothing__card-icon" aria-hidden="true">{{ item.icon }}</span>
          <h4 class="clothing__card-title">{{ item.title }}</h4>
          <p class="clothing__card-desc">{{ item.desc }}</p>
        </div>
      </div>
    </div>

    <!-- Visual banner -->
    <div class="clothing__banner">
      <img :src="bannerPhoto" alt="Child outdoors wearing a wide-brim sun hat" class="clothing__banner-img" />
      <div class="clothing__banner-overlay" />
      <p class="clothing__banner-text">
        Protection starts early. Sun-smart habits today shape healthier skin for life.
      </p>
    </div>

    <!-- UPF rating guide -->
    <div class="clothing__upf uv-card">
      <div class="clothing__upf-text">
        <span class="clothing__eyebrow">Understanding UPF Ratings</span>
        <h3 class="clothing__section-title">Not all fabrics are equal</h3>
        <p class="clothing__upf-intro">
          UPF measures how much UV a fabric blocks. Higher = better.
        </p>
        <div class="clothing__upf-ratings">
          <div
            v-for="item in upfRatings"
            :key="item.rating"
            class="clothing__upf-row"
          >
            <span class="clothing__upf-badge" :style="{ background: item.color }">{{ item.rating }}</span>
            <span class="clothing__upf-label">{{ item.label }}</span>
            <span class="clothing__upf-blocks">Blocks {{ item.blocks }} of UV</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Did you know + beach photo -->
    <div class="clothing__know">
      <div class="clothing__know-photo-wrap">
        <img :src="hatPhoto" alt="Straw sun hat by a poolside" class="clothing__know-photo" />
      </div>
      <div class="clothing__know-content">
        <span class="clothing__eyebrow">Did You Know?</span>
        <h3 class="clothing__section-title">Fabric colour and weave matter</h3>
        <p class="clothing__know-text">
          Hold fabric up to light — if you can see through it, UV can get through it too.
        </p>
        <div class="clothing__know-tips">
          <div class="clothing__know-tip">
            <span class="clothing__know-dot clothing__know-dot--dark" />
            <span>Dark colours absorb more UV</span>
          </div>
          <div class="clothing__know-tip">
            <span class="clothing__know-dot clothing__know-dot--tight" />
            <span>Tight weave blocks more rays</span>
          </div>
          <div class="clothing__know-tip">
            <span class="clothing__know-dot clothing__know-dot--dry" />
            <span>Dry fabric protects better than wet</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom callout -->
    <div class="clothing__callout">
      <p class="clothing__callout-text">
        <strong>Clothing + sunscreen + shade = your best defence.</strong>
        No single method blocks 100% of UV — layer up.
      </p>
    </div>
  </section>
</template>

<style scoped>
.clothing {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

/* Hero */
.clothing__hero {
  position: relative;
  overflow: hidden;
  border-radius: 20px;
  min-height: 320px;
  display: flex;
  align-items: flex-end;
}
.clothing__hero-bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 30%;
}
.clothing__hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to top,
    rgba(30, 20, 12, 0.88) 0%,
    rgba(30, 20, 12, 0.6) 45%,
    rgba(30, 20, 12, 0.2) 75%,
    transparent 100%
  );
  pointer-events: none;
}
.clothing__hero-content {
  position: relative;
  z-index: 1;
  padding: 2rem 2rem 1.75rem;
  width: 100%;
}
.clothing__eyebrow {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--uv-primary, #D8613C);
  margin-bottom: 0.4rem;
}
.clothing__headline {
  margin: 0 0 0.6rem;
  font-size: 1.5rem;
  font-weight: 800;
  color: #fff;
  letter-spacing: -0.02em;
  line-height: 1.3;
  text-shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
}
.clothing__accent {
  color: #ffb088;
}
.clothing__hero-text {
  margin: 0;
  font-size: 0.9375rem;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.8);
  max-width: 52ch;
  text-shadow: 0 1px 6px rgba(0, 0, 0, 0.2);
}

/* Section titles */
.clothing__section {
  padding: 0;
}
.clothing__section-title {
  margin: 0 0 0.75rem;
  font-size: 1.1875rem;
  font-weight: 700;
  color: var(--uv-text, #4A4A4A);
  letter-spacing: -0.01em;
}

/* Essentials grid */
.clothing__grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 0.85rem;
}
.clothing__card {
  background: var(--uv-card, #fff);
  border: 1px solid var(--uv-grid, #E6E1DA);
  border-radius: 16px;
  padding: 1.35rem 1.25rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.clothing__card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
}
.clothing__card-icon {
  display: block;
  font-size: 1.75rem;
  margin-bottom: 0.6rem;
}
.clothing__card-title {
  margin: 0 0 0.35rem;
  font-size: 0.9375rem;
  font-weight: 700;
  color: var(--uv-text, #4A4A4A);
}
.clothing__card-desc {
  margin: 0;
  font-size: 0.8125rem;
  color: var(--uv-text-muted, #8A8A8A);
  line-height: 1.55;
}

/* Visual banner */
.clothing__banner {
  position: relative;
  overflow: hidden;
  border-radius: 16px;
  min-height: 160px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.clothing__banner-img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 40%;
}
.clothing__banner-overlay {
  position: absolute;
  inset: 0;
  background: rgba(30, 20, 12, 0.55);
  pointer-events: none;
}
.clothing__banner-text {
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

/* UPF Guide */
.clothing__upf {
  padding: 1.75rem;
}
.clothing__upf-intro {
  margin: 0 0 1.25rem;
  font-size: 0.9375rem;
  color: var(--uv-text-muted, #8A8A8A);
  line-height: 1.6;
}
.clothing__upf-ratings {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}
.clothing__upf-row {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  padding: 0.7rem 1rem;
  background: var(--uv-bg, #F4F1EC);
  border-radius: 10px;
  flex-wrap: wrap;
}
.clothing__upf-badge {
  padding: 0.25rem 0.7rem;
  font-size: 0.75rem;
  font-weight: 700;
  color: #fff;
  border-radius: 999px;
  white-space: nowrap;
}
.clothing__upf-label {
  font-size: 0.9375rem;
  font-weight: 700;
  color: var(--uv-text, #4A4A4A);
  min-width: 80px;
}
.clothing__upf-blocks {
  font-size: 0.8125rem;
  color: var(--uv-text-muted, #8A8A8A);
  margin-left: auto;
}

/* Did you know */
.clothing__know {
  display: flex;
  gap: 1.5rem;
  background: var(--uv-card, #fff);
  border: 1px solid var(--uv-grid, #E6E1DA);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
}
.clothing__know-photo-wrap {
  flex: 0 0 40%;
  max-width: 280px;
  min-height: 240px;
}
.clothing__know-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.clothing__know-content {
  flex: 1;
  padding: 1.5rem 1.5rem 1.5rem 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.clothing__know-text {
  margin: 0 0 1rem;
  font-size: 0.9375rem;
  color: var(--uv-text-muted, #8A8A8A);
  line-height: 1.6;
}
.clothing__know-tips {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.clothing__know-tip {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--uv-text, #4A4A4A);
}
.clothing__know-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}
.clothing__know-dot--dark {
  background: #4A3228;
}
.clothing__know-dot--tight {
  background: var(--uv-primary, #D8613C);
}
.clothing__know-dot--dry {
  background: #3A9E5C;
}

/* Bottom callout */
.clothing__callout {
  padding: 1.25rem 1.5rem;
  background: linear-gradient(135deg, #D8613C 0%, #c44e2c 100%);
  border-radius: 14px;
  text-align: center;
}
.clothing__callout-text {
  margin: 0;
  font-size: 0.9375rem;
  color: #fff;
  line-height: 1.6;
}
.clothing__callout-text strong {
  display: block;
  font-size: 1rem;
  margin-bottom: 0.25rem;
}

/* Mobile */
@media (max-width: 640px) {
  .clothing__hero {
    min-height: 260px;
  }
  .clothing__hero-content {
    padding: 1.5rem 1.25rem;
  }
  .clothing__headline {
    font-size: 1.25rem;
  }
  .clothing__grid {
    grid-template-columns: 1fr;
  }
  .clothing__know {
    flex-direction: column;
  }
  .clothing__know-photo-wrap {
    flex: none;
    max-width: 100%;
    min-height: 180px;
    max-height: 200px;
  }
  .clothing__know-content {
    padding: 1.25rem;
  }
  .clothing__upf {
    padding: 1.25rem;
  }
  .clothing__upf-blocks {
    margin-left: 0;
  }
}
</style>
