import os
import tempfile
import pdfplumber
from transformers import GPT2Tokenizer

def initialize_engine_with_pdf_text(game_manual_path, *uploaded_files):
    extracted_texts = []

     # Extract text from the game manual
    full_text = extract_text_from_pdf(game_manual_path)
    extracted_texts.append(full_text)

    # Extract texts from the uploaded decks
    for uploaded_file in uploaded_files:
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_file_path = temp_file.name

        # Extract text from the PDF file using pdfplumber
        full_text = extract_text_from_pdf(temp_file_path)
        extracted_texts.append(full_text)

        # Remove the temporary file
        os.remove(temp_file_path)

    # Combine the extracted texts from all PDFs and truncate the text to 4000 tokens
    combined_text = " ".join(extracted_texts)
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    tokens = tokenizer(combined_text, return_tensors="pt", truncation=True, max_length=4000).input_ids[0]
    truncated_text = tokenizer.decode(tokens)

    return truncated_text