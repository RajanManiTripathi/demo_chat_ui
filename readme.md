to run the fast api backend

run 
```bash
uvicorn test:app --reload


```


### Example cURL Command for Testing:

To interact with the assistant via `POST` requests, use the following cURL command:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/chat/' \
  -H 'Content-Type: application/json' \
  -d '{
    "user_input": "Tell me about your recruitment services.",
    "session_id": "session_123",
    "persona_prompt": "You are a professional recruitment assistant who helps with hiring decisions.",
    "model_name": "gemini/gemini-2.0-flash"
  }'
```
`

### Follow-up Query:

To continue the conversation, send the same `session_id` with a follow-up query:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/chat/' \
  -H 'Content-Type: application/json' \
  -d '{
    "user_input": "Can you share more about how you assess candidates?",
    "session_id": "session_123",
    "persona_prompt": "You are a professional recruitment assistant who helps with hiring decisions.",
    "model_name": "gemini/gemini-2.0-flash"
  }'
```
