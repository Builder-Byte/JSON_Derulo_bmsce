import time
import os
import warnings
from transformers import logging as hf_logging
import logging

# --- SILENCE ALL TENSORFLOW/HUGGINGFACE WARNINGS ---
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
warnings.filterwarnings("ignore", category=UserWarning)
hf_logging.set_verbosity_error()
logging.getLogger("tensorflow").setLevel(logging.ERROR)

# --- IMPORT OUR PIPELINE ---
from pipeline import MentalStatePipeline

def run_simulation():
    print("\n🚀 INITIALIZING IMPACT AI 3.0 OBSERVABILITY ENGINE...\n")
    engine = MentalStatePipeline()
    history = []

    # --- THE SIMULATED USER JOURNEY ---
    interactions = [
        {
            "step": 1,
            "text": "Just woke up, getting ready for work.",
            "metrics": {"speed": 65.0, "backspaces": 2, "latency": 150.0},
            "hour": 8 # 8:00 AM
        },
        {
            "step": 2,
            "text": "Traffic was a nightmare but I made it to the office.",
            "metrics": {"speed": 60.0, "backspaces": 4, "latency": 180.0},
            "hour": 9
        },
        {
            "step": 3,
            "text": "Having a normal day, just answering emails.",
            "metrics": {"speed": 68.0, "backspaces": 1, "latency": 140.0},
            "hour": 14 # 2:00 PM (Baseline is now established)
        },
        {
            "step": 4,
            "text": "Honestly everything is totally amazing! I feel so great!",
            "metrics": {"speed": 25.0, "backspaces": 18, "latency": 450.0}, # The Fake Smile (Erratic typing)
            "hour": 16 
        },
        {
            "step": 5,
            "text": "I don't know why I feel so tired. Maybe I'm just stressed.",
            "metrics": {"speed": 40.0, "backspaces": 8, "latency": 300.0},
            "hour": 2 # 2:00 AM (Triggers Night Risk Multiplier)
        },
        {
            "step": 6,
            "text": "I can't do this anymore. It's too much. I'm completely overwhelmed.",
            "metrics": {"speed": 15.0, "backspaces": 25, "latency": 600.0},
            "hour": 3 # 3:00 AM (Severe strain + night + repetition)
        }
    ]

    print("📊 STARTING SIMULATION: Analyzing User Stream...\n")
    print("-" * 70)

    for data in interactions:
        print(f"🕒 [Step {data['step']} | Time: {data['hour']}:00]")
        print(f"📩 Input: \"{data['text']}\"")
        
        # Run the engine!
        output = engine.run(
            text=data['text'],
            typing_metrics=data['metrics'],
            history=history,
            local_hour=data['hour']
        )
        
        # Print Telemetry
        print(f"🧠 CSI: {output['csi']:.4f} | Risk: {output['risk_score']:.4f} | Z-Score: {output['z_score']:+.2f} SD")
        
        # Check for system flags
        if output['is_masking']:
            print("⚠️  SYSTEM ALERT: MASKING DETECTED (High Positivity + Erratic Telemetry)")
            
        if output['trigger_sos']:
            print("🚨 CRITICAL ALERT: TRIGGER SOS MODAL")
        elif output['suggested_intervention']:
            print(f"💡 INTERVENTION TRIGGERED: {output['suggested_intervention']}")

        # Print Engine Explanations
        if output['explanation']:
            print(f"🔍 AI Logic: {output['explanation']}")
            
        print("-" * 70)
        
        # Append to history (Simulating what state_manager.py will do)
        history.append({
            "csi": output["csi"],
            "risk": output["risk_score"],
            "is_masking": output["is_masking"],
            "explanation": output["explanation"]
        })
        
        time.sleep(1) # Artificial delay for dramatic effect

    # Print the final generated Markdown report
    print("\n📝 FINAL CLINICIAN REPORT GENERATED:\n")
    print(output["session_report_md"])
    print("\n✅ SIMULATION COMPLETE. SYSTEM IS READY FOR DEPLOYMENT.")

if __name__ == "__main__":
    run_simulation()