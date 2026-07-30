from fastapi import FastAPI, HTTPException
from .schema import CreateSessionResponse, ChatRequest, ChatResponse
from . import memory, llm
import json


def create_app():
    memory.init_db()
    app = FastAPI(title="Project1 Chat with Memory")


    @app.post("/session", response_model=CreateSessionResponse)
    def create_session():
        sid = memory.create_session()
        return {"session_id": sid}


    @app.post("/chat", response_model=ChatResponse)
    async def chat(req: ChatRequest):
        # append user message
        memory.append_message(req.session_id, "user", req.message)
        # prepare prompt from history
        history = memory.get_history(req.session_id, limit=20)
        prompt = "\n".join([f"{r}:{c}" for r, c in history]) + "\nUser: " + req.message

        adapter = llm.OpenAIAdapter()
        raw = await adapter.generate(prompt)
        try:
            data = json.loads(raw)
            resp = data.get("generated", str(raw))
        except Exception:
            resp = str(raw)

        # append assistant message and prune
        memory.append_message(req.session_id, "assistant", resp)
        memory.prune_history(req.session_id, max_turns=20)

        hist = memory.get_history(req.session_id, limit=20)
        return {"session_id": req.session_id, "response": resp, "history": [{"role": r, "content": c} for r, c in hist]}


    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app
