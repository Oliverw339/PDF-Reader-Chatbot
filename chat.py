from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from llm import create_llm


embeddings = HuggingFaceEmbeddings( model_name= "sentence-transformers/all-MiniLM-L6-v2")

vectorstore = FAISS.load_local( "vectorstores\keto", embeddings, allow_dangerous_deserialization=True)

print("Vectorstore loaded")

#test for good chunks
# question = "What ingredients are used for keto bread?"

# docs = vectorstore.similarity_search(
#     question,
#     k=1
# )


# for doc in docs:
#     print("----------------")
#     print(doc.page_content[:500])
#     print(doc.metadata)

llm = create_llm()

question = "Give me a light and fluffy bread recipe"

docs = vectorstore.similarity_search(question,k=3)

context = "\n\n".join(doc.page_content for doc in docs)

prompt= f""" You answer questions about baking using the below context.
Context: {context} 
Question: {question}
Answer: """ 

response = llm.invoke(prompt)

print(response)