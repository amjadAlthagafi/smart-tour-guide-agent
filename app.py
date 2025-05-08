import os 
import streamlit as st
from  langsmith import utils
import speech_recognition as sr
from langchain.agents import Tool
from langchain.schema import Document
from langchain_openai import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.agents import initialize_agent
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.utilities import OpenWeatherMapAPIWrapper, WikipediaAPIWrapper, DuckDuckGoSearchAPIWrapper

from dotenv import load_dotenv
_ = load_dotenv()

OPENAI_API_KEY  = os.getenv('OPENAI_API_KEY')
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"]="https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"]="Travel Assistant"

# Setup recognizer and APIs
recognizer = sr.Recognizer()
weather_api = OpenWeatherMapAPIWrapper(openweathermap_api_key=os.getenv("OPENWEATHERMAP_API_KEY"))  # API key required
wiki_api = WikipediaAPIWrapper()
duck_api = DuckDuckGoSearchAPIWrapper()
embed = OpenAIEmbeddings(model='text-embedding-ada-002') 
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

# Wikipidia retriever system
def retriever_tool(split_docs,query):
    
    # creates a FAISS vector store for similarity search
    vectorstore = FAISS.from_documents(split_docs, embed)
    retriever = vectorstore.as_retriever()
    results = retriever.get_relevant_documents(query)
    return "\n".join([doc.page_content for doc in results])

# Wikipidia search system 
def wiki_search(query):
    try:
        data = wiki_api.load(query)
        if not data:
            return "i didn't find any information at wikipedia"
        split_docs = splitter.split_documents(data)
        return retriever_tool(split_docs, query)
    except Exception as e:
        return f"error! {str(e)}"

# document identification function
def docs(article):
  return Document(
      page_content=article['snippet'],
      metadata={"title": article['title']}
  )


# DuckDuckGo search system 
def ddg_search(query):
    data = duck_api.results(query,10)
    documents = []
    for raw in data:
     documents.append(docs(raw))
    split_docs = splitter.split_documents(documents)
 
    return retriever_tool(split_docs, query)

listening_placeholder = st.empty() 
# Define the listen_to_user function
def listen_to_user(timeout=3, phrase_time_limit=5):
    """Convert speech to text with error handling"""
    try:
        with sr.Microphone() as source:
            print("\n🎤 Listening... (Speak now)")
            audio = recognizer.listen(source, timeout=timeout)
        return recognizer.recognize_google(audio)
    except sr.WaitTimeoutError:
        print("⌛ No speech detected, please try again!")
        return ""
    except Exception as e:
        print(f"🔇 : {str(e)}. Try speaking again.")
        return ""

# Define the prompt for the agent
tour_guide_prompt = PromptTemplate(
    input_variables=["query"],
    template="""
    You are a SmartTourGuideAgent. Your task is to help users with their travel-related questions.
    If the user asks about a city or country, provide them with relevant details about it.
    If the user asks for a trip plan, create a basic itinerary for them.
    Answer questions with relevant emojis to make the answers more engaging and fun. 
    Query: {query}
    Answer:
    """
)

# Define the tools (API wrappers)
tools = [
    Tool(
        name="TravelInfoRetriever",
        func=wiki_search,
        description=(
            "Retrieve information about a city or country. "
            "For cities, mention landmarks, weather, or activities with emojis. "
            "For countries, mention famous attractions or cultural highlights with emojis."
        ),
    ),
    Tool(
    name="WebSearch",
    func=ddg_search,
    description=(
        "Use this to search general travel topics or if Wikipedia doesn't return results. "
        "Can return articles, facts, or general information. Great for cities not in Wikipedia!"
        ),
    ),
    Tool(
        name='Weather',
        func=weather_api.run,
        description=(
            "Get weather information for any city or travel destination."
        ),
    ),
]

# Initialize agent with memory
memory = ConversationBufferMemory(memory_key="chat_history")

conversational_agent = initialize_agent(
    agent="conversational-react-description",
    tools=tools,
    llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"),  # Using a compatible model for chat completions
    verbose=True,
    agent_kwargs={"prompt": tour_guide_prompt},
    memory=memory,
    handle_parsing_errors=True,
)


st.title("My Smart TourGuide 💬")
st.subheader("🚀 Adventures Around the World")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


query = None
input_user = ""
agent = ""

# Toggle for Audio or Text
on = st.toggle("🎙️ Use Voice Input")
if on:
    if st.button("Start Recording"):
        listening_placeholder = st.write("🎤 Listening...") 
        query = listen_to_user()  # make sure this function returns a valid string
        if query:
            listening_placeholder.success("✅ Voice input received!") 
            input_user = query
            listening_placeholder.empty()          
            result = conversational_agent.run(query)
            agent = result
else:
    query = st.chat_input("Ask Anything ✍️ ")
    if query:
        input_user = query
        result = conversational_agent.run(query)
        agent = result

# Show the interaction in chat format
if query:
    st.chat_message("user").markdown(input_user)
    st.chat_message("assistant").markdown(agent)
    # Optionally: Save to session state for chat history
    st.session_state.messages.append({"role": "user", "content": input_user})
    st.session_state.messages.append({"role": "assistant", "content": agent})

with st.sidebar:
    st.title("Travel Assistant Agent 🌍")
    st.subheader("Your Smart Travel Companion")
    st.markdown(
        """
        Meet your **AI-powered Travel Assistant Agent** – your all-in-one solution for discovering new cities and planning smarter trips.

         **What it does**✨
        - Gives you a short overview of any city you ask about
        - Recommends top tourist attractions
        - Provides live weather updates
        - Checks for nearby airports and informs you if travel access is limited
        - Supports both text and voice interaction

        🔧 **Powered by**:
        - [Wikipedia API](https://www.mediawiki.org/wiki/API:Main_page) for city facts and history
        - [DuckDuckGo API](https://duckduckgo.com/api) for additional insights
        - [OpenWeatherMap API](https://openweathermap.org/api) for real-time weather

        Perfect for travelers, trip planners, and anyone curious about the world 🌐✈️
        """
        
    )
    st.markdown("**Travel Tip**: When you visit a new place, don’t forget to try the local food! 🌮🍣")
