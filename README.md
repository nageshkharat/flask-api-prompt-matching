# Prompt Matching API

A Flask-based REST API with MVC architecture for matching system prompts based on input criteria.

## Installation

```bash
pip install -r requirements.txt
python app.py
```

## Usage

POST to `/match-prompt` with JSON:
```json
{
    "situation": "Commercial Auto",
    "level": "Structure", 
    "file_type": "Summary Report",
    "data": ""
}
```

## Prompt Matching

- Prompt 1: Commercial Auto + Structure + Summary Report
- Prompt 2: General Liability + Summarize + Deposition  
- Prompt 3: Commercial Auto + Summarize + Summons
- Prompt 4: Workers Compensation + Structure + Medical Records
- Prompt 5: Workers Compensation + Summarize + Summons

## Testing

```bash
python test_api.py
``` 