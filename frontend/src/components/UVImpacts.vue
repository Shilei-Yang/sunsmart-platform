<!--
  UV Impacts — Card-style section: short-term and long-term effects.
  Content unchanged; layout and styling aligned with Hi-Fi prototype.
-->
<script setup>
const shortTerm = [
  'Sunburn',
  'Skin redness',
  'Peeling',
]
const longTerm = [
  'Premature skin ageing',
  'Pigmentation',
  'Increased skin cancer risk',
]
</script>

<template>
  <section class="uv-impacts">
    <h2 class="uv-impacts__title">UV Impacts</h2>
    <p class="uv-impacts__intro">
      Understanding how UV exposure affects your skin can help you stay sun smart.
    </p>
    <div class="uv-impacts__grid">
      <div class="uv-impacts__card">
        <h3 class="uv-impacts__card-title">Short-term effects</h3>
        <ul class="uv-impacts__list">
          <li v-for="item in shortTerm" :key="item" class="uv-impacts__item">
            {{ item }}
          </li>
        </ul>
      </div>
      <div class="uv-impacts__card">
        <h3 class="uv-impacts__card-title">Long-term effects</h3>
        <ul class="uv-impacts__list">
          <li v-for="item in longTerm" :key="item" class="uv-impacts__item">
            {{ item }}
          </li>
        </ul>
      </div>
    </div>
  </section>
</template>

<style scoped>
.uv-impacts {
  margin-bottom: 0;
}
.uv-impacts__title {
  margin: 0 0 0.5rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: #0369a1;
  letter-spacing: -0.02em;
}
.uv-impacts__intro {
  margin: 0 0 1.25rem;
  font-size: 0.9375rem;
  color: #64748b;
  line-height: 1.55;
}
.uv-impacts__grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
}
.uv-impacts__card {
  background: #fff;
  border-radius: 16px;
  padding: 1.5rem 1.75rem;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
}
.uv-impacts__card-title {
  margin: 0 0 0.75rem;
  font-size: 1.0625rem;
  font-weight: 700;
  color: #334155;
}
.uv-impacts__list {
  margin: 0;
  padding-left: 1.25rem;
}
.uv-impacts__item {
  margin-bottom: 0.4rem;
  font-size: 0.9375rem;
  color: #475569;
  line-height: 1.45;
}
.uv-impacts__item:last-child {
  margin-bottom: 0;
}

@media (max-width: 600px) {
  .uv-impacts__grid {
    grid-template-columns: 1fr;
  }
}
</style>
