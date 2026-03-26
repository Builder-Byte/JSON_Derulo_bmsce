from typing import Dict

from pydantic import BaseModel


class EmotionSchema(BaseModel):
	label: str
	scores: Dict[str, float]


class FeaturesSchema(BaseModel):
	negativity: float
	uncertainty: float
	typing_irregularity: float


class RiskAnalysisSchema(BaseModel):
	emotion: EmotionSchema
	features: FeaturesSchema
	csi: float
	risk_score: float