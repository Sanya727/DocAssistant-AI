from quart import Quart, request, jsonify, render_template
from langchain_community.llms import Ollama  #!Ollama represents a language model
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.document_loaders import PDFPlumberLoader
from langchain.prompts import PromptTemplate
import os

#! Application Setup
app = Quart(__name__, template_folder='templates')
#? variable to store the path to the database folder
folder_path = "db"  
embedding = FastEmbedEmbeddings()

#! Language Model Initialization
llm = Ollama(model="llama3")

#! Text Splitter Initialization
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1024, chunk_overlap=80, length_function=len, is_separator_regex=False #* regex false indicates that the separator should be treated as a lteral string,not as a regular expression.
)

#! Prompt Template Initialization
raw_prompt = PromptTemplate.from_template(
    """
    <s>[INST] You are a technical assistant, good at searching documents. If you do not have an answer from the provided information, say so. [/INST] </s>
    [INST] {input}
           Context: {context}
           Answer:
    [/INST]
    """
)

#! homepage
@app.route('/')
async def index():
    return await render_template('index.html')


#! for any general query
@app.route("/ai", methods=["POST"])
async def ai_post():
    json_content = await request.json  #* handling req
    query = json_content.get("query")  #* extracts the value associated with the key "query" from the JSON content
    response = llm.invoke(query)       #* invoking lang model
    response_answer = {"Answer": response} #*dictionary
    return jsonify(response_answer)



#! to upload pdf
@app.route("/pdf", methods=["POST"])
async def pdf_post():
    file = (await request.files)["file"]
    file_name = file.filename
    save_file = os.path.join("pdf", file_name)
    await file.save(save_file) #*  writes the file to the disk

    loader = PDFPlumberLoader(save_file) #* PDFPlumberLoader is a utility for loading PDF documents
    docs = loader.load_and_split()       #* splits the PDF into documents 
    chunks = text_splitter.split_documents(docs) #* splits the loaded documents into smaller chunks.

    vector_store = Chroma.from_documents(
        documents=chunks, embedding=embedding, persist_directory=folder_path
    )

    response = {
        "status": "Successfully uploaded",
        "FileName": file_name,
        "chunks": len(chunks)
    }
    return jsonify(response)



#! for pdf-specific query
@app.route("/ask_pdf", methods=["POST"])
async def ask_pdf_post():
    json_content = await request.json
    query = json_content.get("query")

    try:
        #? specifying the directory where the vector store is persisted and the embedding function to use
        vector_store = Chroma(persist_directory=folder_path, embedding_function=embedding)
        #? Creating a Retriever
        retriever = vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                #? k=20 means the retriever will fetch up to 20 documents that are most similar to the query.
                "k": 20,
                "score_threshold": 0.1,
            },
        )

        #? Retrieving documents based on the query
        retrieved_docs = retriever.invoke({"query": query})
        print("Documents retrieved")

        #? Processing the retrieved documents
        #? creates a single string containing the text from all the retrieved documents.
        context = "<br><br>".join([doc.page_content for doc in retrieved_docs])
        print("Retrieved documents processed")

        #? Generating the prompt with the context
        prompt = raw_prompt.format(input=query, context=context)
        print("Prompt generated")

        #? Generating the answer using the LLM and the provided context
        #! flatten() method is used to convert a nested list into a flat list. 
        result = llm.generate(prompts=[prompt])
        print("Result generated")
        # final_res=result.flatten()

        #? checking if the result is a list and if it is not empty
        if result.generations:
            generations_list= result.generations
            if generations_list:
                first_generation=generations_list[0]
                if first_generation:
                    first_chunk=first_generation[0]
                    answer=first_chunk.text.strip()
                else:
                    answer="No answer could be generated."
            else:
                answer="No answer could be generated."
        else:
            answer="No answer could be generated."                    


        response_answer = {
            "answer": answer,
            # "sources": unique_sources
        }

        return jsonify(response_answer)
    
    except Exception as e:
        print(f"An error occurred: {e}") #?This line will log the error message to the console
        return jsonify({"error": "An error occurred during processing."})


if __name__ == '__main__':
    app.run(debug=True)
