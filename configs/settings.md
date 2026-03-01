# Configuration Documentation

This file describes tunable parameters for the CKD AI system.

## Model
Defines active model artifact path and version.

## Confidence Weights
Controls contribution of:
- Base model certainty
- SHAP explainability signal
- Retrieval evidence signal

## Decision Modes
- SAFE: Low confidence
- NORMAL: Moderate confidence
- VERBOSE: High confidence

These thresholds can be tuned without retraining the model.