-- Core schema for UVibe PostgreSQL database.
--
-- This file defines the minimum tables needed for:
-- - Epic 1: Track UV Levels
-- - Epic 2: Raising Awareness
--
-- It also includes optional tables that can be used in future epics.

-- Location master data: Australian postcodes and coordinates.
CREATE TABLE IF NOT EXISTS location (
    id SERIAL PRIMARY KEY,
    postcode VARCHAR(10) NOT NULL,
    suburb   VARCHAR(255) NOT NULL,
    state    VARCHAR(16)  NOT NULL,
    latitude  DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,

    CONSTRAINT uq_location_postcode_suburb_state
        UNIQUE (postcode, suburb, state)
);

CREATE INDEX IF NOT EXISTS idx_location_suburb
    ON location (LOWER(suburb));

CREATE INDEX IF NOT EXISTS idx_location_postcode
    ON location (postcode);


-- UV risk levels table: maps a UV range to a textual risk level,
-- colour token, and a human-readable message.
CREATE TABLE IF NOT EXISTS uv_risk_level (
    id SERIAL PRIMARY KEY,
    min_uv DOUBLE PRECISION NOT NULL,
    max_uv DOUBLE PRECISION NOT NULL,
    risk_level VARCHAR(64) NOT NULL,
    message    TEXT NOT NULL,
    color      VARCHAR(32) NOT NULL,

    CONSTRAINT uq_uv_risk_range UNIQUE (min_uv, max_uv)
);


-- Optional awareness / statistics tables for Epic 2 and future work.
CREATE TABLE IF NOT EXISTS cancer_statistics (
    id SERIAL PRIMARY KEY,
    region VARCHAR(255) NOT NULL,
    year   INTEGER NOT NULL,
    cases  INTEGER NOT NULL,
    CONSTRAINT uq_cancer_region_year UNIQUE (region, year)
);

CREATE TABLE IF NOT EXISTS sun_protection_behaviour (
    id SERIAL PRIMARY KEY,
    region VARCHAR(255) NOT NULL,
    year   INTEGER NOT NULL,
    behaviour_metric VARCHAR(255) NOT NULL,
    value  DOUBLE PRECISION NOT NULL,
    CONSTRAINT uq_behaviour_region_year_metric
        UNIQUE (region, year, behaviour_metric)
);
