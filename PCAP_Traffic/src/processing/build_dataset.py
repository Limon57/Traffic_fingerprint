import os
import pandas as pd
from PCAP_Traffic.src.processing.feature_extractor import extract_features


def build_dataset(pcap_folder, output_file):
    data = []

    for file in os.listdir(pcap_folder):
        if file.endswith(".pcap"):
            filepath = os.path.join(pcap_folder, file)

            print(f"Processing: {file}")

            features = extract_features(filepath)

            if features is None:
                continue


            label = file.split("_")[0]

            features["label"] = label
            data.append(features)

    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)

    print(f"\nDataset saved to {output_file}")