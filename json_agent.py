import json
from memory.shared_memory import SharedMemory

class JSONAgent:
    def __init__(self):
        self.memory = SharedMemory()

    def validate_and_process(self, json_path):
        with open(json_path) as f:
            data = json.load(f)

        # Example: Required fields
        required_fields = ['invoice_id', 'date', 'amount']
        missing = [f for f in required_fields if f not in data]

        fields = json.dumps(data)
        anomalies = {"missing": missing} if missing else {}
        self.memory.log(json_path, "JSON", "Invoice", fields=fields)

        return {"status": "ok", "missing": missing}
