"""
FE9.2 - AI-Generated Image Detection
Returns a model prediction as a warning only, not a final decision.
"""
from pathlib import Path
import os

DEFAULT_MODEL = "umm-maybe/AI-image-detector"


def normalize_label(label):
    return label.lower().replace("_", " ").replace("-", " ").strip()


def label_is_ai(label):
    text = normalize_label(label)
    return any(word in text for word in
               ("artificial", "ai generated", "generated", "synthetic", "fake"))


def label_is_real(label):
    text = normalize_label(label)
    return any(word in text for word in
               ("human", "real", "authentic", "photograph", "natural"))


def detect_ai_image(image_path, warning_threshold=0.90, model_name=None):
    """
    Estimate AI-generated likelihood using a pretrained classifier.

    warning_threshold is configurable and must be validated on a project
    dataset. It is not an official threshold specified by the SRS.
    """
    image_path = Path(image_path)
    if not image_path.is_file():
        raise FileNotFoundError(image_path)
    if not 0 <= warning_threshold <= 1:
        raise ValueError("warning_threshold must be between 0 and 1")

    try:
        from transformers import pipeline
    except ImportError as exc:
        raise RuntimeError(
            "Missing packages. Run: pip install -r requirements.txt"
        ) from exc

    selected_model = model_name or os.getenv("AI_DETECTOR_MODEL", DEFAULT_MODEL)

    try:
        classifier = pipeline(
            "image-classification",
            model=selected_model,
            device=-1
        )
        predictions = classifier(str(image_path))
    except Exception as exc:
        raise RuntimeError(
            "Could not load/run the model. The first run needs Internet "
            f"to download model files. Details: {exc}"
        ) from exc

    if not predictions:
        raise RuntimeError("The model returned no prediction.")

    best = max(predictions, key=lambda item: float(item.get("score", 0)))
    label = str(best.get("label", "unknown"))
    score = float(best.get("score", 0))

    if label_is_ai(label):
        estimated_ai_probability = score
    elif label_is_real(label):
        estimated_ai_probability = 1 - score
    else:
        return {
            "feature": "FE9.2",
            "image": str(image_path.resolve()),
            "predicted_label": label,
            "model_score": round(score, 4),
            "status": "MANUAL_REVIEW_REQUIRED",
            "warning": "Unknown model label. Check model label mapping before interpreting."
        }

    if estimated_ai_probability >= warning_threshold:
        status = "HIGH_AI_LIKELIHOOD_WARNING"
    elif estimated_ai_probability >= 0.60:
        status = "REVIEW_RECOMMENDED"
    else:
        status = "LOW_AI_SIGNAL"

    return {
        "feature": "FE9.2",
        "image": str(image_path.resolve()),
        "predicted_label": label,
        "model_score": round(score, 4),
        "estimated_ai_probability": round(estimated_ai_probability, 4),
        "warning_threshold": warning_threshold,
        "status": status,
        "decision": (
            "Warning only. Organizer must review the submission. "
            "The model does not make a final violation decision."
        ),
        "model": selected_model,
        "all_predictions": predictions
    }
