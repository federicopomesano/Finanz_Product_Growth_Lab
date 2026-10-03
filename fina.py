import datetime
import random
import sqlite3
import numpy as np
import pandas as pd

# Impostiamo il seed per la riproducibilità
np.random.seed(42)
random.seed(42)

NUM_USERS = 5000
START_DATE = datetime.datetime(2026, 1, 1)
END_DATE = datetime.datetime(2026, 3, 31)

# 1. TABELLA USERS
channels = ["TikTok Ads", "Instagram Ads", "Organic Search", "Referral"]
age_groups = ["18-24", "25-34", "35-44", "45+"]
platforms = ["iOS", "Android"]

user_list = []
for uid in range(1, NUM_USERS + 1):
    signup_dt = START_DATE + datetime.timedelta(
        seconds=random.randint(0, int((END_DATE - START_DATE).total_seconds()))
    )
    chan = np.random.choice(channels, p=[0.4, 0.3, 0.2, 0.1])
    age = np.random.choice(age_groups, p=[0.5, 0.35, 0.1, 0.05])
    plat = np.random.choice(platforms, p=[0.6, 0.4])

    user_list.append(
        {
            "user_id": uid,
            "signup_timestamp": signup_dt,
            "acquisition_channel": chan,
            "age_group": age,
            "platform": plat,
        }
    )

df_users = pd.DataFrame(user_list)

# 2. TABELLA EVENTS (Simulazione comportamento reale con Drop-off)
events_list = []
event_id = 1

for idx, user in df_users.iterrows():
    uid = user["user_id"]
    curr_time = user["signup_timestamp"]

    # Evento: app_open
    events_list.append(
        {
            "event_id": event_id,
            "user_id": uid,
            "event_name": "app_open",
            "timestamp": curr_time,
            "lesson_id": None,
        }
    )
    event_id += 1

    # Evento: signup_completed (90% converte)
    if random.random() < 0.90:
        curr_time += datetime.timedelta(seconds=random.randint(30, 120))
        events_list.append(
            {
                "event_id": event_id,
                "user_id": uid,
                "event_name": "signup_completed",
                "timestamp": curr_time,
                "lesson_id": None,
            }
        )
        event_id += 1

        # Evento: onboarding_completed (75% converte)
        if random.random() < 0.75:
            curr_time += datetime.timedelta(seconds=random.randint(60, 300))
            events_list.append(
                {
                    "event_id": event_id,
                    "user_id": uid,
                    "event_name": "onboarding_completed",
                    "timestamp": curr_time,
                    "lesson_id": None,
                }
            )
            event_id += 1

            # Evento: first_lesson_start (60% converte -> Punto critico / Friction)
            if random.random() < 0.60:
                curr_time += datetime.timedelta(
                    seconds=random.randint(10, 120)
                )
                events_list.append(
                    {
                        "event_id": event_id,
                        "user_id": uid,
                        "event_name": "lesson_start",
                        "timestamp": curr_time,
                        "lesson_id": 101,
                    }
                )
                event_id += 1

                # Evento: first_quiz_completed (ACTIVATION - 70% converte)
                if random.random() < 0.70:
                    curr_time += datetime.timedelta(
                        seconds=random.randint(180, 480)
                    )
                    events_list.append(
                        {
                            "event_id": event_id,
                            "user_id": uid,
                            "event_name": "quiz_completed",
                            "timestamp": curr_time,
                            "lesson_id": 101,
                        }
                    )
                    event_id += 1

                    # RETENTION SIMULATION (D1, D3, D7 activity)
                    # Utenti attivati hanno probabilità più alta di tornare
                    for day_offset in [1, 2, 3, 5, 7, 14, 30]:
                        if random.random() < (0.6 / (day_offset**0.5)):
                            retention_time = curr_time + datetime.timedelta(
                                days=day_offset,
                                hours=random.randint(-2, 2),
                            )
                            if retention_time <= END_DATE + datetime.timedelta(
                                days=30
                            ):
                                events_list.append(
                                    {
                                        "event_id": event_id,
                                        "user_id": uid,
                                        "event_name": "streak_extended",
                                        "timestamp": retention_time,
                                        "lesson_id": 101 + day_offset,
                                    }
                                )
                                event_id += 1

df_events = pd.DataFrame(events_list)

# 3. SALVATAGGIO IN DATABASE SQLITE & CSV
conn = sqlite3.connect("finanz_growth_lab.db")
df_users.to_sql("users", conn, if_exists="replace", index=False)
df_events.to_sql("events", conn, if_exists="replace", index=False)

df_users.to_csv("users.csv", index=False)
df_events.to_csv("events.csv", index=False)

print(
    f"Dataset generato con successo! {len(df_users)} utenti e {len(df_events)} eventi registrati."
)
