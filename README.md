# travel-assistant
旅行咨询助手
# Travel Inquiry Assistant

A smart travel inquiry assistant that extracts key information from customer messages and generates professional replies using AI.

**Live Demo**: https://travel-assistant-cqg7da7c8qmqt7weenpnge.streamlit.app/

## Features

- Extracts travel details: destination, duration, travel time, group size, budget
- Identifies trip type and intent
- Detects missing information and asks clarifying questions
- Generates professional, natural replies in English
- User provides own API key for privacy and cost control

## How It Works

1. User enters their DeepSeek API key in the sidebar
2. User types a travel inquiry (e.g., "7-day trip to Japan in October for 2 people, budget $3000")
3. AI analyzes the message and returns:
   - Structured extracted information
   - A professional reply or clarifying question
4. Missing fields are clearly identified

## Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| LLM | DeepSeek API |
| Framework | LangChain |
| Language | Python |

## Installation & Local Run

```bash
# Clone the repository
git clone https://github.com/kk6348653-bit/travel-assistant.git
cd travel-assistant

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
