# SmartTourGuideAgent

#### Multimodal AI Travel Assistant

## Project Goal

Smart TourGuide Agent is an intelligent travel assistant built using LangChain, it enables users to ask questions about cities, countries, weather, and even receive custom travel itineraries.<br> The system is designed to provide instant, accurate responses to user queries, such as "What can I visit in Paris in 2 days?" and provides the following features:

• **Conversational Responses:** The agent provides answers in a conversational style, engaging users with a natural flow of dialogue.

• **Speech Recognition:** The system supports both text and voice input, enabling hands-free interaction. Users can speak their questions, and the system will convert speech to text for processing.

• **Real-time Information:** By integrating with Wikipedia, OpenWeatherMap API, and OpenAI's GPT models, the agent generates real-time, relevant responses tailored to the user's travel-related queries.

• **Custom Travel Itineraries:** Users can ask for custom itineraries, and the agent will generate a fun, engaging schedule with details about places to visit, weather information, and travel recommendations.

## Architecture

1. **Speech Recognition:** Uses Google Speech-to-Text for converting speech input into text.

2. **LangChain Framework:** Handles text processing, splitting, and integration with external APIs (e.g., Wikipedia and OpenWeatherMap).

3. **Wikipedia API:** Uses WikipediaAPIWrapper to retrieve city and country details.

4. **Weather API:** Utilizes OpenWeatherMapAPIWrapper to fetch weather data.

5. **OpenAI:** Uses GPT models (gpt-3.5-turbo-instruct) to process queries and generate responses.

6. **FAISS Vector Store:** Stores and retrieves split documents for more efficient query handling.

7. **Memory:** Utilizes _ConversationBufferMemory_ from LangChain to maintain conversation context.

## Methodology

• **Data Retrieval:** The system uses Wikipedia’s public API to retrieve travel-related information. It also pulls current weather data from OpenWeatherMap’s API.<br>
• **Text Processing:** LangChain’s RecursiveCharacterTextSplitter is used to split large text documents into smaller chunks for better vector storage and retrieval.<br>
• **Vectorization:** FAISS is used to store the split documents in a vector store, which can then be queried by the agent.<br>
• **Model Integration:** OpenAI’s GPT model (GPT-3.5) is used to generate meaningful answers based on the user’s query, powered by a custom prompt template.<br>
• **Audio Integration:** Speech recognition is implemented using Google's speech-to-text API service. <br>

## Setup Instructions

1. **Python 3.8+** (Make sure you have Python installed).

2. Install the following dependencies:

   - `pip install -r requirements.txt`

3. Clone this repository:<br>

   ```bash
   git clone https://github.com/yourusername/smart-tour-guide-agent.git
   cd smart-tour-guide-agent

   ```

4. Set up environment variables: <br>
   Create a .env file in the root directory and add the following:
   OPENAI_API_KEY=your_openai_api_key<br>
   WEATHER_API_KEY=your_openweathermap_api_key<br>
   LANGSMITH_API_KEY=your_langsmith_api_key <br>
   Replace your_openai_api_key , your_openweathermap_api_key and your_langsmith_api_key with your actual API keys.

5. Ensure the pyttsx3 library is correctly configured for your operating system.<br>
   You may need to configure the pyttsx3 library depending on your operating system. Ensure it is working correctly for text-to-speech functionality.

6. Running the System:
   To start the SmartTourGuideAgent, run the following command:<br>
   python smart-tour-guide-agent.ipynb <br>
   This will launch the assistant, where the user can choose to interact with it via text or voice input.

## Repository Structure Overview

smart-tour-guide-agent/<br>
│<br>
├── Source Code/<br>
│ ├── smart-tour-guide-agent.ipynb<br>
│ └── requirements.txt # For development (Jupyter Notebook)<br>
│<br>
├── Deployment Code/<br>
│ ├── app.py # Streamlit Web App<br>
│ └── requirements.txt # For deployment (Streamlit app)<br>
│<br>
├── .env-example # API keys and secrets<br>
├── README.md # Project documentation<br>

## Configuration Details

### requirements.txt

This file lists all the dependencies needed to run the project. Here’s the content of `requirements.txt`:

speechrecognition==3.10.0<br>
langchain==0.1.13<br>
langchain-community==0.0.29<br>
langchain-openai==0.0.8<br>
langchain-core==0.1.33<br>
pyttsx3==2.90<br>
faiss-cpu==1.7.4<br>
python-dotenv==1.0.1<br>
openai==1.12.0 <br>
langsmith==0.1.20<br>
pyaudio==0.2.14<br>
pydub<br>
faiss-cpu<br>
tiktoken<br>
pyowm<br>
weaviate-client<br>
wikipedia<br>
duckduckgo-search<br>

### .env

You need to create a `.env` file in the project’s root directory with your API keys. <br> This file should look like this:<br>
OPENAI_API_KEY=your_openai_api_key
WEATHER_API_KEY=your_openweathermap_api_key
LANGSMITH_API_KEY=your_langsmith_api_key

Make sure to replace `your_openai_api_key`, `your_openweathermap_api_key` and  `your_langsmith_api_key` with your actual API keys.

## Usage Guide

Once the setup is complete, you can interact with the SmartTourGuideAgent in two ways:

1.  **Text Input**: When prompted, type your travel-related question, such as:

    - "Top attractions in paris?"
    - "What’s the weather in Rome?"
    - "Create a trip for china."

2.  **Audio Input**: When prompted, speak into the microphone, and the agent will listen to your question. The agent will then process the input and generate a response.

The agent responds to queries about: <br>
• **Cities**: Landmarks, activities, and attractions.<br>
• **Countries**: Famous places, cultural highlights, etc.<br>
• **Weather**: Current or forecasted weather information for a city or country.<br>
• **Itineraries**: Custom travel plans with emoji-based activities.<br>

## Presentation Materials

The slides used for the final presentation are available at the following link:

[View the presentation slides here](https://drive.google.com/drive/folders/19Uh2avPE9aWIMz_PcFDbJH2hveNSdvgd?usp=sharing)

**Good luck!**
