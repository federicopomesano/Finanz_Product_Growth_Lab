import numpy as np
import pandas as pd
from scipy import stats

# Set seed per riproducibilità
np.random.seed(42)

# SIMULAZIONE A/B TEST
# Sample size: 1000 utenti per gruppo
n_control = 1000
n_treatment = 1000

# Conversion Rate (First Lesson Completion)
# Controllo: ~60% (coerente con i nostri dati SQL)
# Treatment: Ipotizziamo un miglioramento grazie al micro-learning
p_control = 0.601
p_treatment = 0.675

# Generazione dati binari (1 = completato, 0 = abbandonato)
control_results = np.random.binomial(1, p_control, n_control)
treatment_results = np.random.binomial(1, p_treatment, n_treatment)

# CALCOLI STATISTICI
conv_control = control_results.mean()
conv_treatment = treatment_results.mean()
uplift = (conv_treatment - conv_control) / conv_control

# Z-Test per proporzioni
successes = [control_results.sum(), treatment_results.sum()]
samples = [n_control, n_treatment]

# Standard error & Z-score
p_pooled = (
    control_results.sum() + treatment_results.sum()
) / (n_control + n_treatment)
se = np.sqrt(p_pooled * (1 - p_pooled) * (1 / n_control + 1 / n_treatment))
z_score = (conv_treatment - conv_control) / se
p_value = 1 - stats.norm.cdf(z_score)

# Intervallo di confidenza al 95% per la differenza
diff = conv_treatment - conv_control
ci_lower = diff - 1.96 * se
ci_upper = diff + 1.96 * se

# DATAFRAME DI SINTESI
ab_summary = pd.DataFrame(
    {
        "Metric": [
            "Sample Size",
            "Conversions",
            "Conversion Rate",
            "Absolute Lift",
            "Relative Uplift",
            "P-Value",
            "Statistically Significant (p < 0.05)",
        ],
        "Control (8 min)": [
            n_control,
            control_results.sum(),
            f"{conv_control:.2%}",
            "-",
            "-",
            "-",
            "-",
        ],
        "Treatment (3 min)": [
            n_treatment,
            treatment_results.sum(),
            f"{conv_treatment:.2%}",
            f"{diff:+.2%}",
            f"{uplift:+.2%}",
            f"{p_value:.4f}",
            "YES" if p_value < 0.05 else "NO",
        ],
    }
)

# Salva i risultati nel file CSV
ab_summary.to_csv("ab_test_results.csv", index=False)

# Stampe finali a schermo
print("=== A/B TEST RESULTS SUMMARY ===")
print(ab_summary.to_string(index=False))
