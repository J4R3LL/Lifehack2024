import articles as cna
import spacy
import networkx as nx
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login

cna_articles = cna.cna_articles()
nlp = spacy.load("en_core_web_sm")
login(token="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")

# model_name = "mistralai/Mistral-7B-v0.3"
# model = AutoModel.from_pretrained(model_name)


# mistral_models_path = Path.home().joinpath('mistral_models', '7B-v0.3')
# mistral_models_path.mkdir(parents=True, exist_ok=True)

# snapshot_download(repo_id="mistralai/Mistral-7B-v0.3", allow_patterns=["params.json", "consolidated.safetensors", "tokenizer.model.v3"], local_dir=mistral_models_path)

def extract_entities(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    entities = []
    for entity in doc.ents:
        entities.append(entity.text)
    return entities

def extract_relationships(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    relationships = []
    for token in doc:
        if token.dep_ in ["prep", "pobj"]:  # Extract prepositional phrases and their objects
            relationships.append((token.head.text, token.text))
    return relationships

def create_knowledge_graph(text):
    entities = extract_entities(text)
    relationships = extract_relationships(text)
    G = nx.Graph()
    G.add_nodes_from(entities)
    G.add_edges_from(relationships)
    return G

text = ''.join(cna_articles)
knowledge_graph = create_knowledge_graph(text)
#print("Nodes:", knowledge_graph.nodes())
#print("Edges:", knowledge_graph.edges())


# Function to enhance input with knowledge graph
def enhance_input_with_kg(input_text):
    # Extract entities from the input text
    doc = nlp(input_text)
    entities = [ent.text for ent in doc.ents]
    
    # Append knowledge graph information to the input text
    enhanced_text = input_text
    for entity in entities:
        if entity in knowledge_graph:
            facts = " ".join(knowledge_graph[entity])
            enhanced_text += f" {entity} {facts}."
    
    return enhanced_text

# Load the LLaMA2 model and tokenizer

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Meta-Llama-3-8B")

# model_id = "mistralai/Mistral-7B-v0.3"
# tokenizer = AutoTokenizer.from_pretrained(model_id)

# model = AutoModelForCausalLM.from_pretrained(model_id)

# User input
#user_input = "What happens if there's a bomb threat on your flight?"
user_input = input("User: ")
enhanced_input = enhance_input_with_kg(user_input)

# Tokenize and generate response
input_tokens = tokenizer.encode(enhanced_input, return_tensors="pt")
output = model.generate(input_tokens, max_length=100, num_return_sequences=1)

# Decode and print the response
response = tokenizer.decode(output[0], skip_special_tokens=True)
print("LLM:", response)