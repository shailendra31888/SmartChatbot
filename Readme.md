# 🤖 Smart Multi-Source Chatbot (FastAPI + LangGraph + LangChain)

This project is a modular, API-driven chatbot system powered by **FastAPI**, **LangChain**, and **LangGraph**, capable of intelligently routing user queries to different data sources and responding with relevant answers. It includes chat memory for contextual understanding and dynamic routing based on question classification.

---

## 🚀 Features

- 📊 **Classify Queries** into categories: `Trades`, `News`, `LLM`, `FMP Data`, `Google Search`
- 🔍 Integrates with multiple APIs:
  - Google Search
  - News API
  - Financial Modeling Prep (FMP)
  - LLM (GROQ or others)
- 🧠 **Chat Memory Support** using LangChain memory
- 🧭 **LangGraph Pipeline** to route and manage query flow
- 🧩 Clean, modular code structure for scalability

---

## 🗂️ Folder Structure

your_project/
│
├── app/
│   ├── main.py                          ← FastAPI entry point (starts the app)
│
│   ├── api/                             ← API route layer
│   │   └── chatbot.py                   ← Route that receives user question and triggers LangGraph pipeline
│
│   ├── services/                        ← All core functionalities and APIs
│   │   ├── classifier.py                ← classify_with_llm → categorizes the input
│   │   ├── google_search.py            ← google_search function
│   │   ├── news_search.py              ← search_news function
│   │   ├── stock_data.py               ← search function for stock data (FMP)
│   │   └── llm_response.py             ← get_answer_from_groq for LLM-based responses
│
│   ├── memory/                          ← Chat memory handling
│   │   ├── memory_manager.py           ← save_to_memory, was_question_asked_before, etc.
│   │   └── contextual_responder.py     ← check_contextual_and_respond logic
│
│   ├── pipeline/                        ← LangGraph pipeline components
│   │   ├── router.py                   ← route_by_category logic (which node to trigger)
│   │   └── graph.py                    ← Complete LangGraph pipeline setup and node definitions
│
│   ├── models/                          ← Pydantic schemas for request/response (optional, clean structure)
│   │   └── chatbot_schema.py           
│
│   ├── core/                            ← Config, env loading, constants
│   │   ├── config.py                   
│   │   └── utils.py                    
│
├── requirements.txt
├── .env                                 ← API keys and secrets
└── README.md

install all dependencies 
pip install -r requirements.txt
