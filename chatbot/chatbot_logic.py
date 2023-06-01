from llama_index import SimpleDirectoryReader, GPTListIndex, readers, GPTSimpleVectorIndex, LLMPredictor, PromptHelper, ServiceContext
from langchain.chat_models import ChatOpenAI
import os
import dotenv

dotenv.load_dotenv()

def construct_index():
    # set maximum input size
    max_input_size = 500
    # set number of output tokens
    num_outputs = 500
    # set maximum chunk overlap
    max_chunk_overlap = 20
    # set chunk size limit
    chunk_size_limit = 600

    openai_api_key = os.getenv('OPENAI_API_KEY')

    # define prompt helper
    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    # define LLM
    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", max_tokens=num_outputs))

    directory_path = "context_data/data"
    documents = SimpleDirectoryReader(directory_path).load_data()
    
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)
    index = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)

    index.save_to_disk('index.json')

    return index

def get_response(query):
    if not os.path.exists('index.json'):
        construct_index()
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    response = index.query(query)
    print(response.response)
    return response.response