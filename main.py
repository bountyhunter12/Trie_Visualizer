import os
from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentConfig
from google.genai.errors import ClientError

from trie import Trie
from schema import ThemedWordList

# --------------------------------------------------
# ENV SETUP
# --------------------------------------------------
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# --------------------------------------------------
# FALLBACK WORDS
# --------------------------------------------------
def load_fallback_words(theme, trie):
    fallback = {
        "space": [
            "planet", "galaxy", "orbit", "asteroid",
            "nebula", "comet", "cosmos", "satellite"
        ],
        "fantasy": [
            "dragon", "wizard", "magic", "castle",
            "sword", "elf", "dwarf", "quest"
        ],
        "technology": [
            "algorithm", "network", "database", "server",
            "cloud", "ai", "robot", "blockchain"
        ],
    }

    words = fallback.get(theme.lower(), fallback["fantasy"])
    for w in words:
        trie.insert(w)
    print("⚠️ Using fallback words (offline-safe).")
    return words

# --------------------------------------------------
# GEMINI + TRIE LOADER
# --------------------------------------------------
def generate_and_load_trie(theme, num_words, trie):
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

        print(f"✓ Loaded {len(words)} AI-generated words.")
        return words

    except ClientError:
        return load_fallback_words(theme, trie)

    except Exception as e:
        print("Unexpected error:", e)
        return load_fallback_words(theme, trie)

# --------------------------------------------------
# MAIN
# --------------------------------------------------
def main():
    print("=" * 70)
    print("TRIE AUTOCOMPLETE WITH GEMINI API")
    print("=" * 70)

    theme = input("Enter a theme (default fantasy): ").strip() or "fantasy"

    try:
        num_words = int(input("How many words? (default 30): ") or "30")
    except ValueError:
        num_words = 30

    trie = Trie()
    words = generate_and_load_trie(theme, num_words, trie)

    print("\nLoaded words:")
    print(", ".join(words[:10]), "..." if len(words) > 10 else "")

    print("\nGenerating Trie visualization...")
    trie.visualize_graph("ai_generated_trie")

    print("\n" + "=" * 70)
    print("AUTOCOMPLETE MODE (type 'quit' to exit)")
    print("=" * 70)

    while True:
        prefix = input("Prefix: ").strip().lower()
        if prefix == "quit":
            break
        print(trie.search_prefix(prefix) or "No suggestions")

    print("\nThanks for using Trie Autocomplete!")


if __name__ == "__main__":
    main()
