# FreshGuard AI 🍃

FreshGuard AI is an advanced retail waste intelligence system that uses a local AI model (Mistral via Ollama) to analyze structured retail supply chain data. It operates like a financial optimizer and supply chain analyst to predict, detect, and reduce financial waste while maintaining optimal stock availability.

## 🚀 Features

- **Predictive Waste Analysis**: Uses historical sales, expiry dates, and external factors (e.g., weather, footfall index) to predict near-future product waste.
- **Actionable Recommendations**: Doesn't just give generic advice. Recommends specific, quantified actions such as Markdown percentages, Reorders, or Redistributions.
- **100% Local Privacy**: Runs entirely on your local machine using the open-weight **Mistral** model. No store data is sent to external clouds.
- **GPU Accelerated**: Configured to utilize CUDA cores (e.g., RTX 4060 Ti) to provide lightning-fast analytical responses.
- **Modern Dashboard**: Features a sleek, dark-mode, glassmorphism UI to easily interact with the AI and view intelligence reports.

## 🛠️ Prerequisites

Before running this project, you must have:
1. **Python 3.8+** installed.
2. [Ollama](https://ollama.com/) installed and running locally.
3. The Mistral model downloaded via Ollama. 
   - Open your terminal and run: `ollama run mistral`

## 📦 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/maqa817/AI_Agent.git
   cd AI_Agent
   ```
2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🖥️ Running the System

You can start the server effortlessly using the provided batch script:
1. Ensure your Ollama app is running in the background.
2. Double-click the **`start_server.bat`** file.
3. The script will automatically launch the FastAPI backend and open your browser to the FreshGuard Dashboard (`http://127.0.0.1:8000`).

Alternatively, you can start the server manually via terminal:
```bash
python main.py
```

## 🧠 How the AI Works

The AI is strictly structured to receive JSON payloads representing daily store inventory and external conditions. It processes each product through a 5-step logic flow:
1. **Demand Estimation**
2. **Expiry Risk Calculation**
3. **Financial Waste Calculation (AZN)**
4. **Risk Scoring (0-100)**
5. **Decision Engine (Markdown, Hold, Reorder, Redistribute, Alert)**

The AI's response is always formatted in strict JSON, which is automatically decoded and beautifully rendered by the web dashboard.
