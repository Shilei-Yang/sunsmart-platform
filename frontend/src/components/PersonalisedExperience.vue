<!--
  Personalised Experience — Epic 3 UI placeholder.
  Customise UV alerts: skin type, activity goals, alert frequency, preferences, method.
  No backend logic yet.
-->
<script setup>
const skinTypes = ['Type I', 'Type II', 'Type III', 'Type IV', 'Type V', 'Type VI']

const activityGoals = [
  'Short Activity: Up to 3 hour',
  'Moderate Activity: 4 to 8 hours',
  'Extended Activity: More than 9 hours',
]

const alertFrequencyOptions = [
  'Immediate Alerts',
  'Hourly Updates',
  'Daily Summaries',
]

const alertPreferencesOptions = [
  'General UV Alerts',
  'Sunscreen Application and Dosage Reminders',
  'Shade Seeking Alerts',
  'Sun-smart Clothing',
]

const alertMethodOptions = [
  'SMS Notifications',
  'Email Notifications',
]
</script>

<template>
  <section class="personalised">
    <!-- Single large white card -->
    <div class="personalised__card uv-card">
      <h2 class="personalised__title">Customise Your UV Alerts</h2>

      <!-- 1. Select Your Skin Type -->
      <div class="personalised__section">
        <h3 class="personalised__section-title">Select Your Skin Type</h3>
        <p class="personalised__section-desc">Choose your skin type from the following options</p>
        <div class="personalised__pills">
          <span
            v-for="type in skinTypes"
            :key="type"
            class="personalised__pill"
          >
            {{ type }}
          </span>
        </div>
      </div>

      <!-- 2. Set Activity Goals -->
      <div class="personalised__section">
        <h3 class="personalised__section-title">Set Activity Goals</h3>
        <p class="personalised__section-desc">Specify your outdoor activity duration</p>
        <div class="personalised__pills">
          <span
            v-for="goal in activityGoals"
            :key="goal"
            class="personalised__pill"
          >
            {{ goal }}
          </span>
        </div>
      </div>

      <!-- 3. Alert Frequency -->
      <div class="personalised__section">
        <h3 class="personalised__section-title">Alert Frequency</h3>
        <p class="personalised__section-desc">Select how often you want to receive alerts</p>
        <div class="personalised__pills">
          <span
            v-for="freq in alertFrequencyOptions"
            :key="freq"
            class="personalised__pill"
          >
            {{ freq }}
          </span>
        </div>
      </div>

      <!-- 4. Alert Preferences -->
      <div class="personalised__section">
        <h3 class="personalised__section-title">Alert Preferences</h3>
        <p class="personalised__section-desc">Specify the types of alerts you want to receive</p>
        <div class="personalised__pills">
          <span
            v-for="pref in alertPreferencesOptions"
            :key="pref"
            class="personalised__pill"
          >
            {{ pref }}
          </span>
        </div>
      </div>

      <!-- 5. Alert Method -->
      <div class="personalised__section">
        <h3 class="personalised__section-title">Alert Method</h3>
        <p class="personalised__section-desc">Specify how you want to receive the alerts</p>
        <div class="personalised__pills">
          <span
            v-for="method in alertMethodOptions"
            :key="method"
            class="personalised__pill"
          >
            {{ method }}
          </span>
        </div>
      </div>

      <!-- 6. Input Field -->
      <div class="personalised__section">
        <div class="personalised__input-wrap">
          <span class="personalised__input-icon" aria-hidden="true">✎</span>
          <input
            type="text"
            class="personalised__input"
            placeholder="Enter Your Details Here"
            aria-label="Enter your details"
          />
        </div>
      </div>

      <!-- 7. Buttons (aligned right) -->
      <div class="personalised__actions">
        <button type="button" class="personalised__btn personalised__btn--outline">
          Clear
        </button>
        <button type="button" class="personalised__btn personalised__btn--primary">
          Send Alerts
        </button>
      </div>
    </div>
  </section>
</template>

<style scoped>
.personalised {
  margin-bottom: 0;
}

.personalised__title {
  margin: 0 0 1.75rem;
  font-size: 1.375rem;
  font-weight: 700;
  color: var(--uv-primary, #D8613C);
  letter-spacing: -0.02em;
}

.personalised__section {
  margin-bottom: 1.75rem;
}
.personalised__section:last-of-type {
  margin-bottom: 0;
}

.personalised__section-title {
  margin: 0 0 0.35rem;
  font-size: 1.0625rem;
  font-weight: 700;
  color: var(--uv-text, #4A4A4A);
}
.personalised__section-desc {
  margin: 0 0 0.85rem;
  font-size: 0.9375rem;
  color: var(--uv-text-muted, #8A8A8A);
  line-height: 1.5;
}

/* Pill buttons */
.personalised__pills {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.personalised__pill {
  display: inline-block;
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--uv-text, #4A4A4A);
  background: var(--uv-card, #fff);
  border: 1px solid var(--uv-grid, #E6E1DA);
  border-radius: 999px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
}

/* Input with icon */
.personalised__input-wrap {
  position: relative;
  display: flex;
  align-items: center;
}
.personalised__input-icon {
  position: absolute;
  left: 1rem;
  font-size: 1rem;
  color: var(--uv-text-muted, #8A8A8A);
  pointer-events: none;
}
.personalised__input {
  width: 100%;
  padding: 0.9rem 1.25rem 0.9rem 2.75rem;
  font-size: 0.9375rem;
  color: var(--uv-text, #4A4A4A);
  background: var(--uv-card, #fff);
  border: 1px solid var(--uv-grid, #E6E1DA);
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
}
.personalised__input::placeholder {
  color: var(--uv-text-muted, #8A8A8A);
}

/* Buttons aligned right */
.personalised__actions {
  margin-top: 1.75rem;
  padding-top: 0.25rem;
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}
.personalised__btn {
  padding: 0.65rem 1.5rem;
  font-size: 0.9375rem;
  font-weight: 600;
  border-radius: 10px;
  cursor: pointer;
  transition: opacity 0.2s;
}
.personalised__btn:hover {
  opacity: 0.9;
}
.personalised__btn--primary {
  background: var(--uv-primary, #D8613C);
  color: #fff;
  border: none;
}
.personalised__btn--outline {
  background: transparent;
  color: var(--uv-text, #4A4A4A);
  border: 2px solid var(--uv-grid, #E6E1DA);
}
</style>
