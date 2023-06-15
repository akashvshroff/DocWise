# DocWise: An AI PDF Analysis Tool
- DocWise is an AI tool, built using the OpenAI API and LangChain, that allows users to upload their own documents and *chat* with them. See it in action through the video below!
- The name of this tool was generated by ChatGPT, which used the following reasoning: "The name combines "Doc," a commonly used abbreviation for documents, and "Wise" to suggest the application's intelligence and expertise in analyzing PDF files. It conveys the idea that the application can provide valuable insights and understanding from PDF documents, making it a smart choice for users seeking efficient analysis".

## Purpose
- The tool is incredibly useful in helping you optimize your interaction with conversational models by allowing you to provide context to the model itself. You can use upload lectures notes for a class and ask the tool to recommend key words that you should learn before a test or you could upload a lengthy annual report for a company and get the model to summarize the financial performance of the company and help you understand whether it is a good investment. The possibilities are endless. 
- In effect, the tool is built by *chaining* a context engine, (by way of vector embeddings) to the conversational ability of the existing OpenAI models, thereby allowing you to leverage the conversational style and overcome ChatGPT's knowledge limitations.
- I built this tool to help me get experience working with LangChain and understanding how we can use the library to build solutions on top of existing AI models that extend their functionality and improve the process of working with them.

## Tech Breakdown
- The two sections briefly cover the tech that I used to build this system. I learnt a lot of the tools, especially on the langchain side, from Nicholas Renotte's wonderful tutorial that can be found [here](https://www.youtube.com/watch?v=u8vQyTzNGVY&list=PLp7virpu8w7XuBgGJvEWZaLsBM-hnBjq1&index=13&t=195s&ab_channel=NicholasRenotte).
- LangChain covers the interaction with the OpenAI API and working with the user-uploaded file to generate the vector embeddings and Streamlit was used to generate a lightweight UI that facilitates interacting with the application.
### LangChain
- This project employs the LangChain *ecosystem* to add context to the OpenAI API. 
- The general workflow is as follows: 
    - The user uploads a PDF document that is saved to memory by PyPDFLoader. The document is broken into pages or more digestible chunks for the next few steps.
    - Then, the chunks are tokenized and embedded by Chroma. The vector embedding of the data allows us to pass the data as context to the model and allows us to perform mathematical operations to the data - such as cosine similarity, which allows us to find the most relevant sections of the PDF and display them to the user. 
    - Each of these components could be replaced by other services, for example, Pinecone for an online vector store. 
    - The results from the vectorstore search are passed to the LangChain vectorstore agent that converts the data into a better *aligned* or more humanlike response, using the OpenAI models. The vectorstore toolkit by LangChain renders the vectorstore generated from the PDF available as a *tool* to the model that it can use to generate its answers. 
### Streamlit
- Streamlit allows you to build incredibly lightweight UIs with shockingly few lines of code. It's got a variety of built in widgets like file upload and text input that seamlessly integrate together to form a clean interface.
- On any interaction by the user, Streamlit re-runs the entire python script from scratch and doesn't maintain state data across refreshes by default.
- Using the session state option and some basic control flow functions, I was able to add some necessary functionality to the app and hide certain components depending on the user action. For example, if the user has not uploaded any context document, they cannot make any queries.
- Moreover, through this form of state management, I ensure that the computationally intensive LangChain functions aren't rerun for every user input and instead only run once, when the document is uploaded.
- In terms of the visuals, I am using a free animation from Lottie that can be found [here](https://lottiefiles.com/143151-robot-futuristic-ai-animated).