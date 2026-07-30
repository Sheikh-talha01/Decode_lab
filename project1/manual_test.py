import sys
sys.path.insert(0, r'D:\Decodes_lab\\project1\\src')
from project1 import memory, llm
import asyncio
import json

print('Running manual test_memory...')
memory.init_db()
sid = memory.create_session()
memory.append_message(sid, 'user', 'hello')
memory.append_message(sid, 'assistant', 'hi')
hist = memory.get_history(sid)
print('history length:', len(hist))
assert len(hist) >= 2
print('manual test_memory passed')

print('\nRunning demo chat (mock LLM fallback)')
sid2 = memory.create_session()
memory.append_message(sid2, 'user', 'What is my name?')
adapter = llm.OpenAIAdapter(api_key=None)
prompt = '\n'.join([f"{r}:{c}" for r,c in memory.get_history(sid2)]) + '\nUser: What is my name?'
raw = asyncio.get_event_loop().run_until_complete(adapter.generate(prompt))
data = json.loads(raw)
resp = data.get('generated')
memory.append_message(sid2, 'assistant', resp)
print('session:', sid2)
print('assistant response (mock):', resp)
print('final history:', memory.get_history(sid2))
