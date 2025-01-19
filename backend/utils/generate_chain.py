# generate_chain.py
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def create_generate_chain(llm):
    """
    Creates a generate chain for answering code-related questions.

    Args:
        llm (LLM): The language model to use for generating responses.

    Returns:
        A callable function that takes a context and a question as input and returns a string response.
    """

    generate_template = """
    You are a smart AI assistant. 
    Use the following pieces of retrieved context to answer the question. 
    Generate detailed answer including specified numbers, fomulas in the point of technical specifications. 
    If you don't know the answer, just say that you don't know. Do NOT try to make up an answer.
    If the question is not related to the context, politely respond that you only answer questions related to the context.

    <context>
    {context}
    </context>

    <question>
    {question}
    </question>
    """

    generate_prompt = PromptTemplate(template=generate_template, input_variables=["context", "question"])

    # Create the generate chain
    generate_chain = generate_prompt | llm | StrOutputParser()

    return generate_chain