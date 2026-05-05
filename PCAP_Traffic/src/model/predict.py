import sys
from pathlib import Path
from typing import Any


_project_root = Path(__file__).resolve().parents[3]
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

import joblib
import pandas as pd

from PCAP_Traffic.src.processing.feature_extractor import extract_features


MODEL_PATH = Path(__file__).resolve().parents[2] / "model.pkl"


def predict_website(pcap_file: str) -> dict[str, Any]:
    pcap_path = Path(pcap_file)

    if not pcap_path.exists():
        return {
            "success": False,
            "prediction": None,
            "confidence_scores": {},
            "error": f"File not found: {pcap_file}",
        }

    if not MODEL_PATH.exists():
        return {
            "success": False,
            "prediction": None,
            "confidence_scores": {},
            "error": f"Model file not found: {MODEL_PATH}",
        }

    try:
        model = joblib.load(MODEL_PATH)
    except Exception as e:
        return {
            "success": False,
            "prediction": None,
            "confidence_scores": {},
            "error": f"Failed to load model: {e}",
        }

    try:
        features = extract_features(str(pcap_path))
    except Exception as e:
        return {
            "success": False,
            "prediction": None,
            "confidence_scores": {},
            "error": f"Feature extraction failed: {e}",
        }

    if features is None:
        return {
            "success": False,
            "prediction": None,
            "confidence_scores": {},
            "error": "No packets found in PCAP.",
        }

    try:
        df = pd.DataFrame([features])
        prediction = model.predict(df)[0]

        confidence_scores: dict[str, float] = {}

        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(df)[0]
            classes = model.classes_
            confidence_scores = {
                str(cls): float(prob) for cls, prob in zip(classes, probs)
            }

        return {
            "success": True,
            "prediction": str(prediction),
            "confidence_scores": confidence_scores,
            "error": None,
        }

    except Exception as e:
        return {
            "success": False,
            "prediction": None,
            "confidence_scores": {},
            "error": f"Prediction failed: {e}",
        }