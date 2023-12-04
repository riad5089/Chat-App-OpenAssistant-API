
import streamlit as st
from streamlit_chat import message
import os
from constants import HUGGINGFACEHUB_API_TOKEN

from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
# from hugchat import hugchat
from langchain import PromptTemplate,HuggingFaceHub,LLMChain
os.environ["HUGGINGFACEHUB_API_TOKEN"]=HUGGINGFACEHUB_API_TOKEN
st.set_page_config(page_title="OpenAssistant Powerd Chat App")

#sidebar
with st.sidebar:
    st.title('🤗💬 HuggingChat App')
    st.markdown('''
    ## About
    This app is an LLM-powered chatbot built using:
    - [Streamlit](https://streamlit.io/)
    - [LangChain](https://python.langchain.com/)
    - [OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5](https://huggingface.co/OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5) LLM model

    ''')

st.header("Your Personal Assistant 💬")

def main():

    # Generate empty lists for generated and user.
    ## Assistant Response
    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["I'm Assistant, How may I help you?"]

    ## user question
    if 'user' not in st.session_state:
        st.session_state['user'] = ['Hi!']
    # Layout of input/response containers

    response_container = st.container()
    colored_header(label='', description='', color_name='blue-30')
    input_container = st.container()

    # get user input
    def get_text():
        input_text = st.text_input("You: ", "", key="input")
        return input_text

    with input_container:
        user_input = get_text()

    def chain_setup():

        template = """<|prompter|>{question}<|endoftext|>
        <|assistant|>"""

        prompt = PromptTemplate(template=template, input_variables=["question"])

        llm = HuggingFaceHub(repo_id="OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5",
                             model_kwargs={"max_new_tokens": 1200})

        llm_chain = LLMChain(
            llm=llm,
            prompt=prompt
        )
        return llm_chain


    def generate_response(question, llm_chain):
        response = llm_chain.run(question)
        return response

    ## load LLM
    llm_chain = chain_setup()

    # main loop
    with response_container:
        if user_input:
            response = generate_response(user_input, llm_chain)
            st.session_state.user.append(user_input)
            st.session_state.generated.append(response)

        if st.session_state['generated']:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state['user'][i], is_user=True, key=str(i) + '_user')
                message(st.session_state["generated"][i], key=str(i))

if __name__ == '__main__':
    main()


#
# import streamlit as st
# from streamlit_chat import message
# import os
# from constants import HUGGINGFACEHUB_API_TOKEN
#
# from streamlit_extras.colored_header import colored_header
# from streamlit_extras.add_vertical_space import add_vertical_space
# # from hugchat import hugchat
# from langchain import PromptTemplate,HuggingFaceHub,LLMChain
# os.environ["HUGGINGFACEHUB_API_TOKEN"]=HUGGINGFACEHUB_API_TOKEN
# st.set_page_config(page_title="OpenAssistant Powerd Chat App")
#
# #sidebar
# with st.sidebar:
#     st.title('🤗💬 HuggingChat App')
#     st.markdown('''
#     ## About
#     This app is an LLM-powered chatbot built using:
#     - [Streamlit](https://streamlit.io/)
#     - [LangChain](https://python.langchain.com/)
#     - [OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5](https://huggingface.co/OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5) LLM model
#
#     ''')
#
# st.header("Your Personal Assistant 💬")
#
# def main():
#
#     # Generate empty lists for generated and user.
#     ## Assistant Response
#     if 'generated' not in st.session_state:
#         st.session_state['generated'] = ["I'm Assistant, How may I help you?"]
#
#     ## user question
#     if 'user' not in st.session_state:
#         st.session_state['user'] = ['Hi!']
#     # Layout of input/response containers
#
#     response_container = st.container()
#     colored_header(label='', description='', color_name='blue-30')
#     input_container = st.container()
#
#     # get user input
#     def get_text():
#         input_text = st.text_input("You: ", "", key="input")
#         return input_text
#
#     with input_container:
#         user_input = get_text()
#
#     def chain_setup():
#
#         template = """<|prompter|>{question}<|endoftext|>
#         <|assistant|>"""
#
#         prompt = PromptTemplate(template=template, input_variables=["question"])
#
#         llm = HuggingFaceHub(repo_id="OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5",
#                              model_kwargs={"max_new_tokens": 1200})
#
#         llm_chain = LLMChain(
#             llm=llm,
#             prompt=prompt
#         )
#         return llm_chain
#
#
#     def generate_response(question, llm_chain):
#         response = llm_chain.run(question)
#         return response
#
#     ## load LLM
#     llm_chain = chain_setup()
#
#     # main loop
#     with response_container:
#         if user_input:
#             response = generate_response(user_input, llm_chain)
#             st.session_state.user.append(user_input)
#             st.session_state.generated.append(response)
#
#         if st.session_state['generated']:
#             for i in range(len(st.session_state['generated'])):
#                 message(st.session_state['user'][i], is_user=True, key=str(i) + '_user')
#                 message(st.session_state["generated"][i], key=str(i))
#
# if __name__ == '__main__':
#     main()

# https://chat-app-openassistant-api-chbopxekfk2y2yb5nzpbpk.streamlit.app/
