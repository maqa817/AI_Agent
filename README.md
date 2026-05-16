# FreshGuard AI 🍃

FreshGuard AI is an advanced retail waste intelligence system that uses a local AI model (Mistral via Ollama) to analyze structured retail supply chain data. Built specifically for **PASHA Hackathon 6.0**, it operates as an analytical microservice that integrates seamlessly with a Spring Boot backend and an Android mobile app.

## 🚀 Key Features

- **Predictive Waste Analysis**: Uses historical data, expiry dates, and stock quantity to predict near-future product waste in exact AZN.
- **Trend Detection**: Analyzes the last 4 weeks of waste data to alert managers if the waste trend is increasing.
- **Category Weighting**: Automatically assigns +20 higher risk scores to high-waste categories like **FRUIT** and **VEGETABLE** to focus on the highest impact areas.
- **Hackathon-Specific Action Engine**: Provides specific, quantified actions based on precise logic:
  - `DISCOUNT` (If risk is high and days left <= 1)
  - `ACCELERATE_SALES` (If risk is high but there is still time)
  - `REDUCE_NEXT_ORDER` (If demand is low and stock is high)
  - `LOG_WASTE` (If the product has expired)
- **100% Deterministic Local Privacy**: Runs entirely on your local machine using the open-weight **Mistral** model. Seed and Temperature are set to 0 to ensure mathematically deterministic output.
- **GPU Accelerated**: Configured to utilize CUDA cores to provide lightning-fast analytical responses.

## 🛠️ Prerequisites

Before running this project, you must have:
1. **Python 3.8+** installed.
2. [Ollama](https://ollama.com/) installed and running locally.
3. The Mistral model downloaded via Ollama: `ollama run mistral`

## 📦 Installation & Running

1. Clone this repository:
   ```bash
   git clone https://github.com/maqa817/AI_Agent.git
   cd AI_Agent
   ```
2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure your Ollama app is running in the background.
4. Double-click the **`start_server.bat`** file. The backend will start on `http://127.0.0.1:8000`.

## 🏗️ Microservices Architecture

FreshGuard uses a Microservices approach. This Python/FastAPI server is just the "Analytical Brain".
- **The Spring Boot Backend** is the Orchestrator. It fetches data from the database, constructs the JSON payload, and sends an internal POST request to this Python AI server.
- **The Android App** is the Client. It requests analysis from Spring Boot and displays the results to the Department Head.

The AI server accepts JSON payloads at `POST /api/analyze` and returns a structured JSON response with a risk summary, critical products, and actionable recommendations.
