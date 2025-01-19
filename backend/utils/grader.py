from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain import hub

class GraderUtils:
    def __init__(self, model):
        self.model = model

    def create_retrieval_grader(self):
        """
        Creates a retrieval grader that assesses the relevance of a retrieved document to a user question.

        Returns:
            A callable function that takes a document and a question as input and returns a JSON object with a binary score indicating whether the document is relevant to the question.
        """
        grade_prompt = PromptTemplate(
            template="""
            <|begin_of_text|><|start_header_id|>system<|end_header_id|>
            You are a grader assessing relevance of a retrieved document to a user question. \n 
            If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \n
            It does not need to be a stringent test. The goal is to filter out erroneous retrievals. \n
            Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question.
            Provide the binary score as a JSON with a single key 'score' and no preamble or explanation.
            <|eot_id|>
            <|start_header_id|>user<|end_header_id|>

            Here is the retrieved document: \n\n {document} \n\n
            Here is the user question: {question} \n
            <|eot_id|>
            <|start_header_id|>assistant<|end_header_id|>
            """,
            input_variables=["document", "question"],
        )

        # Create the retriever chain
        retriever_grader = grade_prompt | self.model | JsonOutputParser()

        return retriever_grader

    def create_hallucination_grader(self):
        """
        Creates a hallucination grader that assesses whether an answer is grounded in/supported by a set of facts.

        Returns:
            A callable function that takes a generation (answer) and a list of documents (facts) as input and returns a JSON object with a binary score indicating whether the answer is grounded in/supported by the facts.
        """

        system = """You are a grader assessing whether an LLM generation is grounded in / supported by a set of retrieved facts. \n 
                 Give a binary score 'yes' or 'no'. 'Yes' means that the answer is grounded in / supported by the set of facts.
                 Provide the binary score as a JSON with a single key 'score' and no preamble or explanation."""
        hallucination_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system),
                ("human", "Set of facts: \n\n {documents} \n\n LLM generation: {generation}"),
            ]
        )

        hallucination_grader = hallucination_prompt | self.model | JsonOutputParser()

        return hallucination_grader

    def answer_grader(self):
        """
        Creates a code evaluator that assesses whether the generated code is correct and relevant to the given question.

        Returns:
            A callable function that takes a generation (code), a question, and a list of documents as input and returns a JSON object with a binary score and feedback.
        """
        eval_template = PromptTemplate(
            template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are a grader assessing whether an answer addresses / resolves a question \n 
            Give a binary score 'yes' or 'no'. Yes' means that the answer resolves the question.
            Provide a JSON response with the following keys:

            'score': A binary score 'yes' or 'no' indicating whether the code is correct and relevant.
            'feedback': A brief explanation of your evaluation, including any issues or improvements needed.

            <|eot_id|><|start_header_id|>user<|end_header_id|>
            Here is the generated code:
            \n ------- \n
            {generation}
            \n ------- \n
            Here is the question: {question}
            \n ------- \n
            Here are the relevant documents: {documents}
            <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
            input_variables=["generation", "question", "documents"],
        )

        code_evaluator = eval_template | self.model | JsonOutputParser()

        return code_evaluator

    def create_question_rewriter(self):
        """
        Creates a question rewriter chain that rewrites a given question to improve its clarity and relevance.

        Returns:
            A callable function that takes a question as input and returns the rewritten question as a string.
        """
        system = """You a question re-writer that converts an input question to a better version that is optimized \n 
        for vectorstore retrieval. Look at the input and try to reason about the underlying semantic intent / meaning."""
        re_write_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system),
                (
                    "human",
                    "Here is the initial question: \n\n {question} \n Formulate an improved question.",
                ),
            ]
        )
        question_rewriter = re_write_prompt | self.model | StrOutputParser()

        return question_rewriter