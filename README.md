# Finanz_Product_Growth_Lab

Case study di Product & Growth Analytics simulato sul prodotto B2C di **Finanz**. Il progetto copre l'intero ciclo di vita del dato: dalla modellizzazione sintetica all'estrazione SQL, fino al testing statistico di ipotesi di prodotto.

---

## Executive Summary
Attraverso l'analisi del funnel di acquisizione e attivazione, è stato identificato un punto di drop-off significativo nella fase di First Lesson. È stato strutturato ed eseguito un **A/B Test** per valutare l'impatto di una prima sessione di apprendimento ridotta (da 8 a 3 minuti).

### Risultati Chiave:
* Attivazione Totale (Baseline): 28,78% sul totale delle aperture app (da 5.000 a 1.439 utenti attivati).
* Retention Baseline: D1 Retention media del **58,14%**; D7 Retention media del **23,88%**.
* A/B Test Outcome: La variazione (3 min) ha portato il tasso di conversione dal 61,40% al **65,90%** (+4,50% Absolute Lift / +7,33% Relative Uplift).
* Significatività Statistica: Test a due code confermato con **p-value = 0,0363** (< 0,05).

---

## Tecnologie e Strumenti
* Python: Generazione dati comportamentali e calcolo significatività statistica (p-value).
* SQL: Modellizzazione ed estrazione metriche di Funnel e Cohort Retention (D1/D7).
* PowerPoint: visualizzazione dati executive e presentazione strategica.

---

## Struttura del Repository
* 'fina.py`: Script Python per la generazione del dataset sintetico, tracking plan dei dati
* 'abtest.py': Script Python per il calcolo statistico dell'A/B test
* 'users.csv` / 'events.csv': Tabella anagrafica utenti e registro eventi granulari per le analisi comportamentali.
* '01_funnel_analysis.sql' / '02_retention_results.sql': Query SQL per l'estrazione e il calcolo delle conversioni nei funnel e delle retention settimana per settimana.
* 'Funnel_Results.xlsx' / 'Retention_Results.xlsx': Tabelle dati estratte direttamente tramite SQL.
* 'ab_test_results.csv': Dataset con i risultati grezzi della sperimentazione A/B.
* 'Finanz_Product_Growth_Blueprint.pptx': Presentazione in Powerpoint dei risultati evidenziati dall'esperimento e conclusioni
