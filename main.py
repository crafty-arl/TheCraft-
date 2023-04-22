import streamlit as st
import os
from PIL import Image
import pdfplumber
import openai
import tempfile
from transformers import GPT2Tokenizer

os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = "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"

def initialize_engine_with_pdf_text(game_manual_path, *uploaded_files):
    extracted_texts = []

    # Extract text from the game manual
    with pdfplumber.open(game_manual_path) as pdf:
        pages = [page.extract_text() for page in pdf.pages]
    full_text = " ".join(pages)
    extracted_texts.append(full_text)

    # Extract texts from the uploaded decks
    for uploaded_file in uploaded_files:
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_file_path = temp_file.name

        # Extract text from the PDF file using pdfplumber
        with pdfplumber.open(temp_file_path) as pdf:
            pages = [page.extract_text() for page in pdf.pages]

        # Remove the temporary file
        os.remove(temp_file_path)

        # Join the pages into a single string
        full_text = " ".join(pages)
        extracted_texts.append(full_text)

    # Combine the extracted texts from all PDFs and truncate the text to 4000 tokens
    combined_text = " ".join(extracted_texts)
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    tokens = tokenizer(combined_text, return_tensors="pt", truncation=True, max_length=4000).input_ids[0]
    truncated_text = tokenizer.decode(tokens)

    return truncated_text

    combined_text = " ".join(extracted_texts)
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    tokens = tokenizer(combined_text, return_tensors="pt", truncation=True, max_length=4096).input_ids[0]
    truncated_text = tokenizer.decode(tokens)

    return truncated_text

def ask_question(question, initial_memory):
    prompt = f"Answer the following question about the rules of Crafty Tales, based on the provided game manual:\n{question}\n\n{initial_memory}"
    model = "text-davinci-002"
    params = {
        "max_tokens": 100,
        "temperature": 0.5,
    }

    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=params["max_tokens"],
        temperature=params["temperature"],
        stop=None
    )

    answer = response.choices[0].text.strip()
    return answer
def generate_hidden_objectives(text):
    prompt = (f"You are the Game Master youre job is to read the Game Manual Crafty Tales and Generate Hidden Objectives based of Deck 1: and Deck:2 and create Story arc Cards based of the expecation the game will last 10 rounds, the theme of the decks, and actions players can take in game to achieve Story arcs be sure to include points associate with each hidden objective and story arcs.:\n{text}")
    model = "text-davinci-002"
    params = {
        "max_tokens": 4096,
        "temperature": 0.5,
        "n_top": 3
    }

    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=params["max_tokens"],
        temperature=params["temperature"],
        n=params["n_top"],
        stop=None
    )

    hidden_objectives = [choice.text.strip() for choice in response.choices]
    return hidden_objectives

def display_introduction():
    st.title("Crafty Tales - Game Manual")
    st.subheader("Introduction")
    st.write("""
    Crafty Tales is a strategy card game that combines storytelling and creativity. Players build personalized decks and engage in a story-driven battle where they use their characters, locations, events, and items to progress through story arcs and achieve objectives. The primary goal is to complete story arcs and accomplish hidden objectives while managing energy points.
    """)

def display_components():
    st.subheader("Components")
    components = {
        "Character cards": "The characters that players use in the game. Each character card has an energy point value, a name, a brief description of the character and their role in the story, and a unique ability that the character possesses.",
        "Location cards": "The locations that players use in the game. Each location card has an energy point value, a name, a brief description of the location and its significance in the story, and an effect that the location has on the game. Location cards can provide additional energy points, influence character abilities, or affect the game's narrative.",
                "Event cards": "The events that players use in the game. Each event card has an energy point value, a name, a brief description of the event and how it affects the story, and an effect that the event has on the game. Event cards can modify energy points, change a character's ability, or alter the game's narrative.",
        "Item cards": "The items that players use in the game. Each item card has an energy point value, a name, a brief description of the item and its function, and an effect that the item has on the game. Item cards can boost a character's energy points, modify abilities, or influence the game's narrative.",
        "Story Arc cards": "The cards that determine the overall story arc for the game. Each story arc card has a name and a brief description of the story arc. Players use the story arc cards to progress through the game's narrative and complete the objectives.",
        "Hidden Objective cards": "The personal goals that players keep secret from each other. Each hidden objective card has a name and a specific objective that the player must achieve. Hidden objective cards contribute to the overall story arc and provide points for players who complete them."
    }
    component = st.selectbox("Select a component:", list(components.keys()))
    st.write(f"{component}: {components[component]}")

