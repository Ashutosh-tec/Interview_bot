import streamlit as st
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
        
        # Add RAG response to chat history
        st.session_state.messages.append(("Expert", response))
        
        # Clear the input field after submission
        # st.session_state.user_input = ""  # This clears the value, not the widget itself

    # Display chat history
    for speaker, message in st.session_state.messages:
        if speaker == "You":
            st.markdown(f"**{speaker}:** {message}")
        else:
            st.markdown(f"**{speaker}:** {message}")

# Run the Streamlit app
if __name__ == "__main__":
    main()
