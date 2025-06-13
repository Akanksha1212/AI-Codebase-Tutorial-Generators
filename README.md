

## 🚀 Getting Started

1. Clone this repository

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up LLM in [`utils/call_llm.py`](./utils/call_llm.py) by providing credentials. By default, you can use the AI Studio key with this client for Gemini Pro 2.5:

   ```python
   client = genai.Client(
     api_key=os.getenv("GEMINI_API_KEY", "your-api_key"),
   )
   ```

4. To run the webhook listener locally run python3 webhook.py 

5. Run ngrok http 5050 (or 5000 whichever port is free) in another terminal

6. Add webhook to the bitbucket repo and copy payload url(ttps://04e0-147-161-166-182.ngrok-free.app/payload) from previous screen

Now when you create a new PR in that repo or if code gets merged the webhook will get triggered