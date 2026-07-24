from langchain_ollama import OllamaLLM


def create_llm():
    # Create an OllamaLLM
    llm = OllamaLLM(
        model="llama3.2:3b",
        temperature=0.2
    )

    return llm

create_llm()

