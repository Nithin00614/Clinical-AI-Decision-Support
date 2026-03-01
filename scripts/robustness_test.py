import pandas as pd
import joblib
import numpy as np
from sklearn.metrics import roc_auc_score

# Load data
df = pd.read_csv("data/primary_training.csv")
X = df.drop("Class", axis=1)
y = df["Class"]

pipeline = joblib.load("models/full_pipeline.pkl")

# Original AUC
original_prob = pipeline.predict_proba(X)[:,1]
original_auc = roc_auc_score(y, original_prob)

# Add Gaussian noise
noise = np.random.normal(0, 0.05, X.shape)
X_noisy = X + noise

noisy_prob = pipeline.predict_proba(X_noisy)[:,1]
noisy_auc = roc_auc_score(y, noisy_prob)

print("Original AUC:", original_auc)
print("Noisy AUC:", noisy_auc)
print("AUC Drop:", original_auc - noisy_auc)