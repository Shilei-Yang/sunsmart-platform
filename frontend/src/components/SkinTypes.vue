<!--
  Skin Types — Fitzpatrick scale in a responsive grid.
  Desktop: 2–3 columns; mobile: single column. Card styling aligned with prototype.
-->
<script setup>
const skinTypes = [
  {
    type: 'Type I',
    description: 'Pale skin, often with freckles. Always burns, never tans. Highest sun sensitivity.',
  },
  {
    type: 'Type II',
    description: 'Fair skin. Burns easily, tans minimally. Very high sun sensitivity.',
  },
  {
    type: 'Type III',
    description: 'Light to medium skin. Burns moderately, tans gradually. Moderate sun sensitivity.',
  },
  {
    type: 'Type IV',
    description: 'Olive or light brown skin. Burns minimally, tans easily. Lower sun sensitivity.',
  },
  {
    type: 'Type V',
    description: 'Brown skin. Rarely burns, tans deeply. Low sun sensitivity.',
  },
  {
    type: 'Type VI',
    description: 'Dark brown to black skin. Very rarely burns. Lowest sun sensitivity; still needs protection.',
  },
]
</script>

<template>
  <section class="skin-types">
    <h2 class="skin-types__title">Skin Types</h2>
    <p class="skin-types__intro">
      The Fitzpatrick scale describes how skin responds to UV exposure. This is for information only.
    </p>
    <div class="skin-types__grid">
      <article
        v-for="item in skinTypes"
        :key="item.type"
        class="skin-types__card"
      >
        <h3 class="skin-types__card-title">{{ item.type }}</h3>
        <p class="skin-types__card-desc">{{ item.description }}</p>
      </article>
    </div>
  </section>
</template>

<style scoped>
.skin-types {
  margin-bottom: 0;
  padding: 1.5rem 1.75rem;
  background: #fff;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
}
.skin-types__title {
  margin: 0 0 0.5rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: #0369a1;
  letter-spacing: -0.02em;
}
.skin-types__intro {
  margin: 0 0 1.25rem;
  font-size: 0.9375rem;
  color: #64748b;
  line-height: 1.55;
}
.skin-types__grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}
.skin-types__card {
  background: #f8fafc;
  border-radius: 14px;
  padding: 1.25rem 1.5rem;
  border: 1px solid #e2e8f0;
}
.skin-types__card-title {
  margin: 0 0 0.5rem;
  font-size: 1rem;
  font-weight: 700;
  color: #334155;
}
.skin-types__card-desc {
  margin: 0;
  font-size: 0.875rem;
  color: #475569;
  line-height: 1.5;
}

@media (min-width: 600px) {
  .skin-types__grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (min-width: 1000px) {
  .skin-types__grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 1.25rem;
  }
  .skin-types__card {
    padding: 1.35rem 1.5rem;
  }
}
</style>
