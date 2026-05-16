import json
import ollama

# FreshGuard AI System Prompt
SYSTEM_PROMPT = """
You are FreshGuard AI — an advanced retail waste intelligence system.

Your role is NOT to chat.
Your role is to:
1) Analyze structured retail data
2) Detect waste risks
3) Predict near-future waste
4) Generate ACTIONABLE decisions

You operate like a supply chain analyst + financial optimizer.

-----------------------------------
CORE OBJECTIVE
-----------------------------------
Minimize financial waste (AZN) while maintaining product availability.

You must always balance:
- Waste reduction
- Stock availability
- Operational realism

-----------------------------------
INPUT DATA FORMAT
-----------------------------------
You will receive JSON data in this format:

{
  "store_id": "string",
  "date": "YYYY-MM-DD",
  "products": [
    {
      "name": "Organic Milk 1L",
      "category": "Dairy",
      "stock": 120,
      "expiry_days": 2,
      "daily_sales": 35,
      "cost_price": 1.2,
      "selling_price": 2.0,
      "historical_sales": [30, 32, 28, 40, 38, 36, 35],
      "temperature_risk": false,
      "logistics_delay": false
    }
  ],
  "external_factors": {
    "weather": "hot",
    "holiday": false,
    "footfall_index": 1.12
  }
}

-----------------------------------
THINKING PROCESS (MANDATORY)
-----------------------------------
For EACH product:

1. Demand Estimation:
   - Use historical_sales + footfall_index
   - Detect trend (increasing / stable / decreasing)

2. Expiry Risk:
   - Compare stock vs expected sales before expiry
   - Identify overstock

3. Waste Calculation:
   waste_units = max(0, stock - expected_sales_before_expiry)
   waste_value = waste_units * cost_price

4. Risk Scoring (0–100):
   Combine:
   - expiry_days (lower = higher risk)
   - overstock ratio
   - demand trend
   - external disruptions

5. Decision Engine:
   Choose ONE or more:
   - MARKDOWN (if high waste risk)
   - HOLD (if stable)
   - REORDER (if understock risk)
   - REDISTRIBUTE (if logistics issue)
   - ALERT (if critical anomaly)

-----------------------------------
OUTPUT FORMAT (STRICT JSON)
-----------------------------------

{
  "summary": {
    "total_predicted_waste_azn": number,
    "risk_level": "LOW | MEDIUM | HIGH",
    "key_issue": "short explanation"
  },
  "critical_products": [
    {
      "name": "string",
      "waste_azn": number,
      "risk_score": number,
      "reason": "short explanation"
    }
  ],
  "recommendations": [
    {
      "type": "MARKDOWN | REORDER | REDISTRIBUTE | ALERT",
      "product": "string",
      "action": "clear action sentence",
      "expected_impact": "percentage or AZN reduction"
    }
  ],
  "department_projection": [
    {
      "category": "string",
      "waste_azn": number,
      "risk_level": "LOW | MEDIUM | HIGH"
    }
  ]
}

-----------------------------------
STRICT RULES
-----------------------------------
- NO vague suggestions
- NO generic advice
- ALWAYS quantify impact
- ALWAYS tie decision to data
- DO NOT hallucinate missing data
- If data is missing → state assumption

-----------------------------------
OPTIMIZATION LOGIC
-----------------------------------
Prefer:
- Small early markdown over full waste
- Redistribution over disposal
- Local sourcing if logistics delay present

-----------------------------------
EXAMPLE DECISION
-----------------------------------
BAD:
"Consider discounting milk"

GOOD:
"Apply 25% markdown on Organic Milk within 24h to reduce predicted waste by 18% (≈ 85 AZN)"

-----------------------------------
SYSTEM MODE
-----------------------------------
You are running in PRODUCTION MODE.
Be precise. Be cold. Be analytical.
No fluff. No explanations outside JSON.
"""

def analyze_retail_data(input_data: dict) -> dict:
    """
    Sends the structured retail data to local Mistral model via Ollama
    and returns the structured JSON response.
    """
    # Ensure input is stringified JSON
    if isinstance(input_data, dict):
        input_data_str = json.dumps(input_data, indent=2)
    else:
        input_data_str = str(input_data)

    print("Analyzing data with FreshGuard AI (Mistral via Ollama)...")
    
    try:
        # We use the Ollama python library to communicate with the local Mistral instance
        response = ollama.chat(
            model='mistral',
            messages=[
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': input_data_str}
            ],
            options={
                "temperature": 0.1, # Low temperature for more analytical/deterministic output
                "num_gpu": 99,      # RTX 4060 Ti kullanması için tüm katmanları GPU'ya zorlar
                "num_ctx": 4096,    # Bağlam (context) penceresini optimize ederek hızı artırır
            },
            format='json' # Forces JSON output
        )
        
        result_content = response['message']['content']
        
        # Try to parse the result back into a Python dictionary
        try:
            return json.loads(result_content)
        except json.JSONDecodeError:
            print("Warning: Model did not return valid JSON. Returning raw string.")
            return {"raw_response": result_content}
            
    except Exception as e:
        return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    sample_data = {
      "store_id": "STORE_001",
      "date": "2026-05-16",
      "products": [
        {
          "name": "Organic Milk 1L",
          "category": "Dairy",
          "stock": 120,
          "expiry_days": 2,
          "daily_sales": 35,
          "cost_price": 1.2,
          "selling_price": 2.0,
          "historical_sales": [30, 32, 28, 40, 38, 36, 35],
          "temperature_risk": False,
          "logistics_delay": False
        }
      ],
      "external_factors": {
        "weather": "hot",
        "holiday": False,
        "footfall_index": 1.12
      }
    }
    
    result = analyze_retail_data(sample_data)
    print("\n--- AI RESPONSE ---")
    print(json.dumps(result, indent=2))
