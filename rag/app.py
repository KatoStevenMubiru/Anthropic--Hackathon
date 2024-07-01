import streamlit as st
from llama_index.core import VectorStoreIndex, Settings, Document
from llama_index.core.embeddings import resolve_embed_model
from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.core.llms import LLM
from claude_llm import Claude
from document_processor import process_healthcare_document
from healthcare_utils import categorize_query, format_healthcare_response
import os
import asyncio
from typing import Any, List, Optional
from pydantic import BaseModel, Field

def reset():
    st.session_state.messages = []

st.title("Healthcare Document Interrogation System")

api_key = st.sidebar.text_input("Claude API Key", type="password")
os.environ["ANTHROPIC_API_KEY"] = api_key

def provider(model_name):
    return "claude-3-5-sonnet-20240620"

@st.experimental_fragment
def mp_fragment():
    model_name = "claude-3-5-sonnet-20240620"
    provider_name = provider(model_name)
    return model_name, provider_name

class LLMMetadata(BaseModel):
    model_name: str = Field(description="The model name")
    context_window: int = Field(description="The context window size")
    num_output: int = Field(description="Maximum number of output tokens")
    is_chat_model: bool = Field(description="Whether the model is a chat model")
    is_function_calling_model: bool = Field(description="Whether the model supports function calling")
    max_tokens: Optional[int] = Field(description="The maximum number of tokens (if applicable)")
    system_role: str = Field(default="system", description="The role for system messages")

class ClaudeLLM(LLM):
    claude_instance: Claude = Field(exclude=True)

    def __init__(self, claude_instance: Claude):
        super().__init__()
        self.claude_instance = claude_instance

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(
            model_name=self.claude_instance.model,
            context_window=self.claude_instance.context_window,
            num_output=self.claude_instance.max_tokens,
            is_chat_model=True,
            is_function_calling_model=False,
            max_tokens=self.claude_instance.max_tokens,
            system_role="system"
        )

    def complete(self, prompt: str, **kwargs: Any) -> str:
        return self.claude_instance.complete(prompt, **kwargs)

    def chat(self, messages: List[Any], **kwargs: Any) -> str:
        return self.claude_instance.chat(messages, **kwargs)

    def stream_complete(self, prompt: str, **kwargs: Any) -> Any:
        raise NotImplementedError("Stream complete not implemented for Claude")

    def stream_chat(self, messages: List[Any], **kwargs: Any) -> Any:
        raise NotImplementedError("Stream chat not implemented for Claude")

    async def acomplete(self, prompt: str, **kwargs: Any) -> str:
        return await asyncio.to_thread(self.complete, prompt, **kwargs)

    async def achat(self, messages: List[Any], **kwargs: Any) -> str:
        return await asyncio.to_thread(self.chat, messages, **kwargs)

    async def astream_chat(self, messages: List[Any], **kwargs: Any) -> Any:
        raise NotImplementedError("Async stream chat not implemented for Claude")

    async def astream_complete(self, prompt: str, **kwargs: Any) -> Any:
        raise NotImplementedError("Async stream complete not implemented for Claude")

def load_models(model_name, provider_name):
    claude = Claude(model=model_name, api_key=api_key)
    Settings.llm = ClaudeLLM(claude)
    Settings.embed_model = resolve_embed_model("local:BAAI/bge-small-en-v1.5")
    st.write(f"Models loaded: {model_name}")

@st.cache_resource
def rerank_model():
    rerank = SentenceTransformerRerank(
        model="cross-encoder/ms-marco-MiniLM-L-2-v2", top_n=3
    )
    return rerank

with st.sidebar:
    model_name, provider_name = mp_fragment()
    uploaded_file = st.file_uploader("Upload a healthcare PDF", accept_multiple_files=False, on_change=reset)
    st.sidebar.button("Clear Chat History", on_click=reset)

load_models(model_name, provider_name)

if uploaded_file is not None:
    @st.cache_resource
    def vector_store(uploaded_file):
        try:
            st.write(f"Processing file: {uploaded_file.name}")
            documents = process_healthcare_document(uploaded_file)
            st.write(f"Created {len(documents)} document chunks")
            index = VectorStoreIndex.from_documents(documents)
            st.write("Vector index created succesfully")
            return index 
        except Exception as e:
            st.error(f"Error creating index: {str(e)}")
           
    
    index = vector_store(uploaded_file)
    if index:
        chat_engine = index.as_chat_engine(chat_mode="context", verbose=True, similarity_top_k=10, node_postprocessors=[rerank_model()])
        st.write("Chat engine created successfully")
    else:
        st.error("Failed to create chat engine")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if len(st.session_state.messages) == 0:
    with st.chat_message("assistant"):
        initial = "Welcome to the Healthcare Document Interrogation System. Please upload a healthcare-related PDF to begin."
        st.markdown(initial)
        st.session_state.messages.append({"role": "assistant", "content": initial})


if prompt := st.chat_input():
    if not api_key:
        st.warning("Please enter a Claude API key.")
    elif not uploaded_file:
        st.warning("Please upload a healthcare document.")
    elif 'chat_engine' not in locals():
        st.warning("Chat engine not initialized. Please check for errors above.")
    else: 
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                st.write("Processing query...")
                query_category = categorize_query(prompt)
                response = chat_engine.chat(prompt)
                print(response)
                st.write("Query processed successfully")
                formatted_response = format_healthcare_response(response, query_category)
                st.write(formatted_response)
                st.session_state.messages.append({"role": "assistant", "content": formatted_response})
            
            except Exception as e:
                st.error(f"Error processing query: {str(e)}")