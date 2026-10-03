WITH user_activation AS (
    SELECT
        user_id,
        MIN(DATE(timestamp)) AS activation_date
    FROM events
    WHERE event_name = 'quiz_completed'
    GROUP BY user_id
),
retention_events AS (
    SELECT
        e.user_id,
        a.activation_date,
        CAST((JULIANDAY(DATE(e.timestamp)) - JULIANDAY(a.activation_date)) AS INT) AS day_difference
    FROM events e
    JOIN user_activation a ON e.user_id = a.user_id
    WHERE e.event_name = 'streak_extended'
)
SELECT
    -- Selezioniamo la settimana (es. 2026-W01, 2026-W02...)
    strftime('%Y-W%W', a.activation_date) AS activation_week,
    COUNT(DISTINCT a.user_id) AS total_activated_users,

    COUNT(DISTINCT CASE WHEN r.day_difference = 1 THEN r.user_id END) AS d1_retained,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN r.day_difference = 1 THEN r.user_id END) / COUNT(DISTINCT a.user_id), 2) || '%' AS d1_retention_rate,

    COUNT(DISTINCT CASE WHEN r.day_difference = 7 THEN r.user_id END) AS d7_retained,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN r.day_difference = 7 THEN r.user_id END) / COUNT(DISTINCT a.user_id), 2) || '%' AS d7_retention_rate
FROM user_activation a
LEFT JOIN retention_events r ON a.user_id = r.user_id
GROUP BY activation_week
ORDER BY activation_week ASC;
