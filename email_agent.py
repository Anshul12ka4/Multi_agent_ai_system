import re
from memory.shared_memory import SharedMemory

class EmailAgent:
    def __init__(self):
        self.memory = SharedMemory()

    def process_email(self,intent, email_text, source_path):
        # Extract sender (from a line like: "From: someone@example.com")
        sender_match = re.search(r'From:\s*(.+)', email_text, re.IGNORECASE)
        sender = sender_match.group(1).strip() if sender_match else "unknown"

        # # Detect intent
        # if "quotation" in email_text.lower() or "procure" in email_text.lower():
        #     intent = "rfq"
        # elif "complaint" in email_text.lower():
        #     intent = "complaint"
        # elif "invoice" in email_text.lower():
        #     intent = "invoice"
        # elif "regulation" in email_text.lower():
        #     intent = "regulation"
        # else:
        #     intent = "other"

        # Urgency keywords
        urgency = "low"
        if "urgent" in email_text.lower() or "priority" in email_text.lower():
            urgency = "high"
        elif "asap" in email_text.lower() or "soon" in email_text.lower():
            urgency = "medium"

        # Extract email body (naive approach: skip lines like From:/Subject:/Regards)
        body_lines = []
        for line in email_text.strip().splitlines():
            if not re.match(r'^(From|Subject|Regards|Best|Sincerely|Thanks)', line.strip(), re.IGNORECASE):
                body_lines.append(line.strip())
        body = " ".join(body_lines).strip()

        result = {
            "sender": sender,
            "intent": intent,
            "urgency": urgency,
            "body": body
        }

        self.memory.log(source_path, "email", intent, fields=result)

        return result
