import numpy as np
import time
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


NUM_TREES = 100
SUBSET_SIZE = None

MODEL_OUTPUT = "npz_Traffic/model.pkl"
REPORT_OUTPUT = "npz_Traffic/training_report.txt"


print("Loading dataset...")
data = np.load("npz_Traffic/data/Front.npz")

if SUBSET_SIZE is None:
    X = data["X"]
    y = data["y"]
else:
    X = data["X"][:SUBSET_SIZE]
    y = data["y"][:SUBSET_SIZE]

print(f"Dataset loaded: {X.shape}")


print("Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


print("\nTraining RandomForest...")

model = RandomForestClassifier(
    n_estimators=1,
    warm_start=True,
    n_jobs=-1,
    random_state=42
)

start_time = time.time()

for i in range(1, NUM_TREES + 1):
    model.n_estimators = i
    model.fit(X_train, y_train)

    elapsed = time.time() - start_time
    avg_time = elapsed / i
    remaining = avg_time * (NUM_TREES - i)

    print(f"Tree {i}/{NUM_TREES} | elapsed: {elapsed:.1f}s | remaining: {remaining:.1f}s")


print("\nEvaluating model...")
predictions = model.predict(X_test)

report = classification_report(y_test, predictions, zero_division=0)

print("\nClassification Report:")
print(report)


joblib.dump(model, MODEL_OUTPUT)
print(f"\nModel saved to: {MODEL_OUTPUT}")


with open(REPORT_OUTPUT, "w") as f:
    f.write("Dataset shape: " + str(X.shape) + "\n\n")
    f.write(report)

print(f"Training report saved to: {REPORT_OUTPUT}")


total_time = time.time() - start_time
print(f"\nTotal training time: {total_time:.1f} seconds")