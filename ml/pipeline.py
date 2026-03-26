import datetime
from emotion import EmotionEngine
from features import FeatureExtractor
from csi import CSIComputer
from risk_model import RiskModel
from intervention import InterventionEngine
from report import ReportGenerator

class MentalStatePipeline:
    def __init__(self):
        # 1. Initialize the Core Extractors
        self.emotion = EmotionEngine()
        self.features = FeatureExtractor()
        
        # 2. Initialize the Calculators
        self.csi = CSIComputer()
        self.risk = RiskModel(alpha=0.3)
        
        # 3. Initialize the Action Engines (Tier 2 Features)
        self.intervention = InterventionEngine()
        self.report_gen = ReportGenerator()

    def run(self, text: str, typing_metrics: dict, history: list, local_hour: int = None) -> dict:
        """
        Executes the full Multimodal Temporal Observability pipeline.
        """
        # Fallback to server time if the frontend doesn't provide the user's local hour
        if local_hour is None:
            local_hour = datetime.datetime.now().hour

        # --- STEP 1: Feature Extraction ---
        emo = self.emotion.predict(text)
        
        feats = {
            "negativity": self.features.compute_negativity(emo["scores"], text),
            "positivity": self.features.compute_positivity(emo["scores"]),
            "uncertainty": self.features.compute_uncertainty(text),
            "repetition": self.features.compute_repetition(text),
            "typing_irregularity": self.features.typing_irregularity(typing_metrics)
        }

        # --- STEP 2: Masking Detection ---
        is_masking = self.features.detect_masking(feats["positivity"], feats["typing_irregularity"])

        # --- STEP 3: Cognitive Strain Index (CSI) Calibration ---
        raw_csi = self.csi.compute_raw(feats)
        z_score = self.csi.compute_z_score(raw_csi, history)

        # --- STEP 4: Temporal Risk & Interpretability ---
        risk_score, explanations = self.risk.compute(
            current_csi=raw_csi, 
            z_score=z_score, 
            is_masking=is_masking, 
            history=history
        )

        # --- STEP 5: Intervention & Action Triggers ---
        action_plan = self.intervention.determine_action(
            risk_score=risk_score, 
            is_masking=is_masking, 
            local_hour=local_hour
        )

        # --- STEP 6: AI Clinical Report Generation ---
        # We append the current state to history temporarily just for the report generation
        current_state = {
            "csi": raw_csi, 
            "risk": risk_score, 
            "is_masking": is_masking,
            "explanation": explanations
        }
        session_report = self.report_gen.generate_summary(history + [current_state])

        # --- STEP 7: The Final Data Payload ---
        # This dictionary exactly matches the FastAPI RiskAnalysisSchema
        return {
            "emotion": emo,
            "features": feats,
            "csi": round(raw_csi, 4),
            "z_score": round(z_score, 4),
            "is_masking": is_masking,
            "risk_score": round(risk_score, 4), 
            "explanation": explanations,
            "trigger_sos": action_plan["trigger_sos"],
            "suggested_intervention": action_plan["suggested_intervention"],
            "session_report_md": session_report
        }