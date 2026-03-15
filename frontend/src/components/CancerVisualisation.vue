<!--
  CancerVisualisation — Placeholder for skin cancer data chart.
  Reusable component; chart data will be wired in later.
-->
<script setup>
// Chart data will be wired from backend when available
</script>

<template>
  <section class="cancer-viz">
    <h2 class="cancer-viz__title">Skin Cancers in Australia</h2>
    <p class="cancer-viz__subtitle">
      Australia has one of the highest skin cancer rates globally, with a significant number of cases
      linked to excessive UV exposure during outdoor activities.
    </p>
    <div class="cancer-viz__card uv-card">
      <h3 class="cancer-viz__card-title">Cancer Statistics</h3>
      <div class="cancer-viz__chart-area" aria-label="Chart placeholder">
        <p class="cancer-viz__placeholder">
          Cancer visualisation will be displayed here
        </p>
      </div>
    </div>
  </section>
</template>

<style scoped>
.cancer-viz {
  margin-top: 2rem;
  margin-bottom: 2rem;
}
.cancer-viz__title {
  margin: 0 0 0.5rem;
  font-size: 1.375rem;
  font-weight: 700;
  color: var(--uv-primary, #D8613C);
  letter-spacing: -0.02em;
}
.cancer-viz__subtitle {
  margin: 0 0 1.5rem;
  font-size: 1rem;
  line-height: 1.65;
  color: var(--uv-text-muted, #8A8A8A);
}
.cancer-viz__card-title {
  margin: 0 0 1rem;
  font-size: 1.0625rem;
  font-weight: 700;
  color: var(--uv-text, #4A4A4A);
}
.cancer-viz__chart-area {
  min-height: 280px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(248, 247, 245, 0.6);
  border-radius: 12px;
  border: 1px dashed var(--uv-grid, #E6E1DA);
}
.cancer-viz__placeholder {
  margin: 0;
  font-size: 0.9375rem;
  color: var(--uv-text-muted, #8A8A8A);
}
</style>
