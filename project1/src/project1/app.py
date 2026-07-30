from fastapi import FastAPI, HTTPException, Header, WebSocket, WebSocketDisconnect
from .schema import CreateSessionResponse, ChatRequest, ChatResponse
from . import memory, llm
import json
import os
from .auth import require_token


def _require_token(authorization: str | None, allow_none: bool = False):
    token = os.environ.get("PROJECT1_API_TOKEN")
    if not token:
        # no token configured -> allow all (dev mode)
        return True
    if not authorization:
        return False
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return False
    return parts[1] == token


def create_app():
    memory.init_db()
    app = FastAPI(title="Project1 Chat with Memory")


    @app.post("/session", response_model=CreateSessionResponse)
    def create_session():
        sid = memory.create_session()
        return {"session_id": sid}


    @app.post("/chat", response_model=ChatResponse)
    async def chat(req: ChatRequest, authorization: str | None = Header(None)):
        # check auth
            if not require_token(authorization):
                raise HTTPException(status_code=401, detail="Unauthorized")
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


    @app.websocket('/ws')
    async def websocket_endpoint(websocket: WebSocket):
        # Accept connection only if token matches (query param or header)
        await websocket.accept()
        token = websocket.query_params.get('token') or websocket.headers.get('authorization')
        if not require_token(token):
            await websocket.close(code=1008)
            return
        try:
            while True:
                data = await websocket.receive_text()
                # simple echo with mock generation
                adapter = llm.OpenAIAdapter()
                resp_raw = await adapter.generate(data)
                await websocket.send_text(str(resp_raw))
        except WebSocketDisconnect:
            return


    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app
