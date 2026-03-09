import requests
import psycopg2
import time

# Connect to your database
conn = psycopg2.connect(
    dbname="f1",
    user="postgres",
    password="f1pass",
    host="localhost"
)
cur = conn.cursor()

# 1. Create tables with Foreign Keys and Unique Constraints
# Drivers table is independent
cur.execute("""
CREATE TABLE IF NOT EXISTS drivers (
    driver_id VARCHAR(50) PRIMARY KEY,
    code VARCHAR(5),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    nationality VARCHAR(50),
    date_of_birth DATE
)
""")

# Races table is independent
cur.execute("""
CREATE TABLE IF NOT EXISTS races (
    race_id SERIAL PRIMARY KEY,
    season INT,
    round INT,
    session_type VARCHAR(20),
    race_name VARCHAR(100),
    circuit_name VARCHAR(100),
    country VARCHAR(50),
    date DATE,
    UNIQUE(season, round, session_type) -- Prevents duplicate race sessions
)
""")

# Results table links to both Races and Drivers
cur.execute("""
CREATE TABLE IF NOT EXISTS results (
    result_id SERIAL PRIMARY KEY,
    race_id INT REFERENCES races(race_id),       -- Foreign Key to races
    driver_id VARCHAR(50) REFERENCES drivers(driver_id), -- Foreign Key to drivers
    constructor VARCHAR(50),
    grid INT,
    position INT,
    points FLOAT,
    status VARCHAR(50),
    UNIQUE(race_id, driver_id)                   -- Prevents duplicate results per driver per race
)
""")
conn.commit()

# Helper function for robust API calls
def fetch_data(url, max_retries=5):
    for i in range(max_retries):
        r = requests.get(url)
        if r.status_code == 200 and r.text.strip():
            return r.json()
        elif r.status_code == 429:
            time.sleep(2 ** i) # Exponential backoff if rate limited
        else:
            time.sleep(2)
    print(f"Failed to fetch {url} after {max_retries} retries.")
    return None

# 2. Load drivers (Upsert logic)
print("Loading drivers...")
for offset in range(0, 2000, 100):
    url = f"https://api.jolpi.ca/ergast/f1/drivers/?limit=100&offset={offset}"
    data = fetch_data(url)
    
    if not data or not data['MRData']['DriverTable']['Drivers']:
        break
        
    for d in data['MRData']['DriverTable']['Drivers']:
        cur.execute("""
            INSERT INTO drivers (driver_id, code, first_name, last_name, nationality, date_of_birth)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (driver_id) DO UPDATE SET
                code = EXCLUDED.code,
                first_name = EXCLUDED.first_name,
                last_name = EXCLUDED.last_name,
                nationality = EXCLUDED.nationality
        """, (
            d.get('driverId'),
            d.get('code'),
            d.get('givenName'),
            d.get('familyName'),
            d.get('nationality'),
            d.get('dateOfBirth')
        ))
    conn.commit()
    time.sleep(0.5)

print("Drivers loaded.")

# 3. Load seasons 2000-2027 (Both Races and Sprints)
endpoints = [('results', 'Race'), ('sprint', 'Sprint')]

for season in range(2000, 2027):
    print(f"Loading season {season}...")
    
    for endpoint, session_type in endpoints:
        offset = 0
        while True:
            url = f"https://api.jolpi.ca/ergast/f1/{season}/{endpoint}/?limit=100&offset={offset}"
            data = fetch_data(url)
            
            if not data or not data['MRData']['RaceTable']['Races']:
                break 
                
            for race in data['MRData']['RaceTable']['Races']:
                # UPSERT for Races: Inserts or updates, and always returns the race_id
                cur.execute("""
                    INSERT INTO races (season, round, session_type, race_name, circuit_name, country, date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (season, round, session_type) DO UPDATE SET
                        race_name = EXCLUDED.race_name,
                        circuit_name = EXCLUDED.circuit_name,
                        date = EXCLUDED.date
                    RETURNING race_id
                """, (
                    season,
                    int(race.get('round', 0)),
                    session_type,
                    race.get('raceName'),
                    race.get('Circuit', {}).get('circuitName'),
                    race.get('Circuit', {}).get('Location', {}).get('country'),
                    race.get('date')
                ))
                race_id = cur.fetchone()[0]
                
                results_key = 'SprintResults' if session_type == 'Sprint' else 'Results'
                
                for result in race.get(results_key, []):
                    # UPSERT for Results: Updates points/positions if penalties are applied later
                    cur.execute("""
                        INSERT INTO results (race_id, driver_id, constructor, grid, position, points, status)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (race_id, driver_id) DO UPDATE SET
                            constructor = EXCLUDED.constructor,
                            grid = EXCLUDED.grid,
                            position = EXCLUDED.position,
                            points = EXCLUDED.points,
                            status = EXCLUDED.status
                    """, (
                        race_id,
                        result.get('Driver', {}).get('driverId'),
                        result.get('Constructor', {}).get('name'),
                        int(result.get('grid', 0)),
                        int(result['position']) if result.get('position', '').isdigit() else None,
                        float(result.get('points', 0)),
                        result.get('status')
                    ))
                conn.commit()
                
            total_records = int(data['MRData']['total'])
            offset += 100
            if offset >= total_records:
                break
            
            time.sleep(0.5)

print("Ingestion complete. Database is up to date!")
cur.close()
conn.close()