import xml.etree.ElementTree as ET
import streamlit as st
import anthropic
import os

st.set_page_config(page_title="AI Agents Talk", page_icon="👽")

# Anthropic API key setting
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

MODEL = "claude-3-7-sonnet-20250219"
# MODEL = "claude-3-5-haiku-20241022"

def read_prompt_from_xml(file_path):
    """Read the system prompt from an XML file"""
    tree = ET.parse(file_path)
    root = tree.getroot()
    return root.text.strip()

def generate_response(agent_name, system_prompt, messages, conversation_container):
    """Generate a streamed response from the Claude model"""
    try:
        empty_text = conversation_container.empty()
        full_response = ""
        
        # Get response in streaming mode
        with client.messages.stream(
            model=MODEL,
            system=system_prompt,
            messages=messages,
            max_tokens=1000,
        ) as stream:
            for text in stream.text_stream:
                full_response += text
                empty_text.markdown(full_response)
                
        return full_response
    except Exception as e:
        st.error(f"Error generating response from {agent_name}: {e}")
        return None

def generate_conclusion(conversation_history, user_question):
    """Generate the final conclusion from the conversation"""
    try:
        system_prompt = "You are an expert on the AI Agents Talk, capable of analyzing agent conversations to draw clear conclusions.you have to summarize the conversation in user's language and provide a final conclusion."

        # Prompt to generate conclusion from conversation history
        messages = [
            {
                "role": "user", 
                "content": f"The following is a conversation between Agent-1 and Agent-2 regarding the user's question '{user_question}'.\n\n"
                           f"{conversation_history}\n\n"
                           f"Please summarize the key points of this conversation and provide a final conclusion in 3-5 sentences."
            }
        ]
        
        response = client.messages.create(
            model=MODEL,
            system=system_prompt,
            messages=messages,
            max_tokens=777,
        )
        
        return response.content[0].text
    except Exception as e:
        st.error(f"Error generating conclusion: {e}")
        return "Could not generate the conclusion of the conversation."

def conduct_agent_conversation(user_question, conversation_container, max_turns=5):
    """Generate a conversation between agents (real-time display)"""
    # Read system prompts once
    prompts = {
        "Agent-1": read_prompt_from_xml("prompt/Agent-1.xml"),
        "Agent-2": read_prompt_from_xml("prompt/Agent-2.xml")
    }
    
    # Define agent information in a dictionary
    agents = {
        "Agent-1": {"icon": "👨‍💼", "prompt": prompts["Agent-1"]},
        "Agent-2": {"icon": "👩‍⚕️", "prompt": prompts["Agent-2"]}
    }
    
    # Start of conversation (always with Agent-1)
    current_agent = "Agent-1"
    last_agent = None
    last_response = None
    conversation_history = ""
    
    for turn in range(max_turns):
        # Get current agent information
        agent_info = agents[current_agent]
        
        # Prepare messages
        if turn == 0:  # First turn
            agent_messages = [{"role": "user", "content": f"Please provide your initial thoughts on the following question. If you determine the conversation has converged, please respond with 'End of conversation': {user_question}"}]
        else:  # From the second turn onwards
            agent_messages = [
                {"role": "user", "content": f"Question: {user_question}\n\n{last_agent}'s opinion: {last_response}\n\nPlease share your response to this."}
            ]
        
        # Generate response (streaming display)
        with conversation_container:
            st.markdown(f"**{agent_info['icon']} {current_agent}:**")
            agent_response = generate_response(current_agent, agent_info["prompt"], agent_messages, conversation_container)
            
            # Add to conversation history
            conversation_history += f"{current_agent}: {agent_response}\n\n"
            
            if "End of conversation" in agent_response:
                # If the conversation ends, generate and display the conclusion
                conclusion = generate_conclusion(conversation_history, user_question)
                st.markdown("---")
                st.markdown(f"### 🔍 Conclusion of the Conversation")
                st.markdown(f"<div style='background-color: #f0f7ff; padding: 15px; border-radius: 10px; border-left: 5px solid #1E90FF;'>{conclusion}</div>", unsafe_allow_html=True)
                return
        
        # Save current response and speaker
        last_response = agent_response
        last_agent = current_agent
        
        # Set the next agent
        current_agent = "Agent-2" if current_agent == "Agent-1" else "Agent-1"
    
    # Generate conclusion if maximum number of turns is reached
    conclusion = generate_conclusion(conversation_history, user_question)
    with conversation_container:
        st.markdown("---")
        st.markdown(f"### 🔍 Conclusion of the Conversation")
        st.markdown(f"<div style='background-color: #f0f7ff; padding: 15px; border-radius: 10px; border-left: 5px solid #1E90FF;'>{conclusion}</div>", unsafe_allow_html=True)

# Streamlit app settings
st.title("AI Agents Talk")
st.markdown("Two AI agents engage in a discussion to answer the user's question.")

# User input
user_question = st.text_area("Enter your question:", height=100)

# Start conversation button
if st.button("Start Conversation"):
    if user_question:        
        # Create conversation container
        conversation_container = st.container()
        
        # Start conversation
        conduct_agent_conversation(user_question, conversation_container)
    else:
        st.warning("Please enter a question.")
