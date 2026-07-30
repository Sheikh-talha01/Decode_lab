from src.project1 import memory


def test_create_and_append(tmp_path):
    # use default DB path in project root; ensure clean state by re-initializing
    memory.init_db()
    sid = memory.create_session()
    assert sid
    memory.append_message(sid, "user", "hello")
    memory.append_message(sid, "assistant", "hi")
    hist = memory.get_history(sid)
    assert len(hist) >= 2
