-- PostgreSQL schema for NYC Taxi trips
DROP TABLE IF EXISTS trips;
CREATE TABLE trips (
  id SERIAL PRIMARY KEY,
  pickup_datetime TIMESTAMP NOT NULL,
  dropoff_datetime TIMESTAMP NOT NULL,
  pickup_lat DOUBLE PRECISION,
  pickup_lon DOUBLE PRECISION,
  dropoff_lat DOUBLE PRECISION,
  dropoff_lon DOUBLE PRECISION,
  trip_distance_km DOUBLE PRECISION CHECK (trip_distance_km >= 0),
  trip_duration_sec INTEGER CHECK (trip_duration_sec > 0),
  fare_amount NUMERIC(10,2) CHECK (fare_amount >= 0),
  tip_amount NUMERIC(10,2) CHECK (tip_amount >= 0),
  passenger_count SMALLINT CHECK (passenger_count >= 0),
  payment_type VARCHAR(64),
  avg_speed_kmh DOUBLE PRECISION CHECK (avg_speed_kmh >= 0),
  fare_per_km NUMERIC(10,3),
  pickup_hour SMALLINT CHECK (pickup_hour BETWEEN 0 AND 23),
  weekday SMALLINT CHECK (weekday BETWEEN 0 AND 6),
  is_weekend BOOLEAN,
  haversine_km DOUBLE PRECISION,
  created_at TIMESTAMP DEFAULT now()
);

CREATE INDEX idx_trips_pickup_time ON trips (pickup_datetime);
CREATE INDEX idx_trips_dropoff_time ON trips (dropoff_datetime);
CREATE INDEX idx_trips_pickup_loc ON trips (pickup_lat, pickup_lon);
CREATE INDEX idx_trips_dropoff_loc ON trips (dropoff_lat, dropoff_lon);
CREATE INDEX idx_trips_speed ON trips (avg_speed_kmh);
CREATE INDEX idx_trips_fare ON trips (fare_amount);
