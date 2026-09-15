import uuid

def generate_tracking_number():
    return f"EXE-{uuid.uuid4().hex[:8].upper()}"