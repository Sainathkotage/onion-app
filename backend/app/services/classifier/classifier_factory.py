import os
from app.services.classifier.base_classifier import BaseOnionClassifier
from app.services.classifier.gemini_classifier import GeminiOnionClassifier
from app.services.classifier.demo_classifier import DemoOnionClassifier
from app.services.classifier.densenet121_classifier import DenseNet121OnionClassifier
from app.services.classifier.pretrained_classifier import PretrainedOnionClassifier
from app.services.classifier.tflite_classifier import TFLiteOnionClassifier, HAS_LITERT
from app.config import BASE_DIR, GEMINI_API_KEY, SUPPRESS_OTHER_MODELS

class OnionClassifierFactory:
    """
    Factory pattern for creating onion defect classifiers.
    Prioritizes Google Gemini Multimodal Vision for defect classification,
    while suppressing other legacy ML models (DenseNet, TFLite, CV demo).
    """
    @staticmethod
    def get_classifier(classifier_type: str = None) -> BaseOnionClassifier:
        # If other models are suppressed or Gemini API key is available, use Gemini
        if SUPPRESS_OTHER_MODELS or classifier_type in ["gemini", "google", "gemini_classifier"]:
            return GeminiOnionClassifier()

        tflite_paths = [
            str(BASE_DIR.parent / "ml" / "models" / "onion_classifier.tflite"),
            str(BASE_DIR.parent / "frontend_mobile" / "assets" / "models" / "onion_classifier.tflite"),
            str(BASE_DIR.parent / "onion_classifier.tflite"),
            str(BASE_DIR / "onion_classifier.tflite"),
            "onion_classifier.tflite"
        ]
        tflite_path = next((p for p in tflite_paths if os.path.exists(p)), tflite_paths[0])
        densenet_path = os.getenv("DENSENET_MODEL_PATH", str(BASE_DIR.parent / "ml" / "models" / "densenet121_onion.pth"))

        if classifier_type is None:
            if GEMINI_API_KEY:
                classifier_type = "gemini"
            elif HAS_LITERT and os.path.exists(tflite_path):
                classifier_type = "tflite"
            elif os.path.exists(densenet_path):
                classifier_type = "densenet121"
            else:
                classifier_type = os.getenv("ONION_CLASSIFIER_TYPE", "demo").lower()

        if classifier_type in ["gemini", "google"]:
            return GeminiOnionClassifier()
        elif classifier_type in ["tflite", "lite"]:
            return TFLiteOnionClassifier(model_path=tflite_path)
        elif classifier_type in ["densenet121", "densenet", "dense"]:
            weights_path = os.getenv("DENSENET_MODEL_PATH", "ml/models/densenet121_onion.pth")
            return DenseNet121OnionClassifier(model_path=weights_path)
        elif classifier_type in ["pretrained", "resnet", "mobilenet"]:
            return PretrainedOnionClassifier()
        elif classifier_type in ["demo", "cv"]:
            return DemoOnionClassifier()
        else:
            return GeminiOnionClassifier()
