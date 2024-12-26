import streamlit as st
from src.google_query import generate_google_res
from gemini_rag import model, generate_rag_response

# Define the Streamlit application
def main():
    st.title("RAG Chat Application")
    st.write("Welcome to the RAG Chat! Type your message below and press Enter.")
    
    # Store chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # User input box
    user_input = st.text_input("You:", key="user_input")
    
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append(("You", user_input))
        
        # Generate RAG response
        response = generate_rag_response(user_input, model) 
        # adding google response
        extended_response =  response + '\n' +generate_google_res(user_input)
        
        # Add RAG response to chat history
        st.session_state.messages.append(("Expert", extended_response))
        

    # Display chat history
    for speaker, message in st.session_state.messages:
        if speaker == "You":
            st.markdown(f"**{speaker}:** {message}")
        else:
            st.markdown(f"**{speaker}:** {message}")

# Run the Streamlit app
if __name__ == "__main__":
    main()
