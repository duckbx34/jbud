import os
import streamlit as st
from datetime import datetime
import json
from pathlib import Path

# LangChain imports
from langchain_community.llms import Ollama
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.schema import Document


# Initialize Ollama
@st.cache_resource
def init_ollama():
    """Initialize Ollama LLM and embeddings"""
    try:
        llm = Ollama(
            model="gemma3",
            base_url="http://localhost:11434",
            temperature=0.7
        )
        
        embeddings = OllamaEmbeddings(
            model="nomic-embed-text",
            base_url="http://localhost:11434"
        )
        
        return llm, embeddings
    except Exception as e:
        st.error(f"❌ Error connecting to Ollama: {e}")
        st.error("💡 Make sure Ollama is running with: `ollama serve`")
        st.error("💡 And that gemma3 is installed with: `ollama pull gemma3`")
        return None, None

# Journal storage functions
def save_journal_entry(content, mood=None, tags=None):
    """Save a journal entry to local storage"""
    journal_dir = Path("journal_entries")
    journal_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now()
    filename = f"entry_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"
    
    entry = {
        "content": content,
        "timestamp": timestamp.isoformat(),
        "mood": mood,
        "tags": tags or [],
        "date": timestamp.strftime('%Y-%m-%d'),
        "time": timestamp.strftime('%H:%M')
    }
    
    with open(journal_dir / filename, 'w') as f:
        json.dump(entry, f, indent=2)
    
    return filename

def load_journal_entries():
    """Load all journal entries"""
    journal_dir = Path("journal_entries")
    if not journal_dir.exists():
        return []
    
    entries = []
    for file_path in journal_dir.glob("*.json"):
        try:
            with open(file_path, 'r') as f:
                entry = json.load(f)
                entry['filename'] = file_path.name
                entries.append(entry)
        except Exception as e:
            st.warning(f"⚠️ Error loading {file_path}: {e}")
    
    return sorted(entries, key=lambda x: x['timestamp'], reverse=True)

def create_vector_store(entries, embeddings):
    """Create vector store from journal entries"""
    if not entries:
        return None
    
    documents = []
    for entry in entries:
        # Create rich document content
        doc_content = f"""
        Date: {entry['date']} {entry['time']}
        Mood: {entry.get('mood', 'Not specified')}
        Tags: {', '.join(entry.get('tags', []))}
        
        Entry:
        {entry['content']}
        """
        
        doc = Document(
            page_content=doc_content,
            metadata={
                'date': entry['date'],
                'mood': entry.get('mood'),
                'tags': ', '.join(entry.get('tags', [])),
                'filename': entry.get('filename')
            }
        )
        documents.append(doc)
    
    # Split documents if they're too long
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(documents)
    
    # Create vector store
    try:
        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=embeddings,
            persist_directory="./journal_chroma_db"
        )
        return vectorstore
    except Exception as e:
        st.error(f"❌ Error creating vector store: {e}")
        return None

def get_journal_insights(query, vectorstore, llm):
    """Get insights from journal entries"""
    if not vectorstore:
        return "No journal entries found. Start by writing your first entry!", []
    
    # Create retrieval QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
        return_source_documents=True
    )
    
    # Enhanced prompt for better insights
    enhanced_query = f"""
    Based on the journal entries provided, please analyze and provide insights about: {query}

    Please analyze patterns, emotions, and experiences from the past entries.
    Provide practical advice and perspectives based on what has been written before.
    Be empathetic and supportive while being honest about patterns you notice.
    
    Focus on:
    1. What patterns do you see in the entries?
    2. How have similar situations been handled before?
    3. What practical advice can you give based on past experiences?
    4. What growth or changes do you notice over time?
    
    Use a warm, supportive tone as if you're a wise friend who has been following this person's journey.
    """
    
    try:
        result = qa_chain({"query": enhanced_query})
        return result["result"], result.get("source_documents", [])
    except Exception as e:
        return f"❌ Error getting insights: {e}", []