def display_card_database():
    st.subheader("Card Database")
    st.write("Browse and search for character, location, event, and item cards.")
    search_card_type = st.selectbox("Search by card type", ["All", "Character", "Item", "Location", "Event"])

    if search_card_type == "All":
        card_types_to_display = ["Character", "Item", "Location", "Event"]
    else:
        card_types_to_display = [search_card_type]

    num_columns = 4

    for card_type in card_types_to_display:
        if os.path.exists(f"uploaded_images/{card_type}"):
            st.markdown(f"## {card_type}s")
            card_files = os.listdir(f"uploaded_images/{card_type}")

            cols = st.columns(num_columns)
            for index, card_file in enumerate(card_files):
                card_image = Image.open(f"uploaded_images/{card_type}/{card_file}")
                cols[index % num_columns].image(card_image, caption=card_file, use_column_width=True)

def display_setup_and_gameplay():
    st.subheader("Setup and Gameplay")

    # Define the game manual path
    game_manual_path = "\Crafty+\Crafty Tales_ Game Rules.pdf"

    # Add a chat interface to ask questions about the rules
    st.write("Do you have a question about the rules? Ask here!")
    question = st.text_input("Type your question:")
    if question:
        initial_memory_manual = initialize_engine_with_pdf_text(game_manual_path)
        answer = ask_question(question, initial_memory_manual)
        st.write(answer)


def display_tips_and_strategies():
    st.subheader("Tips and Strategies")
    # Add the tips and strategies content here
    st.write("Build a well-balanced deck with a mix of character, location, event, and item cards.")
    st.write("Pay attention to the energy points of your cards and manage your energy efficiently.")
    st.write("Adapt your strategy based on your hidden objectives and the current story arc.")
    st.write("Communicate with your opponents to create a collaborative and engaging story.")
    st.write("Be creative and take risks, as unexpected twists can lead to higher points and more entertaining gameplay.")
    st.subheader("Upload PDFs")
    uploaded_deck1 = st.file_uploader("Upload Deck 1 PDF", type=['pdf'], key='deck1')
    uploaded_deck2 = st.file_uploader("Upload Deck 2 PDF", type=['pdf'], key='deck2')
    
    submit_button = st.button("Submit")
    generate_story_arc_button = st.button("Generate Story Arc")

    if submit_button and uploaded_deck1 and uploaded_deck2:
        initial_memory_deck1 = initialize_engine_with_pdf_text(uploaded_deck1)
        initial_memory_deck2 = initialize_engine_with_pdf_text(uploaded_deck2)
        
        hidden_objectives_deck1 = generate_hidden_objectives(initial_memory_deck1)
        hidden_objectives_deck2 = generate_hidden_objectives(initial_memory_deck2)

        st.write("Generated Hidden Objectives for Deck 1:")
        for objective in hidden_objectives_deck1:
            st.write(objective)
        st.write("Generated Hidden Objectives for Deck 2:")
        for objective in hidden_objectives_deck2:
            st.write(objective)

    if generate_story_arc_button and uploaded_deck1 and uploaded_deck2:
        initial_memory_deck1 = initialize_engine_with_pdf_text(uploaded_deck1)
        initial_memory_deck2 = initialize_engine_with_pdf_text(uploaded_deck2)
        
        story_arc = generate_story_arc(initial_memory_deck1, initial_memory_deck2)
        st.write("Generated Story Arc:")
        st.write(story_arc)
def generate_hidden_objectives(initial_memory):
    # Set up OpenAI prompt and parameters
    prompt = (f"Generate three hidden objectives for Deck 1: and Deck 2: be sure that these are actions players can take in game Crafty Tales using the following PDF as reference:\n{initial_memory}")
    model = "text-davinci-002"
    params = {
        "max_tokens": 500,
        "temperature": 0.5,
        "n_top": 3
    }

    # Generate response from OpenAI
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=params["max_tokens"],
        temperature=params["temperature"],
        n=params["n_top"],
        stop=None
    )

    # Extract and return the generated hidden objectives
    hidden_objectives = [choice.text.strip() for choice in response.choices]
    return hidden_objectives


def main():
    st.sidebar.title("Navigation")
    section = st.sidebar.radio("Go to", [
        "Introduction",
        "Components",
        "Card Database",
        "Setup and Gameplay",
        "Tips and Strategies"
    ])

    if section == "Introduction":
        display_introduction()
    elif section == "Components":
        display_components()
    elif section == "Card Database":
        display_card_database()
    elif section == "Setup and Gameplay":
        display_setup_and_gameplay()
    elif section == "Tips and Strategies":
        display_tips_and_strategies()

if __name__ == "__main__":
    main()

