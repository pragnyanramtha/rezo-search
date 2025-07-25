import os
import json
import requests
from flask import Flask, request, jsonify, session, render_template
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

from googleapiclient.discovery import build as google_build
import google.generativeai as genai
from tavily import TavilyClient

# --- INITIALIZATION ---
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "a-default-secret-key-for-dev")

# --- API CLIENT SETUP ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
SEARCHAPI_IO_API_KEY = os.getenv("SEARCHAPI_IO_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-2.5-flash')


@app.route('/')
def index():
    """Serves the landing page."""
    return render_template('index.html')

def search_google(query):
    try:
        service = google_build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
        res = service.cse().list(q=query, cx=GOOGLE_CSE_ID, num=5).execute()
        return [{"title": i.get('title'), "text": i.get('snippet'), "url": i.get('link')} for i in res.get('items', [])]
    except Exception as e: print(f"Google Search Error: {e}"); return []

def search_tavily(query):
    try:
        res = tavily_client.search(query=query, search_depth="basic", max_results=5)
        return [{"title": i.get('title'), "text": i.get('content'), "url": i.get('url')} for i in res.get('results', [])]
    except Exception as e: print(f"Tavily Search Error: {e}"); return []

def search_searchapi_io(query):
    url = "https://www.searchapi.io/api/v1/search"
    params = {"engine": "google", "q": query, "api_key": SEARCHAPI_IO_API_KEY, "num": 5}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return [{"title": i.get('title'), "text": i.get('snippet'), "url": i.get('link')} for i in data.get('organic_results', [])]
    except Exception as e: print(f"SearchApi.io Error: {e}"); return []



def run_parallel_searches(query):
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(f, query) for f in [search_google, search_tavily, search_searchapi_io]]
        return [future.result() for future in futures]

def deduplicate_results(results_list):
    all_results, seen_urls = [], set()
    for results in results_list:
        for result in results:
            if result and result.get('url') and result['url'] not in seen_urls:
                all_results.append(result); seen_urls.add(result['url'])
    return all_results

def clean_gemini_json_response(text):
    try: return json.loads(text.strip().lstrip("```json").rstrip("```"))
    except Exception: return {"error": "Failed to parse AI model JSON response.", "raw_response": text}

def generate_ai_response(prompt):
    try: response = gemini_model.generate_content(prompt); return clean_gemini_json_response(response.text)
    except Exception as e: return {"error": f"Gemini API Error: {e}"}

def get_ai_summary(q, r): return generate_ai_response(f'Summarize results for "{q}". JSON output: {{"summary": "..."}}. Results: {json.dumps(r)}')
def get_ranked_links(q, r): return generate_ai_response(f'Rank top 5 results for "{q}". JSON output: {{"ranked_results": [...]}}. Results: {json.dumps(r)}')
def get_contextual_query(c, f): return gemini_model.generate_content(f'Previous context: "{c if c else "None"}". Follow-up: "{f}". Create a new search query.').text.strip()
def get_conversational_answer(c, f, r): return generate_ai_response(f'Context: "{c if c else "New conversation."}". User asks: "{f}". Give a conversational answer as JSON with "answer" and "relevant_urls". Results: {json.dumps(r)}')


# --- FLASK API ROUTE (REWRITTEN LOGIC) ---

@app.route('/search', methods=['GET'])
def search_api():
    query = request.args.get('query')

    mode = request.args.get('mode', 'default').lower()

    output_format = request.args.get('output', 'json').lower()

    if not query:
        return jsonify({"error": "A 'query' parameter is required."}), 400

    response_data = None

    response_data = None

    if mode == 'summary':
        results = deduplicate_results(run_parallel_searches(query))
        if not results: response_data = {"error": "Could not fetch search results."}
        else: response_data = get_ai_summary(query, results)

    elif mode == 'links':
        results = deduplicate_results(run_parallel_searches(query))
        if not results: response_data = {"error": "Could not fetch search results."}
        else: response_data = get_ranked_links(query, results)

    elif mode == 'conversation':
        chat_context = session.get('chat_context', '')
        new_search_query = get_contextual_query(chat_context, query)
        results = deduplicate_results(run_parallel_searches(new_search_query))
        if not results: response_data = {"error": "Could not fetch results for follow-up."}
        else:
            response_data = get_conversational_answer(chat_context, query, results)
            if 'answer' in response_data:
                session['chat_context'] = response_data['answer']
    
    
    else:
        results = deduplicate_results(run_parallel_searches(query))
        if not results: response_data = {"error": "Could not fetch search results."}
        else:
            summary_res = get_ai_summary(query, results)
            links_res = get_ranked_links(query, results)
            response_data = {**summary_res, **links_res}


   
    if output_format == 'gui':
        return render_template('results.html', data=response_data)
    else: 
        return jsonify(response_data)


if __name__ == '__main__':
    app.run(debug=True, port=5000)