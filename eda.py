import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import os

print("Working directory:", os.getcwd())
os.makedirs("outputs", exist_ok=True)
print("Saving charts to:", os.path.abspath("outputs"))

sns.set(style="whitegrid")
os.makedirs("outputs", exist_ok=True)

# Load data
df = pd.read_csv("hospital_readmissions_30k.csv")

# Create numeric target
df["readmitted"] = df["readmitted_30_days"].map({"Yes": 1, "No": 0})

# Basic checks
print(df.head())
print(df.info())
print(df.describe())

# Target distribution
print("\nReadmission distribution (%):")
print(df["readmitted"].value_counts(normalize=True) * 100)

sns.countplot(x="readmitted", data=df)
plt.title("Readmission Distribution")
plt.savefig("outputs/readmission_distribution.png", dpi=300, bbox_inches="tight")
plt.close()

# Age vs readmission
sns.boxplot(x="readmitted", y="age", data=df)
plt.title("Age vs Readmission")
plt.savefig("outputs/age_vs_readmission.png", dpi=300, bbox_inches="tight")
plt.close()

# Length of stay vs readmission
sns.boxplot(x="readmitted", y="length_of_stay", data=df)
plt.title("Length of Stay vs Readmission")
plt.savefig("outputs/los_vs_readmission.png", dpi=300, bbox_inches="tight")
plt.close()

# Diabetes & readmission
sns.barplot(x="diabetes", y="readmitted", data=df, estimator=np.mean)
plt.title("Readmission Rate by Diabetes Status")
plt.savefig("outputs/diabetes_readmission.png", dpi=300, bbox_inches="tight")
plt.close()

# Correlation heatmap
numeric_cols = [
    "age",
    "cholesterol",
    "bmi",
    "medication_count",
    "length_of_stay",
    "readmitted"
]

plt.figure(figsize=(8,6))
sns.heatmap(
    df[numeric_cols].corr(),
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)
plt.title("Correlation Matrix")
plt.savefig("outputs/correlation_heatmap.png", dpi=300, bbox_inches="tight")
plt.close()

readmission_rate = df["readmitted"].mean() * 100
avg_los_all = df["length_of_stay"].mean()
avg_los_readmit = df.loc[df["readmitted"] == 1, "length_of_stay"].mean()
avg_los_no = df.loc[df["readmitted"] == 0, "length_of_stay"].mean()

print("\n=== HEADLINE METRICS ===")
print(f"Readmission rate: {readmission_rate:.2f}%")
print(f"Avg LOS (all): {avg_los_all:.2f}")
print(f"Avg LOS (readmitted=1): {avg_los_readmit:.2f}")
print(f"Avg LOS (readmitted=0): {avg_los_no:.2f}")

los_readmit = df.loc[df["readmitted"] == 1, "length_of_stay"].mean()
los_no = df.loc[df["readmitted"] == 0, "length_of_stay"].mean()

print("\nAvg length_of_stay (readmitted=1):", round(los_readmit, 2))
print("Avg length_of_stay (readmitted=0):", round(los_no, 2))

dest_rate = (df.groupby("discharge_destination")["readmitted"].mean() * 100).sort_values(ascending=False)
print("\nTop 10 discharge destinations by readmission rate (%):")
print(dest_rate.head(10).round(2))

import os
os.makedirs("outputs", exist_ok=True)

top10 = dest_rate.head(10)

plt.figure(figsize=(10,5))
top10.plot(kind="bar")
plt.title("Top 10 Discharge Destinations by Readmission Rate (%)")
plt.ylabel("Readmission Rate (%)")
plt.savefig("outputs/discharge_destination_risk.png", dpi=300, bbox_inches="tight")
plt.close()

