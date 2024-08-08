import json
import time
from datetime import datetime

def sanitize(s):
    return s.strip()

def transform_value(key, value):
    if 'S' in value:
        s = sanitize(value['S'])
        if not s:
            return None
        try:
            dt = datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
            return int(dt.timestamp())
        except ValueError:
            return s
    elif 'N' in value:
        try:
            return float(sanitize(value['N']).lstrip('0') or '0')
        except ValueError:
            return None
    elif 'BOOL' in value:
        b = sanitize(value['BOOL']).lower()
        if b in ['1', 't', 'true']:
            return True
        elif b in ['0', 'f', 'false']:
            return False
        return None
    elif 'NULL' in value:
        n = sanitize(value['NULL']).lower()
        return None if n in ['1', 't', 'true'] else False
    elif 'L' in value:
        if isinstance(value['L'], list):
            return [transform_value('', v) for v in value['L'] if transform_value('', v) is not None]
        return None
    elif 'M' in value:
        return transform_map(value['M'])
    return None

def transform_map(data):
    result = {}
    for key, value in sorted(data.items()):
        key = sanitize(key)
        if key:
            transformed = transform_value(key, value)
            if transformed is not None:
                result[key] = transformed
    return result if result else None

def transform_json(data):
    transformed = transform_map(data)
    return [transformed] if transformed else []

# Main execution
if __name__ == "__main__":
    start_time = time.time()

    with open('input.json', 'r') as f:
        input_data = json.load(f)

    output_data = transform_json(input_data)

    print(json.dumps(output_data, indent=2))

    end_time = time.time()
    print(f"\nExecution time: {end_time - start_time:.6f} seconds")
