CREATE TABLE IF NOT EXISTS equipment_log(
    name TEXT,
    date DATE PRIMARY KEY,
    time TIME,
    equipment TEXT,
    signature TEXT
)
