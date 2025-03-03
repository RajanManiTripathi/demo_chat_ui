# AI Chat Assistant - Multi-Page Streamlit App

A comprehensive AI chat assistant built with Streamlit that supports multiple chat rooms, AI models, and conversation history.

## Features

- **Multiple Chat Rooms**: Create and manage different chat rooms for various topics
- **AI Model Selection**: Choose from GPT-4, GPT-3.5, Claude, and more
- **Chat History**: Save and review past conversations
- **Cost Tracking**: Monitor token usage and associated costs
- **Saved Prompts**: Store and reuse your favorite prompts
- **User Settings**: Customize your experience with themes and preferences

## Project Structure

```
/ai_assistant
│── app.py                # Main entry point
│── config.yaml           # Configuration file
│── requirements.txt      # Python dependencies
│── utils.py              # Helper functions
│── /pages
│   ├── Home.py           # Welcome page
│   ├── Chat.py           # Chat interface
│   ├── Rooms.py          # Room management
│   ├── Settings.py       # User settings
```

## Getting Started

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   streamlit run app.py
   ```

3. Open your browser and navigate to the provided URL (typically http://localhost:8501)

## Usage

- **Home**: View welcome information and quick access to features
- **Chat**: Interact with AI models in your selected room
- **Rooms**: Create and manage different chat rooms
- **Settings**: Configure AI models, user preferences, and view usage statistics

## Note

This is a demonstration app that simulates AI responses. In a production environment, you would connect to actual AI APIs like OpenAI or Anthropic.