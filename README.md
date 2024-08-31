# EXPLORE (Expert Processing for Language and Optimal Retrieval of Documents and Extracts)
Welcome to the EXPLORE repository! This project integrates language models with document processing capabilities to provide a tool for managing and querying PDF documents. This project uses Quart for the backend framework, Langchain for working with language models (LLMs), and Chroma for managing vector stores. The system can handle both general queries and PDF-specific queries, offering a versatile solution for document management and interaction.



FEATURES:

1. Interactive Homepage: A clean and user-friendly homepage that welcomes users to the application.
2. AI-powered Querying: Leverage the power of the Ollama language model for general queries and document-specific questions.
3. PDF Upload: Upload PDF files and store them for future reference and querying.
4. Advanced Text Splitting: Utilizes Recursive Character Text Splitter to break down documents into manageable chunks, enhancing search and retrieval performance.
5. Embeddings and Vector Store: Fast and efficient document embedding with FastEmbedEmbeddings and storage using Chroma for quick retrieval.
6. Custom Prompt Templates: Tailor the interaction with the language model using customizable prompt templates to get the best responses.



KEY COMPONENTS AND FUNCTIONALITIES:

1. Backend Framework: Quart

    Quart is an asynchronous web framework for Python based on the ASGI standard. It is inspired by Flask and supports HTTP/1.1, HTTP/2, and WebSockets.
    The project sets up a Quart application to handle various routes for rendering templates and processing API requests.

2. Language Models: Langchain and Ollama

    Langchain is used for building applications with language models.
    Ollama represents the language model (in this case, llama3), which is initialized and used to generate responses to queries.

3. Document Processing and Vector Store:

    PDFPlumberLoader is used for loading and processing PDF documents.
    Chroma manages the vector store, which stores document embeddings to facilitate efficient document retrieval based on similarity scores.

4. Text Splitting:

    RecursiveCharacterTextSplitter is used to split large texts into manageable chunks. This ensures that queries can be efficiently processed even for lengthy documents.

5. Prompt Template:

    PromptTemplate is utilized to structure the input queries and context before sending them to the language model. This helps in generating more accurate and relevant responses.
