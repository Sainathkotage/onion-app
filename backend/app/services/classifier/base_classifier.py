from abc import ABC, abstractmethod
from typing import List, Dict

class BaseOnionClassifier(ABC):
    """
    Abstract Base Class for Onion Defect Classifiers.
    Exposes 5 standardized classes: Healthy, Damaged, Rotten, Sprouted, Undersized.
    """
    CLASSES = ["Healthy", "Damaged", "Rotten", "Sprouted", "Undersized"]

    @abstractmethod
    def classify_batch(self, onions: List[Dict], upload_id: str) -> Dict:
        """
        Classifies a batch of detected onions.
        Returns dict matching BatchClassificationResult schema.
        """
        pass
