import datetime

from matplotlib import text
from emotion import EmotionEngine
from features import FeatureExtractor
from csi import CSIComputer
from risk_model import RiskModel
from intervention import InterventionEngine
from report import ReportGenerator
from audio_engine import VoiceModulationEngine

class MentalStatePipeline:
    def __init__(self):
        # 1. Initialize the Core Extractors
        self.emotion = EmotionEngine()
        self.features = FeatureExtractor()
        self.audio_engine = VoiceModulationEngine() # NEW: Acoustic Engine
        
        # 2. Initialize the Calculators
        self.csi = CSIComputer()
        self.risk = RiskModel(alpha=0.3)
        
        # 3. Initialize the Action Engines (Tier 2 Features)
        self.intervention = InterventionEngine()
        self.report_gen = ReportGenerator()

    def run(self, text: str, typing_metrics: dict, history: list, local_hour: int = None, audio_path: str = None) -> dict:
        """
        Executes the full Multimodal (Text + Keystroke + Acoustic) pipeline.
        """
        # Fallback to server time if the frontend doesn't provide the user's local hour
        if local_hour is None:
            local_hour = datetime.datetime.now().hour

        # We start an explanations array early to catch acoustic anomalies
        explanations = []

        # --- STEP 1: Feature Extraction ---
        emo = self.emotion.predict(text)
        
        feats = {
            "negativity": self.features.compute_negativity(emo["scores"], text),
            "positivity": self.features.compute_positivity(emo["scores"]),
            "uncertainty": self.features.compute_uncertainty(text),
            "repetition": self.features.compute_repetition(text),
            "typing_irregularity": self.features.typing_irregularity(typing_metrics)
        }

        # --- STEP 2: Base Masking Detection ---
        is_masking = self.features.detect_masking(feats["positivity"], feats["typing_irregularity"])

        # --- STEP 3: Vocal Telemetry Processing (The Judge's Request) ---
        vocal_strain = 0.0
        if audio_path:
            voice_metrics = self.audio_engine.extract_vocal_telemetry(audio_path)
            vocal_strain = voice_metrics.get("vocal_strain_index", 0.0)
            
            # THE OVERRIDE: If the user's voice is literally shaking, force a masking flag
            if vocal_strain > 0.75 and not is_masking:
                is_masking = True
                explanations.append("Acoustic anomaly: High vocal tremor detected contradicting semantic input.")

        # --- STEP 4: Cognitive Strain Index (CSI) Calibration ---
        raw_csi = self.csi.compute_raw(feats)
        
        # Acoustic Fusion: Blend the typing/text strain with the vocal strain
        if audio_path:
            raw_csi = (0.6 * raw_csi) + (0.4 * vocal_strain)

        z_score = self.csi.compute_z_score(raw_csi, history)

        # --- STEP 5: Temporal Risk & Interpretability ---
        risk_score, risk_explanations = self.risk.compute(
            current_csi=raw_csi, 
            z_score=z_score, 
            is_masking=is_masking, 
            history=history
        )
        explanations.extend(risk_explanations)

        # --- THE FAIL-SAFE: CRISIS LEXICON OVERRIDE ---
        # If the user explicitly states severe distress, bypass all EMA smoothing!
        crisis_keywords = [
            "kill myself", "killing myself", "suicide", "end it all", 
            "want to die", "can't do this anymore", "no reason to live",
            "i give up", "giving up", "no point anymore" # Added your test phrases!
        ]
        text_lower = text.lower()
        if any(keyword in text_lower for keyword in crisis_keywords):
            risk_score = 1.00  # Instantly max out the risk
            explanations.append("CRITICAL: Severe crisis lexicon detected. Bypassing temporal smoothing.")
            is_masking = False # They aren't masking, they are explicitly crying for help

        # --- STEP 6: Intervention & Action Triggers ---
        action_plan = self.intervention.determine_action(
            risk_score=risk_score, 
            is_masking=is_masking, 
            local_hour=local_hour
        )

        # --- STEP 7: AI Clinical Report Generation ---
        current_state = {
            "csi": raw_csi, 
            "risk": risk_score, 
            "is_masking": is_masking,
            "explanation": explanations
        }
        session_report = self.report_gen.generate_summary(history + [current_state])

        # --- STEP 8: The Final Data Payload ---
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