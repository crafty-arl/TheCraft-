# app.py

from components import (
    display_introduction,
    display_components,
    display_card_database,
    display_setup_and_gameplay,
    display_chat,display_card_database_content
)
import streamlit as st

def main():
    st.sidebar.title("Crafty Tales")
    st.sidebar.subheader("Table of Contents")

    section = st.sidebar.radio(
        "",
        (
            "Introduction",
            "Components",
            "Card Database",
            "Setup and Gameplay",
            "Chat with the Game Master",
        ),
    )

    if section == "Introduction":
        display_introduction()
    elif section == "Components":
        display_components()
    elif section == "Card Database":
        display_card_database()
    elif section == "Setup and Gameplay":
        display_setup_and_gameplay()
    elif section == "Chat with the Game Master":
        display_chat()
        

if __name__ == "__main__":
    main()
