import os
import json
import datetime
from dotenv import load_dotenv
from agents.email_agent import EmailAgent
from agents.classifier_agent import classify_input
from agents.json_agent import JSONAgent
from memory.shared_memory import SharedMemory

load_dotenv()

def load_input(file_path):
    if file_path.endswith(".json"):
        with open(file_path, "r") as f:
            return f.read(), "json"
    elif file_path.endswith(".pdf"):
        import pdfplumber
        with pdfplumber.open(file_path) as pdf:
            text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        return text, "pdf"
    elif file_path.endswith(".txt"):
        with open(file_path, "r") as f:
            return f.read(), "email"
    else:
        raise ValueError("Unsupported file type.")


# def classify_input(content, format_hint):
#     content_lower = content.lower()

#     # Infer format
#     if format_hint == "json":
#         file_format = "json"
#     elif format_hint == "email" or "from:" in content_lower or "subject:" in content_lower:
#         file_format = "email"
#     elif format_hint == "pdf":
#         file_format = "pdf"
#     else:
#         file_format = "unknown"

#     # Infer intent
#     if "quotation" in content_lower or "procure" in content_lower:
#         intent = "rfq"
#     elif "invoice" in content_lower:
#         intent = "invoice"
#     elif "complaint" in content_lower:
#         intent = "complaint"
#     elif "regulation" in content_lower:
#         intent = "regulation"
#     else:
#         intent = "other"

#     return {"format": file_format, "intent": intent}

def main(file_path):
    content, format_hint = load_input(file_path)

    
    result = classify_input(content, format_hint)
    intent = result.get("intent")
    format_detected = result.get("format")

    print(f"\n Format: {format_detected},  Intent: {intent}")

   
    email_agent = EmailAgent()
    json_agent = JSONAgent()

    
    if format_detected == "json":
        processed = json_agent.validate_and_process(file_path)
    elif format_detected == "email":
        processed = email_agent.process_email(intent,content, file_path)
    else:
        print("Unsupported format for routing.")
        return

    
    shared_memory = SharedMemory()
    shared_memory.log(
        source=file_path,
        type_=format_detected,
        intent=intent,
        # timestamp=datetime.datetime.now().isoformat(),
        fields=processed
    )

    print("\n Final Processed Output:")
    try:
        parsed = json.loads(processed) if isinstance(processed, str) else processed
        print(json.dumps(parsed, indent=2))
    except:
        print(processed)

if __name__ == "__main__":
    main("input_samples/sample_email.txt")
