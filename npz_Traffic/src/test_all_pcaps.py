import os
import joblib
from pcap_to_features import extract_sequence

MODEL_PATH = "npz_Traffic/model.pkl"
PCAP_FOLDER = "PCAP_Traffic/data/pcaps"

def main():
    model = joblib.load(MODEL_PATH)

    for filename in os.listdir(PCAP_FOLDER):
        if filename.endswith(".pcap"):
            pcap_path = os.path.join(PCAP_FOLDER, filename)

            features = extract_sequence(pcap_path)
            features = features.reshape(1, -1)

            prediction = model.predict(features)[0]

            expected = filename.replace(".pcap", "")
            print(f"File: {filename}")
            print(f"Expected: {expected}")
            print(f"Predicted label: {prediction}")
            print("-" * 40)

if __name__ == "__main__":
    main()