WITH funnel_stages AS (
    SELECT
        COUNT(DISTINCT CASE WHEN event_name = 'app_open' THEN user_id END) AS step_1_app_open,
        COUNT(DISTINCT CASE WHEN event_name = 'signup_completed' THEN user_id END) AS step_2_signup,
        COUNT(DISTINCT CASE WHEN event_name = 'onboarding_completed' THEN user_id END) AS step_3_onboarding,
        COUNT(DISTINCT CASE WHEN event_name = 'lesson_start' THEN user_id END) AS step_4_first_lesson,
        COUNT(DISTINCT CASE WHEN event_name = 'quiz_completed' THEN user_id END) AS step_5_activated
    FROM events
)
SELECT
    step_1_app_open AS users_app_open,
    step_2_signup AS users_signup,
    ROUND(100.0 * step_2_signup / step_1_app_open, 2) || '%' AS conv_signup,

    step_3_onboarding AS users_onboarding,
    ROUND(100.0 * step_3_onboarding / step_2_signup, 2) || '%' AS conv_onboarding,

    step_4_first_lesson AS users_first_lesson,
    ROUND(100.0 * step_4_first_lesson / step_3_onboarding, 2) || '%' AS conv_first_lesson,

    step_5_activated AS users_activated,
    ROUND(100.0 * step_5_activated / step_4_first_lesson, 2) || '%' AS conv_activation
FROM funnel_stages;
