import openai
from transformers import GPT2Tokenizer, GPT2LMHeadModel
openai.api_key = "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"

# ... (rest of the code)

def generate_chatbot_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text.strip()
def ask_question(question):
    
   
    prompt = f"Answer the following question about the rules of Crafty Tales, based on the provided game manual:\n{question}"
    model = "text-davinci-003"
    params = {
        "max_tokens": 150,
        "min_tokens": 0,  
        "temperature": 0,
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

def generate_hidden_objectives(deck_data, model, tokenizer, num_objectives=5):
    prompt = f"Generate {num_objectives} hidden objectives for a card game based on the following deck data: {deck_data}"

    inputs = tokenizer.encode(prompt, return_tensors='pt')
    outputs = model.generate(inputs, max_length=100, num_return_sequences=num_objectives, no_repeat_ngram_size=2, temperature=0.8)
    generated_objectives = []

    for output in outputs:
        objective = tokenizer.decode(output, skip_special_tokens=True)
        generated_objectives.append(objective)

    return generated_objectives



def generate_story_arcs_from_deck(deck_data, model, tokenizer, num_arcs=3):
    prompt = f"Generate {num_arcs} story arcs for a card game based on the following deck data: {deck_data}"

    inputs = tokenizer.encode(prompt, return_tensors='pt')
    outputs = model.generate(inputs, max_length=150, num_return_sequences=num_arcs, no_repeat_ngram_size=2, temperature=0.8)
    generated_arcs = []

    for output in outputs:
        arc = tokenizer.decode(output, skip_special_tokens=True)
        generated_arcs.append(arc)

    return generated_arcs
