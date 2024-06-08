from flask import Flask,request
from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.document_loaders import PDFPlumberLoader
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.prompts import PromptTemplate

#! Creating a Flask application instance.
app=Flask(__name__)
#! Defining the path to the directory where the vector store will be saved.
folder_path="db"
#!  Initializing an embedding model to convert documents into vector representations.
embedding=FastEmbedEmbeddings()

#! Creating a reference/instance of Ollama lm
llm=Ollama(model="llama3")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1024, chunk_overlap=80, length_function=len, is_separator_regex=False
)
"""
is_separator_regex=False: This indicates that the separator used to split 
the text is not based on a regular expression. Instead, it relies on other 
methods to identify where to split the text.
"""


raw_prompt = PromptTemplate.from_template(
    """ 
    <s>[INST] You are a technical assistant, good at searching docuemnts. If you do not have an answer from the provided information say so. [/INST] </s>
    [INST] {input}
           Context: {context}
           Answer:
    [/INST]
"""
)



@app.route("/ai", methods=["POST"])
def aiPost():
  print("Post /ai called")
  json_content=request.json
  query=json_content.get("query")

  print(f"query:{query}")


  #? Invoking the reference
  response=llm.invoke(query)
  print(response)


  response_answer ={"Answer" : response}
  return response_answer

#! COPYING SAME+ FEW CHANGES
#! PDF Query Endpoint
@app.route("/ask_pdf", methods=["POST"])
def askPDFPost():
  #*This line prints a message to the console indicating that the /ask_pdf endpoint has been called.
  print("Post /ask_pdf called") 
  json_content=request.json
  query=json_content.get("query")

  print(f"query:{query}")

  #! Loading Vector Store
  print("Loading vector store")
  vector_store = Chroma(persist_directory=folder_path, embedding_function=embedding)

  #?Invoking the reference
  # response=llm.invoke(query)
  # print(response)
  # response_answer ={"Answer" : response}
  # return response_answer
  #! Creating Retrieval Chain
  print("Creating chain")
  #* This line creates a retriever object from the vector store
  retriever = vector_store.as_retriever(
      search_type="similarity_score_threshold",
      search_kwargs={
          "k": 20,
          #*The search_kwargs dictionary specifies that up to 20 documents (k: 20) should be retrieved,
          #* and only documents with a similarity score above 0.1 
          "score_threshold": 0.1,
      },
    )
  
  #*This chain processes and formats the documents retrieved for further use.
  document_chain = create_stuff_documents_chain(llm, raw_prompt)
  chain = create_retrieval_chain(retriever, document_chain)

  #*The chain processes the query, retrieves relevant documents, and generates a response, which is stored in the result variable.
  result = chain.invoke({"input": query})

  print(result) #*This line prints the result to the console for debugging purposes.

  #!initializing an empty list~(sources) to store information about the retrieved documents.
  sources = []
  for doc in result["context"]:
      sources.append(
          {"source": doc.metadata["source"], "page_content": doc.page_content}
      )

  response_answer = {"answer": result["answer"],"sources":sources}
  return response_answer


#! PDF upload endpoint
@app.route("/pdf", methods=["POST"])
def pdfPost():
  file=request.files["file16"] #! "file" is the key as it will be store as a dictionary
  file_name=file.filename
  save_file="pdf/" + file_name #! This line constructs the path where the uploaded file will be saved
  file.save(save_file)
  print(f"filename:{file_name}")

  loader = PDFPlumberLoader(save_file)
  docs = loader.load_and_split()
  print(f"docs len={len(docs)}")

  chunks = text_splitter.split_documents(docs)
  print(f"chunks len={len(chunks)}")

  vector_store = Chroma.from_documents(
      documents=chunks, embedding=embedding, persist_directory=folder_path
  ) #*persist_directory specifies where to store the vector data on disk

  vector_store.persist()


  response={
    "status" : "Successfully uploaded",
    "FileName": file_name,
    "doc_len": len(docs),
    "chunks": len(chunks)
  }
  return response



def start_app():
  app.run(host="0.0.0.0" , port=8080, debug=True)

#*Ensures that the application starts only if the script is run directly
if __name__== "__main__":
  start_app()







# from flask import Flask,request
# from langchain_community.llms import ollama
# app=Flask(__name__)
# llm=Ollama(model="llama3")
# @app.route("/ai", methodes=["POST"])
# def aiPost()
#   print("Post /ai called")
#   json_content=request.json
#   query=json_content.get(ques)
#   print(f"query:{query}") 
#   response=llm.invoke(query)
#   print(response)

#   response_answer={"Answer" : response}
#   return response_answer

# def start_app():
#   app.run(host="0.0.0.0", port=8080,debug=True)

# if(__name__=="__main__"):
#   start_app()  