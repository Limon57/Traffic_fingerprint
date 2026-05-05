import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


def train_model(dataset_path):

    df = pd.read_csv(dataset_path)


    X = df.drop("label", axis=1)
    y = df["label"]


    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )


    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42
    )


    model.fit(X_train, y_train)


    y_pred = model.predict(X_test)


    accuracy = accuracy_score(y_test, y_pred)

    print("\n==============================")
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    print("==============================\n")

    print("Classification Report:")
    print(classification_report(y_test, y_pred))


    print("\nFeature Importance:")
    for feature, importance in zip(X.columns, model.feature_importances_):
        print(f"{feature}: {importance:.4f}")

    joblib.dump(model, "model.pkl")
    print("\nModel saved as model.pkl")

    return model



if __name__ == "__main__":
    train_model("PCAP_Traffic/data/features.csv")