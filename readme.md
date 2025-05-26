# JBUD 

**Local, Safe & Secure Personal AI Journaling Assistant**

https://github.com/user-attachments/assets/b5fa60b4-7f7b-4530-a19e-0151d0a21fde

JBUD is a **completely local, privacy-first** AI-powered journaling application that runs entirely on your computer. No cloud services, no data sharing, no privacy concerns - just you and your thoughts, enhanced by AI that learns from YOUR unique experiences.

Write your thoughts, reflect on your experiences, and get personalized insights based on your own journal entries - all while keeping your most personal data completely private and secure on your own machine.




## ✨ Features

- **📝 Smart Journaling**: Write entries with mood tracking and tags
- **🔍 AI Insights**: Ask questions about your past entries and get personalized advice
- **📊 Pattern Recognition**: Discover trends in your thoughts, moods, and experiences
- **🔒 Complete Privacy**: Everything runs locally - no cloud, no data sharing
- **🎯 Personal Growth**: Track your emotional journey and personal development
- **🏷️ Organized**: Filter entries by mood, tags, and dates

## 🔒 Privacy First

- **100% Local**: Uses Ollama for local AI processing
- **No Cloud Dependencies**: All data stays on your machine
- **No API Keys**: No external services required
- **Encrypted Storage**: Your journal entries are stored locally as JSON files

## 🚀 Quick Start

### Prerequisites

1. **Install Ollama** from [ollama.ai](https://ollama.ai)
2. **Pull Gemma 3 model**:
   ```bash
   ollama pull gemma3
   ```
3. **Start Ollama server**:
   ```bash
   ollama serve
   ```

### Installation

1. **Install Ollama and AI Models**:
   ```bash
   # Install Ollama (visit https://ollama.ai for your OS)
   # Then install required models:
   ollama pull gemma3          # Main chat model
   ollama pull nomic-embed-text # Embedding model for vector search
   
   # Start Ollama server (keep this running)
   ollama serve
   ```

2. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/jbud.git
   cd jbud
   ```

3. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install streamlit langchain langchain-community chromadb ollama-python
   ```

5. **Run JBUD**:
   ```bash
   streamlit run jbud.py
   ```

6. **Open your browser** to `http://localhost:8501`

## 📖 How to Use

### 1. Write Your First Entry
- Go to the "✍️ New Entry" tab
- Write about your day, thoughts, or feelings
- Add a mood and tags for better organization
- Get immediate AI reflection on your entry

### 2. Build Your Journal
- Write regularly for a few days/weeks
- The more you write, the better insights you'll get
- JBUD learns from YOUR unique experiences and patterns

### 3. Ask Your Journal
- Switch to "🔍 Ask Journal" tab
- Ask questions like:
  - "How do I usually handle stress?"
  - "What patterns do you see in my mood?"
  - "What has been making me happy lately?"
  - "How have I grown over time?"
- Get insights based on your actual journal entries

### 4. Browse and Reflect
- Use "📚 Browse Entries" to review past entries
- Filter by mood, tags, or dates
- Track your emotional journey over time

## 🎯 Example Questions to Ask

- **Emotional Patterns**: "What triggers my anxiety?" or "When am I happiest?"
- **Problem Solving**: "How did I handle similar challenges before?"
- **Growth Tracking**: "What progress have I made on my goals?"
- **Relationship Insights**: "How do I typically resolve conflicts?"
- **Habit Analysis**: "What activities improve my mood most?"

## 🛠️ Technical Details

### Built With
- **Streamlit**: Web interface
- **LangChain**: AI orchestration and RAG implementation
- **Ollama**: Local LLM inference with Gemma 3
- **ChromaDB**: Vector database for semantic search
- **Gemma 3**: Latest Google language model for insights

### Architecture
```
Your Journal Entries → Vector Database → AI Analysis → Personalized Insights
                   ↘                                ↗
                    Local Storage (Privacy Preserved)
```

### Project Structure
```
jbud/
├── jbud.py                   # Main application
├── journal_entries/          # Your journal entries (auto-created)
├── journal_chroma_db/        # Vector database (auto-created)
├── venv/                     # Virtual environment
└── README.md                 # This file
```

## ⚙️ Configuration

### Changing AI Models
Edit the `init_ollama()` function to use different models:
```python
llm = Ollama(
    model="llama3.3",  # or "mistral", "codellama", etc.
    base_url="http://localhost:11434"
)
```

### Customizing Insights
Modify the prompts in `get_journal_insights()` function to change how JBUD analyzes your entries.

## 🔧 Troubleshooting

### "Error connecting to Ollama"
- Ensure Ollama is running: `ollama serve`
- Check if Gemma 3 is installed: `ollama list`
- Verify Ollama is accessible: `curl http://localhost:11434/api/tags`

### "No journal entries found"
- Write a few entries first before asking questions
- Entries are automatically saved in `journal_entries/` folder

### Slow Performance
- Use a smaller model like `gemma3:8b` instead of larger variants
- Ensure sufficient RAM (8GB+ recommended)
- Close other resource-intensive applications

### Dependencies Issues
- Ensure virtual environment is activated: `source venv/bin/activate`
- Update pip: `pip install --upgrade pip`
- Reinstall packages: `pip install -r requirements.txt`

## 🤝 Contributing

We welcome contributions! Here are ways you can help:

- **Bug Reports**: Open an issue with details about the problem
- **Feature Requests**: Suggest new features or improvements
- **Code Contributions**: Submit pull requests with enhancements
- **Documentation**: Help improve setup instructions and usage guides

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Submit a pull request with a clear description

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Roadmap

- [ ] Export journal to PDF/Markdown
- [ ] Weekly/monthly summary reports
- [ ] Mood tracking graphs and analytics
- [ ] Voice-to-text entry support
- [ ] Mobile-responsive design
- [ ] Plugin system for custom integrations
- [ ] Encryption for sensitive entries
- [ ] Multi-language support

## 💡 Why JBUD?

**Privacy-First**: Your thoughts are personal. JBUD ensures they stay that way by running everything locally.

**Personalized**: Unlike generic AI assistants, JBUD learns from YOUR experiences and provides insights based on YOUR patterns.

**Open Source**: Transparent, customizable, and community-driven development.

**Practical**: Not just a diary - get actionable insights to improve your mental health and personal growth.

## 🤗 Community

- **GitHub Issues**: Report bugs or request features
- **Discussions**: Share your experiences and tips
- **Star the repo**: If JBUD helps you, give us a star! ⭐

## ⚠️ Disclaimer

JBUD is a personal development tool and not a replacement for professional mental health care. If you're experiencing serious mental health issues, please consult with a qualified healthcare professional.

---

**Made with ❤️ for personal growth and privacy**

*Start your journey of self-reflection today. Your future self will thank you.*
