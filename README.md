# 🚀 Multisource Search Agent

A powerful AI-driven **multisource research agent** that searches your query across **Google**, **Bing** (via [SerpAPI](https://serpapi.com/)), and **Reddit** (via [ScrapeCreators](https://app.scrapecreators.com/)).  
Each source is independently analyzed and synthesized into a final answer — combining **grounded truth** with **public sentiment**.

---

## 📑 Table of Contents
- [✨ Features](#-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [⚙️ Setup Instructions](#️-setup-instructions)


---

## ✨ Features
- 🧩 **Multistep search agent** → goes beyond a single query for deeper insights  
- 🔍 **Cross-source analysis** → synthesizes answers from Google, Bing, and Reddit  
- ⚡ **Groq-powered LLM inference** → extremely fast and efficient  
- 👨‍💻 **User-friendly experience** → live logs show which step is being executed (no more blind waiting!)  
- 🗣️ **Sentiment + factual grounding** → combines facts with public opinion  

---

## 🛠️ Tech Stack
- [LangGraph](https://github.com/langchain-ai/langgraph) – Orchestrating agent workflows  
- [LangChain](https://www.langchain.com/) – LLM integration  
- [Groq](https://groq.com/) – High-speed inference  
- [Streamlit](https://streamlit.io/) – Interactive web UI  

---

## ⚙️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/multisource-search-agent.git
   cd multisource-search-agent
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a .env file in the project root:**
   ```bash
   GROQ_API_KEY=your_groq_key
   SC_API_KEY=your_scrapecreators_key
   SERP_API_KEY=your_serpapi_key
   ```
   🔑 Get Your API Keys
   - [Groq API Key](https://groq.com/)  
   - [ScrapeCreators API Key](https://app.scrapecreators.com)  
   - [SerpAPI Key](https://serpapi.com/)  


3. **Run the application:**
   ```bash
   streamlit run main.py
   ```