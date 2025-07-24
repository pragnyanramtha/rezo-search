# Rezo Search: A Smart, AI-Powered Search API

Rezo Search is a powerful meta-search API that aggregates results from Google, Tavily, and other sources. It then uses the Google Gemini 2.5 Flash model to intelligently process, rank, and summarize the information, providing users with context-aware and relevant search experiences.

**Live Demo URL:** [https://rezo-search.onrender.com](https://rezo-search.onrender.com)

## ✨ Features

-   **Multi-Source Aggregation**: Fetches results from multiple search providers in parallel for comprehensive coverage.
-   **Intelligent Deduplication**: Combines and removes duplicate URLs for a clean, unique list of results.
-   **Four Powerful Modes**:
    1.  **Default Mode**: Provides a complete AI-generated summary and a list of the top 5 ranked links.
    2.  **Summary-Only Mode**: Delivers a quick, concise AI-generated paragraph summarizing the topic.
    3.  **Links-Only Mode**: Returns a clean JSON list of ranked, relevant URLs for exploration.
    4.  **Conversational Mode**: Remembers the context of your search, allowing you to ask follow-up questions.
-   **AI-Powered Ranking**: Uses Gemini to rank search results based on their relevance to the user's query.
-   **Context-Aware Follow-ups**: Intelligently rewrites search queries in conversational mode to find answers to follow-up questions.
-   **Easy Deployment**: Ready to be deployed on any modern PaaS like Render or Heroku.

## 🚀 API Usage

The API has a single endpoint: `/search`. Behavior is controlled using the `query` and `mode` URL parameters.

**Base URL**: `https://rezo-search.onrender.com`

---

### 1. Default Mode

Provides a comprehensive overview with an AI summary and ranked links. Omit the `mode` parameter to use this.

**Request:**
```bash
curl "https://rezo-search.onrender.com/search?query=impact+of+quantum+computing+on+cybersecurity"
```

**Example Response:**
```json
{
  "summary": "Quantum computing poses a significant threat to current cybersecurity protocols...",
  "ranked_results": [
    {
      "rank": 1,
      "title": "Quantum Computing and Cybersecurity | NIST",
      "text": "This official resource from NIST provides a foundational overview of the risks...",
      "url": "https://www.nist.gov/..."
    }
  ]
}
```

---

### 2. Summary-Only Mode

Returns a single JSON object with a concise summary.

-   `mode=summary`

**Request:**
```bash
curl "https://rezo-search.onrender.com/search?query=explain+the+concept+of+blockchain&mode=summary"
```

**Example Response:**
```json
{
  "summary": "A blockchain is a decentralized, distributed, and immutable digital ledger..."
}
```

---

### 3. Links-Only Mode

Returns a JSON object containing a list of ranked, relevant links.

-   `mode=links`

**Request:**
```bash
curl "https://rezo-search.onrender.com/search?query=best+open+source+alternatives+to+photoshop&mode=links"
```

**Example Response:**
```json
{
  "ranked_results": [
    {
      "rank": 1,
      "title": "GIMP - GNU Image Manipulation Program",
      "text": "GIMP is the most well-known and powerful open-source alternative...",
      "url": "https://www.gimp.org/"
    }
  ]
}
```

---

### 4. Conversational Mode

Allows for follow-up questions. This requires a client that supports cookies (like a web browser or `curl` with a cookie jar).

-   `mode=conversation`

**Turn 1: Initial Question**
```bash
# The -c flag saves cookies to a file for the next request
curl -c cookies.txt "https://rezo-search.onrender.com/search?query=what+are+the+main+features+of+the+rust+programming+language&mode=conversation"
```

**Turn 2: Follow-up Question**
```bash
# The -b flag sends the saved cookies, maintaining context
curl -b cookies.txt "https://rezo-search.onrender.com/search?query=tell+me+more+about+its+ownership+model&mode=conversation"
```
The API will understand you are still asking about Rust and provide a specific answer about its ownership system.

## 🛠️ Technology Stack

-   **Backend**: Flask, Gunicorn
-   **AI Model**: Google Gemini 1.5 Flash
-   **Search APIs**:
    -   Google Custom Search API
    -   Tavily Search API
    -   SearchApi.io
-   **Deployment**: Render

## ⚙️ Local Setup and Installation

To run this project on your own machine, follow these steps.

### Prerequisites

-   Python 3.8+
-   Git

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/rezo-search.git
cd rezo-search
```

### 2. Set Up a Virtual Environment

```bash
# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

You **must** create a `.env` file in the root directory to store your API keys. Copy the format from `.env.example`.

Create a file named `.env` and add the following, replacing the placeholder text with your actual keys:

```
# Google APIs
GOOGLE_API_KEY="AIzaSy..."
GOOGLE_CSE_ID="your_custom_search_engine_id"
GEMINI_API_KEY="AIzaSy..."

# Other Search APIs
TAVILY_API_KEY="tvly-..."
SEARCHAPI_IO_API_KEY="your_searchapi_key"

# Flask
FLASK_SECRET_KEY="generate_a_strong_random_string_here_for_sessions"
```

### 5. Run the Application

```bash
flask run
```

The application will be available at `http://127.0.0.1:5000`.

## 🚀 Deployment

This application is configured for easy deployment on [Render](https://render.com/).

1.  Push your code to a GitHub repository.
2.  Create a new "Web Service" on Render and connect it to your repository.
3.  Use the following settings:
    -   **Build Command**: `pip install -r requirements.txt`
    -   **Start Command**: `gunicorn --workers 4 --bind 0.0.0.0:$PORT app:app`
4.  Add all the variables from your `.env` file to the "Environment" section in the Render dashboard.

Render will automatically deploy your application.

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
