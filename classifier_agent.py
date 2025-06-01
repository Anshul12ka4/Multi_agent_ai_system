import json
from transformers import pipeline

# Use zero-shot classification for free alternative
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def classify_input(content, format_hint):
    
    trimmed_content = content[:1000] if len(content) > 1000 else content

    labels = ["invoice", "RFQ", "complaint", "regulation", "other"]

    try:
        result = classifier(trimmed_content, candidate_labels=labels)
        top_intent = result["labels"][0].lower()

        return {
            "format": format_hint.lower(),
            "intent": top_intent
        }

    except Exception as e:
        print(" Classification failed:", str(e))
        return {"format": "unknown", "intent": "unknown"}
