import pandas as pd
import joblib
from sklearn.metrics import roc_auc_score, f1_score, accuracy_score

# ----------------------------
# Load trained pipeline
# ----------------------------
pipeline = joblib.load("models/full_pipeline.pkl")

# Required feature order
required_features = list(pipeline.feature_names_in_)

# ----------------------------
# Load UCI dataset
# ----------------------------
df = pd.read_csv("data/Uci_raw.csv")

# Remove leading/trailing spaces
df.columns = df.columns.str.strip()

# Replace '?' with NaN
df = df.replace("?", pd.NA)

# Rename columns to match model
rename_map = {
    "bp": "Bp",
    "sg": "Sg",
    "al": "Al",
    "su": "Su",
    "rbc": "Rbc",
    "bu": "Bu",
    "sc": "Sc",
    "sod": "Sod",
    "pot": "Pot",
    "hemo": "Hemo",
    "wbcc": "Wbcc",
    "rbcc": "Rbcc",
    "htn": "Htn",
    "class": "Class"
}

df = df.rename(columns=rename_map)

# Keep only required features
df = df[required_features + ["Class"]]

# Convert numeric columns to float
numeric_cols = ["Bp","Sg","Al","Su","Bu","Sc","Sod","Pot","Hemo","Wbcc","Rbcc"]
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

# Encode categoricals
df["Rbc"] = df["Rbc"].map({"normal": 1, "abnormal": 0})
df["Htn"] = df["Htn"].map({"yes": 1, "no": 0})
df["Class"] = df["Class"].map({"ckd": 1, "notckd": 0})

df = df.dropna()

X_ext = df[required_features]
y_ext = df["Class"]

# ----------------------------
# Predict
# ----------------------------
y_prob = pipeline.predict_proba(X_ext)[:, 1]
y_pred = pipeline.predict(X_ext)

# ----------------------------
# Metrics
# ----------------------------
auc = roc_auc_score(y_ext, y_prob)
f1 = f1_score(y_ext, y_pred)
acc = accuracy_score(y_ext, y_pred)

print("Schema AUC:", auc)
print("Schema F1:", f1)
print("Schema Accuracy:", acc)

