"""
Local sentiment analysis using Hugging Face transformers.

All inference runs on-device. No data is sent to external APIs.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Sequence

logger = logging.getLogger(__name__)


@dataclass
class SentimentResult:
    label: str  # "POSITIVE" | "NEGATIVE" | "NEUTRAL"
    score: float  # 0.0 - 1.0 confidence


class SentimentAnalyzer:
    """
    Batch sentiment classifier.

    Uses DistilBERT fine-tuned on SST-2 by default. Model is downloaded
    once from Hugging Face and cached locally.
    """

    def __init__(
        self,
        model_name: str = "distilbert-base-uncased-finetuned-sst-2-english",
        batch_size: int = 16,
    ) -> None:
        self._model_name = model_name
        self._batch_size = batch_size
        self._pipeline = None  # Lazy load

    def _ensure_loaded(self) -> None:
        if self._pipeline is not None:
            return
        try:
            from transformers import pipeline  # type: ignore
        except ImportError as e:
            raise RuntimeError(
                "transformers is required. Install via: pip install -r requirements.txt"
            ) from e

        logger.info("Loading local sentiment model: %s", self._model_name)
        self._pipeline = pipeline(
            "sentiment-analysis",
            model=self._model_name,
            device=-1,  # CPU by default; -1 = CPU, 0 = first GPU
        )

    def analyze(self, texts: Sequence[str]) -> list[SentimentResult]:
        """Analyze a batch of texts. Returns one result per input."""
        if not texts:
            return []
        self._ensure_loaded()

        results: list[SentimentResult] = []
        for i in range(0, len(texts), self._batch_size):
            batch = list(texts[i : i + self._batch_size])
            # Truncate long comments — DistilBERT max = 512 tokens
            batch = [t[:2000] for t in batch]
            outputs = self._pipeline(batch, truncation=True)
            for out in outputs:
                results.append(
                    SentimentResult(label=out["label"], score=float(out["score"]))
                )
        return results
