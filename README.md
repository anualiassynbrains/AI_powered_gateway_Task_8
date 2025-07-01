# 🧠 AI Powered Gateway – Task 8

A FastAPI-based service integrating Groq’s Llama models and Redis for cost‑aware, API-key-based text summarization.

---

## 🌐 Features

- ✅ REST API endpoint (`/summarize`) that:
  - Accepts user input via POST
  - Uses **Groq Llama models** to:
    - Estimate cost (1–10)
    - Summarize the input text
  - Enforces **per-user rate limiting** using **Redis**, based on available credits

---

## 🏗️ Project Architecture

This project follows a **two-model "gatekeeper" architecture**:

### 1. **Cost Estimator** (`llama3-8b-8192`)
Acts as the **"gatekeeper"** by evaluating the complexity of the text and returning a numeric cost (between 1 and 10). This prevents overuse and filters expensive requests.

### 2. **Summarizer** (`llama3-70b-8192`)
Performs the **actual summarization** of the text, only if the user has enough credits (as validated by the gatekeeper logic).

---

## 🗃️ Role of Redis

- Redis is used for **stateful tracking** of **user credits**.
- Each request is tied to an `X-API-Key` header.
- Redis stores per-user balances using keys like: `user:<API-KEY>`.
- Default balance: `100 credits`.
- If the user has **enough credits**, Redis:
  - Deducts the estimated cost
  - Allows the request to continue
- If not, it returns a `429 Too Many Requests`.

---

## 🛠️ Prerequisites

- ✅ A working **Groq API Key**
- ✅ A **Redis instance** (local or free cloud-based)

---

## ⚙️ Setup Instructions

```bash
git clone https://github.com/yourusername/AI_powered_gateway_Task_8.git
```

```bash
cd your folder name
```
```bash
poetry add fastapi uvicorn redis python-dotenv groq
```
```bash
poetry shell
```
### Prerequisites


-  free cloud Redis instance
- Groq API key

### .env File Configuration

Create a .env file in your root directory:


### How to run
```bash
cd src
cd costmanagement
uvicorn main:app--reload
```

### How it Works

Cost Estimation

costestimator.py sends the input text to Groq’s Llama to receive a numeric cost (1–10).

  

Rate Limiting

rate\_limiter.py checks the user’s credit balance in Redis (default: 100), deducts the cost, or returns a 429 error if insufficient.

  

Summarization

summarizer.py uses Llama to generate a clear, concise summary of the input.