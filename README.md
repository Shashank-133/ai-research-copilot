\# 🤖 AI Research Co-Pilot Pro



A production-ready AI research assistant built with a custom multi-agent architecture. Upload documents, search the web in real-time, and generate comprehensive research reports instantly.



!\[Python](https://img.shields.io/badge/python-3.8+-blue)

!\[Streamlit](https://img.shields.io/badge/streamlit-1.31+-red)

!\[License](https://img.shields.io/badge/license-MIT-green)



\## ✨ Features



\### 🤖 Custom Multi-Agent System

Built from scratch without frameworks - three specialized AI agents working together:

\- \*\*Researcher Agent\*\*: Gathers and organizes information from web searches

\- \*\*Analyst Agent\*\*: Synthesizes data and identifies key insights

\- \*\*Writer Agent\*\*: Creates polished, professional outputs



\### 🔍 Real-Time Web Search

\- DuckDuckGo API integration

\- Automatic source citation

\- Current information beyond AI training data



\### 📄 Document Intelligence

\- Upload and analyze PDF, DOCX, and TXT files

\- Extract insights from documents

\- Ask questions about uploaded content



\### 📊 Professional Reports

\- Export research as PDF or Word documents

\- Formatted with sources and citations

\- Complete multi-agent breakdown included



\### 📈 Analytics Dashboard

\- Track usage statistics

\- Interactive visualizations with Plotly

\- Query history and insights



\## 🚀 Quick Start



\### Prerequisites

\- Python 3.8 or higher

\- Nebius AI API key (\[Get one here](https://studio.nebius.ai/))



\### Installation



1\. \*\*Clone the repository\*\*

```bash

git clone https://github.com/yourusername/ai-research-copilot.git

cd ai-research-copilot

```



2\. \*\*Create virtual environment\*\*

```bash

python -m venv venv



\# Windows

venv\\Scripts\\activate



\# macOS/Linux

source venv/bin/activate

```



3\. \*\*Install dependencies\*\*

```bash

pip install -r requirements.txt

```



4\. \*\*Set up environment variables\*\*

```bash

\# Copy the example file

cp .env.example .env



\# Edit .env and add your Nebius API key

```



5\. \*\*Run the application\*\*

```bash

streamlit run main.py

```



The app will open in your browser at `http://localhost:8501`



\## 🎯 Usage



\### Basic Chat

1\. Type your question in the chat input

2\. AI responds with comprehensive answers

3\. View sources in expandable sections



\### Multi-Agent Mode

1\. Enable "Multi-Agent Mode" in sidebar

2\. Watch three specialized agents collaborate

3\. View each agent's contribution



\### Document Analysis

1\. Upload PDF, DOCX, or TXT in sidebar

2\. Ask questions about the document

3\. Get AI-powered insights



\### Export Reports

1\. Click export buttons after responses

2\. Choose PDF or DOCX format

3\. Professional formatted reports ready to use



\### Analytics

1\. Switch to "Analytics Dashboard" tab

2\. View usage statistics and trends

3\. Track research history



\## 🛠️ Tech Stack



\- \*\*Frontend\*\*: Streamlit

\- \*\*AI Models\*\*: Nebius AI API

&nbsp; - Llama 3.3 70B (Fast \& Balanced)

&nbsp; - DeepSeek V3 (Best Reasoning)

&nbsp; - Qwen3 235B (Ultra Large)

\- \*\*Architecture\*\*: Custom multi-agent system with RAG

\- \*\*Web Search\*\*: DuckDuckGo API

\- \*\*Document Processing\*\*: PyPDF2, python-docx

\- \*\*Report Generation\*\*: ReportLab, python-docx

\- \*\*Visualization\*\*: Plotly, Pandas



\## 🏗️ Project Structure

```

ai-research-copilot/

├── src/

│   ├── \_\_init\_\_.py

│   ├── config.py          # Configuration and settings

│   ├── search.py          # Web search functionality

│   ├── document.py        # Document processing

│   ├── export.py          # PDF/DOCX export

│   └── agents.py          # Multi-agent system

├── main.py                # Streamlit application

├── requirements.txt       # Python dependencies

├── .env.example          # Environment template

├── .gitignore            # Git ignore rules

└── README.md             # This file

```



\## 🏗️ Architecture

```

┌─────────────────────────────────────────┐

│      Streamlit Web Interface            │

├─────────────────────────────────────────┤

│                                         │

│  ┌──────────┐  ┌──────────┐  ┌───────┐  │

│  │Researcher│→ │  Analyst │→ │ Writer│  │

│  │  Agent   │  │  Agent   │  │ Agent │  │

│  └──────────┘  └──────────┘  └───────┘  │

│                                         │

├─────────────────────────────────────────┤

│ Web Search │ Document │ Export         │

├─────────────────────────────────────────┤

│         Nebius AI API Layer             │

└─────────────────────────────────────────┘

```



\## 💡 Key Technical Decisions



\### Why Custom Multi-Agent vs Framework?

\- \*\*Full Control\*\*: Complete control over agent orchestration

\- \*\*API Flexibility\*\*: Easy integration with any LLM provider

\- \*\*Lightweight\*\*: No framework overhead

\- \*\*Learning\*\*: Deeper understanding of multi-agent systems



\### Why RAG Architecture?

\- Combines retrieval (web search) with generation

\- Provides current, factual information

\- Goes beyond AI training data limitations



\### Why Modular Structure?

\- Clean separation of concerns

\- Easy to test and maintain

\- Scalable for future features

\- Professional code organization



\## 📋 Available Models



| Model | Size | Best For |

|-------|------|----------|

| Llama 3.3 70B | 70B | General queries, fast responses |

| DeepSeek V3 | Large | Complex reasoning, analysis |

| Qwen3 235B | 235B | Detailed research, comprehensive answers |



\## ⚙️ Configuration



\### Environment Variables

```bash

OPENAI\_API\_KEY=your\_nebius\_api\_key\_here

OPENAI\_API\_BASE=https://api.studio.nebius.ai/v1

```



\### Customizing Models



Edit `src/config.py` to add or modify available models:

```python

MODEL\_OPTIONS = {

&nbsp;   "Your Model Name": "model-identifier",

&nbsp;   # Add more models here

}

```



\## 🤝 Contributing



Contributions are welcome! Please feel free to submit a Pull Request.



1\. Fork the repository

2\. Create your feature branch (`git checkout -b feature/AmazingFeature`)

3\. Commit your changes (`git commit -m 'Add some AmazingFeature'`)

4\. Push to the branch (`git push origin feature/AmazingFeature`)

5\. Open a Pull Request



\## 📝 License



This project is licensed under the MIT License - see the \[LICENSE](LICENSE) file for details.



\## 🙏 Acknowledgments



\- \[Streamlit](https://streamlit.io/) - Amazing framework for rapid prototyping

\- \[Nebius AI](https://nebius.ai/) - Powerful AI model infrastructure

\- \[DuckDuckGo](https://duckduckgo.com/) - Privacy-focused search API



\## 🎯 Use Cases



\- 📚 \*\*Academic Research\*\*: Literature reviews and research synthesis

\- 💼 \*\*Business Intelligence\*\*: Market analysis and competitive research

\- ✍️ \*\*Content Creation\*\*: Research-backed content and articles

\- 📊 \*\*Data Analysis\*\*: Document analysis and insight extraction

\- 🎓 \*\*Learning\*\*: Educational research and study assistance



\## 🔮 Future Roadmap



\- \[ ] Add more AI model providers

\- \[ ] Implement conversation memory

\- \[ ] Add collaborative features

\- \[ ] Support for more document formats

\- \[ ] API endpoint for integrations

\- \[ ] Custom agent templates

\- \[ ] Multi-language support



\## 📧 Contact



\*\*Shashank Gupta\*\* - \[@yourtwitter](https://twitter.com/yourtwitter)



Project Link: \[https://github.com/Shashank-133/ai-research-copilot](https://github.com/Shashank-133/ai-research-copilot)



---



\*\*⭐ Star this repository if you find it helpful!\*\*



Built with ❤️ 

