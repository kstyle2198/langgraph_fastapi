import streamlit as st
from langserve import RemoteRunnable
from pprint import pprint
import time

st.title('Agent Test Server')
input_text = st.text_input('How can I help you?')

if input_text:
    with st.spinner("Processing..."):
        try:
            app = RemoteRunnable("http://localhost:8080/agent_chat/")
            config = {"recursion_limit": 3}
            for output in app.stream(input={"question": input_text}, config=config):
                for key, value in output.items():
                    # Node
                    pprint(f"Node '{key}':")
                    st.info(f"Node '{key}':")
                    # Optional: print full state at each node
                    # pprint.pprint(value["keys"], indent=2, width=80, depth=None)
                pprint("\n---\n")
            output = value['generation']  
            st.write(output)
        
        except Exception as e:
            st.error(f"Error: {e}")
        

# import streamlit as st
# from langserve import RemoteRunnable
# from pprint import pprint
# import asyncio
# import time

# # Set up the Streamlit app
# st.title("Test Server")

# # Input for user question
# input_text = st.text_input("How can I help you?")

# async def generate_output(input_text):
#     """
#     Generates output by streaming results from the RemoteRunnable.

#     Args:
#         input_text (str): User input text.

#     Yields:
#         str: Generated output text from the server.
#     """
#     app = RemoteRunnable("http://localhost:8000/agent_chat/")
#     config = {"recursion_limit": 3}

#     async for output in app.astream(input={"question": input_text}, config=config):
#         print(output)
#         print("="*70)
#         for key, value in output.items():
#             print(f"Node '{key}':")
#         print("\n---\n")
#         try:
#             yield value['generation']
#         except: pass

# async def process_input(input_text):
#     """
#     Processes the input text and streams results to the Streamlit interface.

#     Args:
#         input_text (str): User input text.
#     """
#     try:
#         # Stream the output using Streamlit's built-in streaming
#         with st.spinner("Processing..."):
#             async for output in generate_output(input_text):
#                 st.write(output)
#                 print(output, end="")
#     except Exception as e:
#         st.error(f"An error occurred: {e}")

# if input_text:
#     # Use Streamlit's asyncio support for running async functions
#     asyncio.run(process_input(input_text))
