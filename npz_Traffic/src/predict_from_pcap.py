import joblib
import numpy as np
from pcap_to_features import extract_sequence

model = joblib.load("npz_Traffic/model.pkl")

pcap_file = "PCAP_Traffic/data/test/google_test.pcap"

features = extract_sequence(pcap_file)

features = features.reshape(1, -1)

prediction = model.predict(features)

print("Predicted label:", prediction[0])