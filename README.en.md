# Bank Customer Churn — SQL & Python Analysis

Analysis of customer churn at a retail bank based on 10,000 customer records.
Goal: identify the segments where customers are most likely to leave — and turn that into a concrete, actionable recommendation.

**Key result:** A clearly defined high-risk segment (German, inactive customers over 40) churns at **62.2%** — more than three times the overall average of ~20%.

---

## Dataset

- **Source:** [Churn Modelling (Kaggle)](https://www.kaggle.com/datasets/shrutimechlearn/churn-modelling)
- **Size:** 10,000 customers, 14 features
- **Target variable:** `Exited` (1 = customer left, 0 = stayed)
- **Key features:** country (`Geography`), age (`Age`), number of bank products (`NumOfProducts`), account balance (`Balance`), activity status (`IsActiveMember`), gender (`Gender`)

## Approach & Tools

| Step | Tool |
|---|---|
| Loaded raw data (CSV) into a database | SQLite (DB Browser for SQLite) |
| Data analysis & business questions | SQL |
| Evaluation & visualization | Python · pandas · matplotlib |

Workflow: CSV → SQLite table → 8 analytical questions answered in SQL → results loaded into Python and visualized as charts.

---

## Findings

### 1. Overall churn
Of 10,000 customers, **2,037 left → 20.4%**. This is the baseline against which every segment is compared.

### 2. Churn by country

![Churn by country](churn_pro_land.png)

| Country | Customers | Churned | Churn rate |
|---|---|---|---|
| France | 5,014 | 810 | 16.2% |
| **Germany** | 2,509 | 814 | **32.4%** |
| Spain | 2,477 | 413 | 16.7% |

**Germany is the problem market: double the churn rate of France and Spain.** Notably, Germany has almost the same *absolute* number of churners as France (814 vs. 810) — but from only half the customer base. Without looking at the rate (instead of the absolute number), this effect would stay invisible.

### 3. Churn by age

![Churn by age group](churn_pro_alter.png)

| Age group | Customers | Churned | Churn rate |
|---|---|---|---|
| under 40 | 5,987 | 597 | 10.0% |
| **40 and older** | 4,013 | 1,440 | **35.9%** |

Older customers churn **3.6x more often** than younger ones. Again, the absolute figures (1,440 vs. 597) understate the gap — only the rate reveals the full extent.

### 4. Churn by number of bank products

![Churn by number of products](churn_pro_produkt.png)

| Products | Customers | Churned | Churn rate |
|---|---|---|---|
| 1 | 5,084 | 1,409 | 27.7% |
| 2 | 4,590 | 348 | **7.6%** (most loyal) |
| 3 | 266 | 220 | 82.7% |
| 4 | 60 | 60 | 100.0% |

**The relationship is not linear.** Two products is the sweet spot with the lowest churn rate. Customers with 3–4 products, however, leave almost entirely. This points to a product or advisory problem (possible causes: overselling, unsuitable product bundles).
> ⚠️ *Methodological note:* The 3- and 4-product groups are small (266 and 60 customers). The rates are a strong signal but statistically less robust than the large groups — this would warrant deeper investigation.

### 5. Additional drivers
- **Gender:** Women 25.1% vs. men 16.5% — women churn ~1.5x more often.
- **Account balance:** Higher balance correlates with *higher* churn (no balance 13.8% → up to 100k 20.6% → over 100k 25.2%). This effect likely overlaps with the Germany effect (German customers typically hold high balances) and would need to be isolated.

### 6. High-risk segment (combining the drivers)
Combining the strongest risk factors — **German customers, over 40, inactive** — yields:

| Segment | Customers | Churned | Churn rate |
|---|---|---|---|
| Germany · 40+ · inactive | 596 | 371 | **62.2%** |

Nearly two out of three customers in this segment leave — three times the average, at a robust group size of 596 customers.

---

## Recommendation

1. **Focus retention efforts on the high-risk segment.** The 596 German, inactive customers over 40 offer the greatest leverage: addressing them targets the highest churn concentration instead of spreading resources thin.
2. **Investigate 3/4-product customers before the problem scales.** Churn rates of 80–100% are a red flag — a root-cause analysis (sales process, fees, advisory) should be a priority.
3. **Re-activation campaigns for inactive members**, since inactivity is a core component of the high-risk segment.
4. **Analyze the German market more deeply** to understand the cause of the doubled churn.

---

## Analytical principles applied
- **Rates over absolute numbers:** Because the comparison groups differ in size, churn *rates* are compared, not absolute churn counts. Absolute numbers otherwise lead to false conclusions (see the Germany and age findings).
- **Group sizes considered:** Small segments (e.g. 4 products, n=60) are treated as a signal, not a confirmed conclusion.
- **Overlapping effects named** (e.g. balance × country) instead of jumping to causal claims.

## How to run

```bash
# Create environment and install packages
python -m venv churn_env
churn_env\Scripts\python.exe -m pip install pandas matplotlib

# Run the analysis script (generates the PNG charts)
churn_env\Scripts\python.exe churn.py
```

Prerequisite: `churn.db` (imported into SQLite from `Churn_Modelling.csv`) at the given path.

## Files in this project
- `churn.py` — analysis and visualization script (SQL queries + matplotlib charts)
- `churn_pro_land.png`, `churn_pro_alter.png`, `churn_pro_produkt.png` — generated charts
- `README.md` — German version · `README.en.md` — this document

## Roadmap
- **JOIN extension:** add a country → region reference table to demonstrate multi-table joins.
- **GenAI layer:** automatically summarize the findings into an executive summary via an LLM API.
- **ML model:** churn prediction (scikit-learn) based on the identified drivers.

---

*Analysis project to build practical SQL and Python skills in the data analytics domain.*
