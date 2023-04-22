import streamlit as st
import PyPDF2
from openai_utils import ask_question
from pdf_loader import load_pdf_content

from utils import (display_introduction_content, display_components_content, display_card_database_content,generate_chatbot_response, display_setup_and_gameplay_content,display_tips_and_strategies_content,generate_chatbot_response)


def display_introduction():
    display_introduction_content()

def display_components():
    display_components_content()

def display_card_database():
    display_card_database_content()

def display_setup_and_gameplay():
    display_setup_and_gameplay_content()

def display_tips_and_strategies():
    display_tips_and_strategies_content()


def display_chat():
    game_manual_file = "\Crafty+\Crafty Tales_ Game Rules.pdf"
    game_manual_text = load_pdf_content(game_manual_file)
    st.write("I'm the GAME Master for Crafty Tales. Ask me anything about the game!")
   


    user_input = st.text_input("You: ", "")
    submit_button = st.button("Submit")

    if submit_button and user_input:
        text = generate_chatbot_response(game_manual_text)
        chatbot_response = ask_question(user_input)
        st.write(f"Chatbot: {chatbot_response}")
        print(game_manual_text)
def display_upload_decks():
    st.markdown("## Upload Decks")
    st.write("Upload your deck files to add them to the card database (30 cards only).")

    uploaded_file = st.file_uploader("Choose a deck file (.txt or .csv)", type=["txt", "csv"])

    if uploaded_file is not None:
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
        st.write(file_details)
        file_data = uploaded_file.getvalue().decode("utf-8")
        
        # Check if there are exactly 30 cards in the deck
        card_data = file_data.splitlines()
        if len(card_data) != 30:
            st.error("Your deck must contain exactly 30 cards.")
            return

        st.write(file_data)
        st.success("Deck successfully uploaded!")

        # Add custom tag for the deck
        custom_tag = st.text_input("Enter a custom tag for your deck:")
        if custom_tag:
            # Save the custom tag along with the deck data in the card database
            # Replace `save_deck_to_database` with the actual function to save data in your database
            save_deck_to_database(deck_data=card_data, custom_tag=custom_tag)
            st.success(f"Deck tagged with '{custom_tag}'")

def display_hidden_objectives():
    st.markdown("## Hidden Objectives")
    st.write("Generate hidden objectives based on your uploaded decks.")

    if st.button("Generate Objectives"):
        deck_data = ""  # Replace this with the actual uploaded deck data
        hidden_objectives = generate_hidden_objectives(deck_data)
        st.write(hidden_objectives)

def display_story_arcs():
    st.markdown("## Story Arcs")
    st.write("Generate story arcs based on your uploaded decks.")

    if st.button("Generate Story Arcs"):
        deck_data = ""  # Replace this with the actual uploaded deck data
        story_arcs = generate_story_arcs_from_deck(deck_data)
        st.write(story_arcs)
