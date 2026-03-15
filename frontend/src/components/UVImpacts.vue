<!--
  UV Impacts — Split-panel card: photo left, rich content right.
  Short-term uses warm amber accents; long-term uses deeper red accents.
  No emojis — pure CSS accent bars and clean typography.
-->
<script setup>
const shortTerm = [
  { label: 'Sunburn', desc: 'Redness and pain from overexposure' },
  { label: 'Skin irritation', desc: 'Tenderness and peeling within days' },
  { label: 'Eye damage', desc: 'Photokeratitis from unprotected eyes' },
]
const longTerm = [
  { label: 'Premature ageing', desc: 'Wrinkles, fine lines and dark spots' },
  { label: 'DNA damage', desc: 'Mutations that accumulate over time' },
  { label: 'Skin cancer risk', desc: 'Melanoma and non-melanoma cancers' },
]

import impactPhoto from '@/assets/pexels-olly-800323.jpg'
</script>

<template>
  <section class="uv-impacts">
    <div class="uv-impacts__split">
      <!-- Left: photo panel -->
      <div class="uv-impacts__photo-panel">
        <img
          :src="impactPhoto"
          alt="Person standing in strong sunlight outdoors"
          class="uv-impacts__photo"
        />
        <div class="uv-impacts__photo-overlay" />
        <span class="uv-impacts__photo-badge">UV Exposure</span>
      </div>

      <!-- Right: content panel -->
      <div class="uv-impacts__content">
        <p class="uv-impacts__eyebrow">Know the risks</p>
        <h2 class="uv-impacts__title">How UV Affects<br />Your Skin</h2>
        <p class="uv-impacts__intro">
          Even brief unprotected exposure can trigger damage.
          Here's what happens at different timescales.
        </p>

        <div class="uv-impacts__columns">
          <!-- Short-term -->
          <div class="uv-impacts__group">
            <h3 class="uv-impacts__group-label">
              <span class="uv-impacts__group-dot uv-impacts__group-dot--short" />
              Short-term
            </h3>
            <div class="uv-impacts__cards">
              <div
                v-for="(item, i) in shortTerm"
                :key="item.label"
                class="uv-impacts__mini-card uv-impacts__mini-card--short"
              >
                <span class="uv-impacts__mini-num uv-impacts__mini-num--short">{{ i + 1 }}</span>
                <div>
                  <p class="uv-impacts__mini-label">{{ item.label }}</p>
                  <p class="uv-impacts__mini-desc">{{ item.desc }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Long-term -->
          <div class="uv-impacts__group">
            <h3 class="uv-impacts__group-label">
              <span class="uv-impacts__group-dot uv-impacts__group-dot--long" />
              Long-term
            </h3>
            <div class="uv-impacts__cards">
              <div
                v-for="(item, i) in longTerm"
                :key="item.label"
                class="uv-impacts__mini-card uv-impacts__mini-card--long"
              >
                <span class="uv-impacts__mini-num uv-impacts__mini-num--long">{{ i + 1 }}</span>
                <div>
                  <p class="uv-impacts__mini-label">{{ item.label }}</p>
                  <p class="uv-impacts__mini-desc">{{ item.desc }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.uv-impacts {
  margin-top: 2rem;
  margin-bottom: 0;
}

.uv-impacts__split {
  display: flex;
  overflow: hidden;
  border-radius: 20px;
  background: var(--uv-card, #fff);
  border: 1px solid var(--uv-grid, #E6E1DA);
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
  min-height: 360px;
}

/* Photo panel */
.uv-impacts__photo-panel {
  position: relative;
  flex: 0 0 36%;
  min-height: 360px;
  overflow: hidden;
}
.uv-impacts__photo {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center top;
}
.uv-impacts__photo-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to right,
    transparent 40%,
    rgba(255, 255, 255, 0.45) 80%,
    rgba(255, 255, 255, 0.95) 100%
  );
  pointer-events: none;
}
.uv-impacts__photo-badge {
  position: absolute;
  top: 1rem;
  left: 1rem;
  padding: 0.3rem 0.75rem;
  font-size: 0.6875rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #fff;
  background: rgba(216, 97, 60, 0.85);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border-radius: 999px;
}

/* Content panel */
.uv-impacts__content {
  flex: 1;
  padding: 2.25rem 2rem 2rem 1.5rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.uv-impacts__eyebrow {
  margin: 0 0 0.3rem;
  font-size: 0.6875rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--uv-primary, #D8613C);
}
.uv-impacts__title {
  margin: 0 0 0.5rem;
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--uv-text, #4A4A4A);
  letter-spacing: -0.03em;
  line-height: 1.2;
}
.uv-impacts__intro {
  margin: 0 0 1.5rem;
  font-size: 0.875rem;
  color: var(--uv-text-muted, #8A8A8A);
  line-height: 1.6;
  max-width: 50ch;
}

/* Two-column groups */
.uv-impacts__columns {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
}

.uv-impacts__group-label {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  margin: 0 0 0.65rem;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--uv-text, #4A4A4A);
}
.uv-impacts__group-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
}
.uv-impacts__group-dot--short { background: #e49a2a; }
.uv-impacts__group-dot--long  { background: var(--uv-danger, #D44A4A); }

/* Mini-cards */
.uv-impacts__cards {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.uv-impacts__mini-card {
  display: flex;
  align-items: flex-start;
  gap: 0.65rem;
  padding: 0.6rem 0.75rem;
  border-radius: 10px;
  border: 1px solid var(--uv-grid, #E6E1DA);
  transition: box-shadow 0.2s, border-color 0.2s;
}
.uv-impacts__mini-card:hover {
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
}
.uv-impacts__mini-card--short {
  border-left: 3px solid rgba(228, 154, 42, 0.5);
  background: rgba(228, 154, 42, 0.03);
}
.uv-impacts__mini-card--short:hover { border-left-color: #e49a2a; }
.uv-impacts__mini-card--long {
  border-left: 3px solid rgba(212, 74, 74, 0.5);
  background: rgba(212, 74, 74, 0.03);
}
.uv-impacts__mini-card--long:hover { border-left-color: #D44A4A; }

/* Numbered circle */
.uv-impacts__mini-num {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  font-size: 0.6875rem;
  font-weight: 700;
  line-height: 1;
  margin-top: 0.1rem;
  color: #fff;
}
.uv-impacts__mini-num--short { background: #e49a2a; }
.uv-impacts__mini-num--long  { background: var(--uv-danger, #D44A4A); }

.uv-impacts__mini-label {
  margin: 0;
  font-size: 0.8125rem;
  font-weight: 700;
  color: var(--uv-text, #4A4A4A);
  line-height: 1.3;
}
.uv-impacts__mini-desc {
  margin: 0.1rem 0 0;
  font-size: 0.72rem;
  color: var(--uv-text-muted, #8A8A8A);
  line-height: 1.4;
}

/* Mobile */
@media (max-width: 700px) {
  .uv-impacts__split {
    flex-direction: column;
    min-height: auto;
  }
  .uv-impacts__photo-panel {
    flex: none;
    height: 200px;
    min-height: auto;
  }
  .uv-impacts__photo-overlay {
    background: linear-gradient(
      to bottom,
      transparent 40%,
      rgba(255, 255, 255, 0.7) 80%,
      rgba(255, 255, 255, 1) 100%
    );
  }
  .uv-impacts__content {
    padding: 1.25rem 1.5rem 1.5rem;
  }
  .uv-impacts__columns {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}
</style>
