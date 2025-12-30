import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentConfig
from google.genai.errors import ClientError
from visualize_trie import build_trie_graph


from trie import Trie
from schema import ThemedWordList

# --------------------------------------------------
# ENV + CLIENT
# --------------------------------------------------
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# --------------------------------------------------
# FALLBACK WORDS
# --------------------------------------------------
def load_fallback_words(theme, trie):
    fallback = {
        "space": ["planet", "galaxy", "orbit", "asteroid", "nebula"],
        "fantasy": ["dragon", "wizard", "magic", "castle", "quest"],
        "technology": ["ai", "cloud", "database", "server", "robot"],
        "earth": ["continent", "volcano", "river", "forest", "mountain"],
        "ocean": ["coral", "wave", "reef", "tide", "shark"],
        "music": ["melody", "rhythm", "guitar", "piano", "harmony"],
    }


    words = fallback.get(theme.lower(), fallback["fantasy"])
    for w in words:
        trie.insert(w)
    return words, True


# --------------------------------------------------
# GEMINI WORD GENERATION
# --------------------------------------------------
def generate_words(theme, num_words, trie):
    prompt = (
        f"Generate exactly {num_words} unique single words "
        f"related to '{theme}'. Return JSON:\n"
        f'{{"words": ["word1", "word2"]}}'
    )

    config = GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=ThemedWordList,
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=config,
        )

        words = response.parsed.words
        for w in words:
            trie.insert(w.lower())
        return words, False

    except (ClientError, Exception):
        return load_fallback_words(theme, trie)


# --------------------------------------------------
# STREAMLIT UI
# --------------------------------------------------
st.set_page_config(page_title="Trie Autocomplete Visualizer", layout="centered")

st.title("🌳 Trie Autocomplete Visualizer")
st.markdown(
    """
    This app demonstrates **Trie data structures** for fast autocomplete  
    with **AI-generated words** and **visual tree representation**.
    """
)

# Sidebar controls

st.sidebar.header("Configuration")

theme = st.sidebar.selectbox(
    "Choose a Theme",
    [
        "space",
        "fantasy",
        "technology",
        "ocean",
        "earth",
        "sports",
        "music",
        "mythical creatures"
    ]
)

num_words = st.sidebar.slider(
    "Number of words",
    min_value=5,
    max_value=50,
    value=15
)


# Session state
if "trie" not in st.session_state:
    st.session_state.trie = Trie()
    st.session_state.words = []

# Generate button
if st.sidebar.button("Generate Trie"):
    st.session_state.trie = Trie()
    words, fallback = generate_words(theme, num_words, st.session_state.trie)
    st.session_state.words = words

    if fallback:
        st.warning("Using fallback words (Gemini unavailable).")
    else:
        st.success("Words generated using Gemini AI!")

# Display words
if st.session_state.words:
    st.subheader("📄 Loaded Words")
   

    cols = st.columns(4)
    for i, word in enumerate(st.session_state.words):
        cols[i % 4].markdown(
            f"""
            <div style="
                padding:6px;
                border-radius:8px;
                background:#1f2937;
                text-align:center;
                margin-bottom:10px;
            ">
                {word}
            </div>
            """,
            unsafe_allow_html=True
        )



    # Graph visualization
    st.subheader("🌳 Trie Visualization")
    # Graph visualization
    

    trie_graph = build_trie_graph(
        st.session_state.trie,
        theme,
        len(st.session_state.words)
    )

    st.graphviz_chart(trie_graph)


st.subheader("🔍 Autocomplete")
prefix = st.text_input("Type a prefix")

if prefix:
    if not st.session_state.words:
        st.info("Generate the Trie first from the sidebar 👈")
    else:
        results = st.session_state.trie.search_prefix(prefix.lower())
        if results:
            st.success(results)
        else:
            st.error("No suggestions found")


st.markdown("---")

