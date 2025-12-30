# Trie Autocomplete Visualizer

An interactive Streamlit-based Python project that demonstrates the Trie data structure for fast autocomplete.  
The project supports theme-based word generation using Google Gemini AI with a safe fallback mode, and visualizes the Trie structure as a tree.

This project is designed for learning, demonstration, and visualization of how Tries work internally.

---

## Features

### Trie Data Structure
- Efficient insertion  
- Prefix-based search (autocomplete)

### Theme-Based Word Generation
- Uses Google Gemini API (when available)
- Automatic fallback to local datasets

### Interactive Streamlit UI
- Theme selection (space, fantasy, technology, ocean, etc.)
- Adjustable number of words
- Live autocomplete suggestions

### Trie Visualization
- Visual tree rendering using Graphviz
- Shows how words are stored and shared by prefix

### Modular & Extensible Design
- Easy to add deletion, ranking, or advanced search

---

## Technologies Used
- Python 3.8+
- Streamlit
- Trie (Data Structures)
- Google Gemini API
- Graphviz
- Pydantic (schema validation)
- python-dotenv

## Frontend Preview

![Trie Autocomplete Visualizer UI](assets/.png)

---

## Requirements
- Python 3.8 or higher
- Graphviz (installed and added to PATH)

Install Python dependencies:
```bash
pip install -r requirements.txt
```
## Getting Started

### Clone the repository
```bash
git clone https://github.com/<your-username>/trie-autocomplete-visualizer.git
cd trie-autocomplete-visualizer
python -m venv venv
venv\Scripts\activate   # Windows
```
### Install dependencies
```bash
pip install -r requirements.txt
```
### Configure environment variables
```bash
GOOGLE_API_KEY=your_gemini_api_key_here
```
### Run the application
```bash
streamlit run streamlit_app.py
```

---

## How to Use
- Select a theme from the sidebar  
- Choose the number of words  
- Click **Generate Trie**  


---

## License
MIT License

