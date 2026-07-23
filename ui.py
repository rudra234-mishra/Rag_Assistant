import streamlit as st
from backend import ask_question

st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif !important; }

/* ── Background: pure black ── */
.stApp { background: #0a0a0a; }

.block-container {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 2rem 1.5rem !important;
}

/* ── Title: red → green gradient ── */
h1 {
    font-size: 1.9rem !important;
    font-weight: 700 !important;
    text-align: center;
    background: linear-gradient(90deg, #ef4444, #22c55e);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
}
p { color: #6b7280 !important; text-align: center; }

/* ── User bubble: red tint ── */
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: #1a0808 !important;
    border: 1px solid #ef4444 !important;
    border-radius: 18px 18px 4px 18px !important;
    padding: 14px 18px !important;
    margin: 6px 0 !important;
    box-shadow: 0 0 16px rgba(239,68,68,0.12);
}

/* ── Assistant bubble: green tint ── */
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: #071a0c !important;
    border: 1px solid #22c55e !important;
    border-radius: 18px 18px 18px 4px !important;
    padding: 14px 18px !important;
    margin: 6px 0 !important;
    box-shadow: 0 0 16px rgba(34,197,94,0.1);
}

/* ── User text ── */
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) p,
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) span,
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) div {
    color: #fca5a5 !important;
    font-size: 0.95rem !important;
    line-height: 1.7 !important;
}

/* ── Assistant text ── */
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) p,
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) span,
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) div {
    color: #bbf7d0 !important;
    font-size: 0.95rem !important;
    line-height: 1.7 !important;
}

/* ── User avatar: red ── */
div[data-testid="chatAvatarIcon-user"] {
    background: linear-gradient(135deg, #ef4444, #b91c1c) !important;
    border-radius: 50% !important;
    box-shadow: 0 0 10px rgba(239,68,68,0.4);
}

/* ── Assistant avatar: green ── */
div[data-testid="chatAvatarIcon-assistant"] {
    background: linear-gradient(135deg, #22c55e, #15803d) !important;
    border-radius: 50% !important;
    box-shadow: 0 0 10px rgba(34,197,94,0.4);
}

/* ── Chat input ── */
div[data-testid="stChatInput"] {
    background: #111111 !important;
    border: 1.5px solid #1f1f1f !important;
    border-radius: 14px !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stChatInput"]:focus-within {
    border-color: #22c55e !important;
    box-shadow: 0 0 0 3px rgba(34,197,94,0.1) !important;
}
div[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: #e5e7eb !important;
    font-size: 0.95rem !important;
    border: none !important;
    box-shadow: none !important;
}
div[data-testid="stChatInput"] textarea::placeholder { color: #374151 !important; }
div[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #22c55e, #15803d) !important;
    border: none !important;
    border-radius: 8px !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stChatInput"] button:hover {
    opacity: 0.85 !important;
    transform: scale(1.06) !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #080808 !important;
    border-right: 1px solid #1a1a1a !important;
}
section[data-testid="stSidebar"] * { color: #9ca3af !important; }

/* ── Sidebar clear button: red ── */
section[data-testid="stSidebar"] .stButton > button {
    background: #0a0a0a !important;
    color: #ef4444 !important;
    border: 1.5px solid #ef4444 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    width: 100%;
    transition: all 0.2s ease !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: #ef4444 !important;
    color: #fff !important;
}

hr { border-color: #1a1a1a !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Sidebar ──
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:1.2rem 0 0.8rem 0;'>
        <div style='font-size:2.2rem;'>🤖</div>
        <div style='font-size:1rem;font-weight:700;
                    background:linear-gradient(90deg,#ef4444,#22c55e);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                    margin-top:6px;'>RAG Chatbot</div>
        <div style='font-size:0.75rem;color:#374151;margin-top:3px;'>Document Q&A</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    asked = len([m for m in st.session_state.messages if m["role"] == "user"])
    st.markdown(f"""
    <div style='display:flex;gap:8px;margin-bottom:4px;'>
        <div style='flex:1;background:#1a0808;border:1px solid #ef4444;
                    border-radius:12px;padding:12px 8px;text-align:center;'>
            <div style='font-size:1.5rem;font-weight:700;color:#ef4444;'>{asked}</div>
            <div style='font-size:0.7rem;color:#374151;margin-top:2px;'>Asked</div>
        </div>
        <div style='flex:1;background:#071a0c;border:1px solid #22c55e;
                    border-radius:12px;padding:12px 8px;text-align:center;'>
            <div style='font-size:1.5rem;font-weight:700;color:#22c55e;'>{asked}</div>
            <div style='font-size:0.7rem;color:#374151;margin-top:2px;'>Answered</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("<p style='font-size:0.72rem;color:#374151;text-align:left;letter-spacing:0.5px;'>TIPS</p>",
                unsafe_allow_html=True)
    for tip in ["Ask clear, specific questions", "Answers come from your document", "Ask follow-ups anytime"]:
        st.markdown(f"<p style='font-size:0.8rem;color:#6b7280;text-align:left;margin:4px 0;'>· {tip}</p>",
                    unsafe_allow_html=True)

    st.divider()

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()


# ── Header ──
st.markdown("<h1>🤖 RAG Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p>Ask questions and get answers from your document.</p>", unsafe_allow_html=True)
st.divider()

# ── Empty state ──
if not st.session_state.messages:
    st.markdown("""
    <div style='text-align:center;padding:3rem 1rem;
                background:#111111;
                border-top:2px solid #ef4444;
                border-bottom:2px solid #22c55e;
                border-left:1px solid #1f1f1f;
                border-right:1px solid #1f1f1f;
                border-radius:16px;margin:1rem 0 2rem 0;'>
        <div style='font-size:2.5rem;margin-bottom:10px;'>💬</div>
        <div style='font-size:1rem;font-weight:600;color:#e5e7eb;margin-bottom:6px;'>
            Start a conversation
        </div>
        <div style='font-size:0.85rem;color:#374151;'>
            Type your question below to get started.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Chat history ──
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ── Input ──
question = st.chat_input("Ask anything from your document...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = ask_question(question)
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})