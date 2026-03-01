# Data Shift & Model Drift Considerations

## What is Data Shift?

Data shift occurs when real-world input distribution differs from training distribution.

This model demonstrated sensitivity to perturbation during robustness testing.

---

## Observed Sensitivity

Gaussian noise injection resulted in:

- AUC drop: 0.3364

Indicating reliance on dominant predictors.

---

## Production Risk

Potential real-world risks include:

- Lab measurement variability
- Population demographic differences
- Missing feature distributions

---

## Mitigation Implemented

- Confidence thresholding
- Decision mode controller (SAFE / NORMAL / VERBOSE)
- Human-in-the-loop override

---

## Future Improvements

- PSI-based drift detection
- Continuous calibration tracking
- Shadow deployment monitoring