# Streamlit UI
def main():
    st.set_page_config(
        page_title="JBUD",
        page_icon="📝",
        layout="wide"
    )
    
    # Header
    st.title("📝 JBUD")
    st.subheader("Your Personal AI Journaling Assistant")
    
    # Info banner
    with st.expander("ℹ️ About JBUD"):
        st.write("""
        **JBUD** is your private AI journaling companion that runs completely on your local machine.
        
        - 🔒 **Complete Privacy**: All data stays on your computer
        - 🧠 **Personal Insights**: AI learns from YOUR journal entries
        - 📊 **Pattern Recognition**: Discover trends in your thoughts and moods
        - 💭 **Self Reflection**: Get perspective on your experiences and growth
        
        **How it works:**
        1. Write journal entries regularly
        2. After a few entries, ask questions about your patterns
        3. Get personalized insights based on your own experiences
        """)
    
    # Initialize Ollama
    llm, embeddings = init_ollama()
    if not llm or not embeddings:
        st.error("🛑 Cannot proceed without Ollama connection. Please check the setup instructions above.")
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.header("📊 Your Journal Stats")
        entries = load_journal_entries()
        st.metric("Total Entries", len(entries))
        
        if entries:
            recent_date = entries[0]['date']
            st.metric("Last Entry", recent_date)
            
            # Mood distribution
            moods = [e.get('mood') for e in entries if e.get('mood')]
            if moods:
                from collections import Counter
                mood_counts = Counter(moods)
                st.write("**Recent Moods:**")
                for mood, count in mood_counts.most_common(3):
                    st.write(f"• {mood}: {count}")
        
        st.write("---")
        st.write("**💡 Tips:**")
        st.write("• Write regularly for better insights")
        st.write("• Be honest and detailed in entries")
        st.write("• Try different question types")
        st.write("• Use tags to organize themes")
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs(["✍️ New Entry", "🔍 Ask Your Journal", "📚 Browse Entries"])
    
    with tab1:
        st.header("Write New Journal Entry")
        
        # Entry form
        with st.form("journal_entry"):
            entry_content = st.text_area(
                "What's on your mind today?",
                height=200,
                placeholder="Share your thoughts, feelings, experiences, challenges, victories, or anything that matters to you today..."
            )
            
            col1, col2 = st.columns(2)
            with col1:
                mood = st.selectbox(
                    "How are you feeling?",
                    ["", "😊 Great", "🙂 Good", "😐 Okay", "😔 Down", "😰 Stressed", "😡 Frustrated", "🤔 Contemplative", "😴 Tired", "🎉 Excited"]
                )
            
            with col2:
                tags_input = st.text_input(
                    "Tags (comma-separated)",
                    placeholder="work, relationships, goals, health, etc."
                )
            
            submitted = st.form_submit_button("💾 Save Entry", use_container_width=True)
            
            if submitted and entry_content.strip():
                tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
                filename = save_journal_entry(entry_content, mood, tags)
                st.success(f"✅ Entry saved successfully!")
                st.balloons()
                
                # Immediate insight
                st.subheader("🤖 Quick Reflection")
                reflection_prompt = f"""
                Someone just wrote this journal entry: "{entry_content}"
                
                Please provide a brief, supportive reflection on what they shared.
                Offer 1-2 insights or gentle observations about their thoughts/feelings.
                Be encouraging, empathetic, and supportive.
                Keep it concise but meaningful.
                """
                
                with st.spinner("Reflecting on your entry..."):
                    try:
                        reflection = llm(reflection_prompt)
                        st.info(f"💭 {reflection}")
                    except Exception as e:
                        st.error(f"❌ Error generating reflection: {e}")
    
    with tab2:
        st.header("Ask Your Journal")
        
        entries = load_journal_entries()
        if not entries:
            st.warning("📝 No journal entries yet. Write your first entry to get started!")
            st.info("💡 **Tip**: Write 3-5 entries before asking questions for better insights.")
        else:
            # Create vector store
            with st.spinner("🔍 Loading your journal entries..."):
                vectorstore = create_vector_store(entries, embeddings)
            
            if len(entries) < 3:
                st.info(f"📈 You have {len(entries)} entries. Consider writing a few more for richer insights!")
            
            # Query interface
            example_queries = [
                "How do I usually handle stress?",
                "What patterns do you see in my mood?",
                "What has been making me happy lately?",
                "How have I grown over the past month?",
                "What challenges do I face repeatedly?",
                "What are my main sources of motivation?",
                "When do I feel most confident?",
                "What activities improve my wellbeing?"
            ]
            
            st.write("**💡 Example questions you can ask:**")
            cols = st.columns(2)
            for i, query in enumerate(example_queries[:6]):
                col = cols[i % 2]
                with col:
                    if st.button(f"💬 {query}", key=f"example_{i}", use_container_width=True):
                        st.session_state.query = query
            
            query = st.text_input(
                "🤔 Ask your journal anything:",
                value=st.session_state.get('query', ''),
                placeholder="e.g., 'How do I usually handle difficult days?' or 'What makes me feel fulfilled?'"
            )
            
            if st.button("🔮 Get Insights", use_container_width=True) and query:
                with st.spinner("🧠 Analyzing your journal entries..."):
                    insights, sources = get_journal_insights(query, vectorstore, llm)
                    
                    st.subheader("💡 Insights from Your Journal")
                    st.write(insights)
                    
                    if sources:
                        with st.expander("📄 Source Entries Used"):
                            for i, doc in enumerate(sources[:3]):
                                st.write(f"**Entry {i+1}:**")
                                st.write(doc.page_content[:300] + "...")
                                st.write("---")
    
    with tab3:
        st.header("Browse Your Entries")
        
        entries = load_journal_entries()
        if not entries:
            st.info("📝 No journal entries yet. Start writing to see them here!")
        else:
            # Filters
            col1, col2, col3 = st.columns(3)
            with col1:
                all_moods = [e.get('mood', '') for e in entries if e.get('mood')]
                selected_mood = st.selectbox("Filter by mood:", ["All"] + list(set(all_moods)))
            
            with col2:
                all_tags = []
                for entry in entries:
                    all_tags.extend(entry.get('tags', []))
                selected_tag = st.selectbox("Filter by tag:", ["All"] + list(set(all_tags)))
            
            with col3:
                # Date range filter
                if entries:
                    dates = [datetime.fromisoformat(e['timestamp']).date() for e in entries]
                    min_date, max_date = min(dates), max(dates)
                    selected_date = st.date_input("Show entries from:", value=None)
            
            # Apply filters
            filtered_entries = entries
            if selected_mood != "All":
                filtered_entries = [e for e in filtered_entries if e.get('mood') == selected_mood]
            if selected_tag != "All":
                filtered_entries = [e for e in filtered_entries if selected_tag in e.get('tags', [])]
            if 'selected_date' in locals() and selected_date:
                filtered_entries = [e for e in filtered_entries if e['date'] >= str(selected_date)]
            
            st.write(f"📊 Showing **{len(filtered_entries)}** of **{len(entries)}** entries:")
            
            # Display entries
            for entry in filtered_entries[:20]:  # Show latest 20
                with st.expander(f"📅 {entry['date']} {entry['time']} - {entry.get('mood', '😐 No mood')}"):
                    st.write(entry['content'])
                    if entry.get('tags'):
                        st.write("🏷️ **Tags:** " + ", ".join(entry['tags']))
                    
                    # Entry stats
                    word_count = len(entry['content'].split())
                    st.caption(f"📝 {word_count} words • Created: {entry['date']} {entry['time']}")

if __name__ == "__main__":
    main()