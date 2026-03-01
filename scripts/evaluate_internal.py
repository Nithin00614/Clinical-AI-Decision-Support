import pandas as pd
import joblib
from sklearn.metrics import (
    roc_auc_score,
    f1_score,
    accuracy_score,
    confusion_matrix,
    brier_score_loss
)

# Load primary dataset
df = pd.read_csv("data/processed_uci.csv")

# Separate features & target
X = df.drop("Class", axis=1)
y = df["Class"]

# Load trained pipeline
pipeline = joblib.load("models/full_pipeline.pkl")

# Predict
y_prob = pipeline.predict_proba(X)[:, 1]
y_pred = pipeline.predict(X)

# Metrics
auc = roc_auc_score(y, y_prob)
f1 = f1_score(y, y_pred)
acc = accuracy_score(y, y_pred)
brier = brier_score_loss(y, y_prob)

tn, fp, fn, tp = confusion_matrix(y, y_pred).ravel()

sensitivity = tp / (tp + fn)
specificity = tn / (tn + fp)

print("AUC:", auc)
print("F1:", f1)
print("Accuracy:", acc)
print("Sensitivity:", sensitivity)
print("Specificity:", specificity)
print("Brier Score:", brier)