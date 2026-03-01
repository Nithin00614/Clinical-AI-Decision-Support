
# Data Preprocessing Documentation

## Raw Dataset Characteristics

- Mixed numerical and categorical features
- Missing values represented as '?'
- Some categorical columns:
  - Rbc
  - Htn

---

## Cleaning Steps

1. Replaced '?' with NaN
2. Converted numeric columns using coercion
3. Encoded categorical fields:
   - Rbc → normal=1, abnormal=0
   - Htn → yes=1, no=0
4. Removed irrelevant columns
5. Selected 14 stable clinical predictors

---

## Feature Selection Rationale

Selected based on:
- Clinical relevance
- Statistical separability
- Low redundancy
- Practical availability in EHR systems

---

## Scaling

- StandardScaler applied inside pipeline
- Ensures numeric stability for logistic regression

---

## Final Schema

Final production schema:

[Bp, Sg, Al, Su, Rbc, Bu, Sc, Sod, Pot, Hemo, Wbcc, Rbcc, Htn]

Target: Class