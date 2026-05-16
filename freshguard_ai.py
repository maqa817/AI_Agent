import json
import ollama

# FreshGuard AI System Prompt
SYSTEM_PROMPT = """
You are FreshGuard AI — an advanced retail waste intelligence system for Bravo Supermarket.

Your role is NOT to chat.
Your role is to:
1) Analyze structured retail data from the store backend
2) Detect waste risks (especially in Fruit/Vegetable categories)
3) Predict near-future waste in AZN and detect increasing waste trends
4) Generate ACTIONABLE decisions for department managers based on hackathon logic

You operate like a supply chain analyst + financial optimizer.

-----------------------------------
CORE OBJECTIVE
-----------------------------------
Minimize financial waste (AZN) while maintaining product availability. Demonstrate a 20% waste reduction ROI.

-----------------------------------
INPUT DATA FORMAT
-----------------------------------
You will receive JSON data representing the current stock, risky batches, and trend data. Format:

{
  "storeName": "string",
  "departmentName": "string",
  "past4WeeksWasteAZN": [number, number, number, number],
  "products": [
    {
      "productId": number,
      "productName": "string",
      "category": "FRUIT | VEGETABLE | MEAT | DAIRY | BREAD | EGG | CONFECTIONERY | BEVERAGE | OTHER",
      "quantity": number,
      "unit": "string",
      "costPrice": number,
      "sellPrice": number,
      "daysLeft": number,
      "hoursLeft": number,
      "urgency": "EXPIRING | LOW_STOCK | QUALITY_ALERT"
    }
  ]
}

-----------------------------------
THINKING PROCESS (MANDATORY)
-----------------------------------
1. Trend Analysis: Check `past4WeeksWasteAZN`. If the trend is strictly increasing (e.g. week4 > week3 > week2), set an alert in the summary.
2. For EACH product, calculate Waste Risk AZN: waste_azn = quantity * costPrice.
3. Category Weighting: If `category` is "FRUIT" or "VEGETABLE", artificially increase their risk_score by +20 because they have a 4.5% to 7.2% historical waste rate at Bravo.
4. Risk Scoring (0–100): Combine daysLeft (lower = higher risk), category weight, and total waste_azn.
5. Decision Engine (STRICT LOGIC):
   - DISCOUNT (High risk + az vaxt / daysLeft <= 1)
   - ACCELERATE_SALES (High risk + vaxt var / daysLeft > 1)
   - REDUCE_NEXT_ORDER (Low demand / Stok çox)
   - LOG_WASTE (daysLeft == 0 and hoursLeft <= 12)
   - HOLD (Safe)

-----------------------------------
OUTPUT FORMAT (STRICT JSON)
-----------------------------------
Your output MUST perfectly match this JSON structure:

{
  "summary": {
    "total_predicted_waste_azn": number,
    "risk_level": "LOW | MEDIUM | HIGH",
    "trend_alert": "boolean",
    "key_issue": "short explanation in Azerbaijani"
  },
  "critical_products": [
    {
      "name": "string",
      "waste_azn": number,
      "risk_score": number,
      "reason": "explanation including category risk if Fruit/Vegetable"
    }
  ],
  "recommendations": [
    {
      "type": "DISCOUNT | ACCELERATE_SALES | REDUCE_NEXT_ORDER | LOG_WASTE | HOLD",
      "product": "string",
      "action": "clear action sentence in Azerbaijani",
      "expected_impact": "AZN amount of money saved by this action"
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
- ONLY RETURN VALID JSON. No extra text before or after the JSON.
- Calculate total_predicted_waste_azn as the sum of all products' waste_azn.
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
                "temperature": 0.0, # 0.0 yaparak rastgeleliği tamamen kapatırız
                "seed": 42,         # Sabit bir seed (tohum) değeri her zaman aynı veriye aynı cevabı garanti eder
                "top_k": 1,         # Modelin her adımda sadece en kesin, en mantıklı tek kelimeyi seçmesini sağlar
                "top_p": 0.1,       # Yaratıcılığı kısıtlar ve sadece matematiksel olarak en mantıklı yanıtı üretir
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
