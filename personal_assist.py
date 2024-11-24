import google.generativeai as genai
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image

# Configure the Google Generative AI model
key = "AIzaSyB-7cKMdUpA5kTccpNxd72IT5CjeSgSmkc"
genai.configure(api_key=key)

# Initialize the generative AI model
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Function to generate responses based on the selected prompt
def assist_with_image(model, img, prompt_type):
    """
    Generate responses for assisting visually impaired individuals based on the provided image and prompt type.

    Args:
        model: The generative AI model object (e.g., genai.GenerativeModel).
        img: The input image to be analyzed.
        prompt_type: The type of prompt (1 to 5) for generating the response.

    Returns:
        str: The response generated by the model.
    """
    # Define prompts
    prompts = {
        "Object Recognition": '''Analyze the uploaded image. Identify all visible objects and describe each object, including its color, 
              shape, and possible purpose. Provide additional context on how these objects could be relevant for a visually 
              impaired individual in this setting.''',
        
        "Reading Labels or Text": '''From the uploaded image, extract and read any visible text, labels, or signs. Provide the text clearly 
              and explain its context or significance. For example, if it is a product label, describe the product details 
              and how it might be useful.''',
        
        "Environment Understanding": '''Analyze the uploaded image. Describe the overall environment, including the layout, objects, and any 
              potential obstacles or points of interest. Provide actionable suggestions for a visually impaired person 
              to navigate or interact with this environment safely.''',
        
        "Personalized Assistance": '''Examine the uploaded image and provide guidance for completing the task described below. For example, 
              if the task is to identify a specific object or understand a situation, explain what is visible and suggest 
              steps to achieve the task effectively.''',
        
        "Providing Task-Specific Information": '''Based on the uploaded image, assist with the following task: [Insert task description here, e.g., 
              'find a can of soup on a shelf' or 'identify the medication bottle with the name X']. Provide clear, 
              step-by-step guidance tailored for a visually impaired user.'''
    }

    # Check for valid prompt type
    if prompt_type not in prompts:
        return "Invalid prompt type. Please choose a valid prompt type."

    # Get the prompt for the given type
    prompt = prompts[prompt_type]

    # Generate content using the model
    response = model.generate_content([img, prompt])
    
    # Return the generated response
    return response.text

# Streamlit UI setup
st.set_page_config(
    page_title=" Visual Assistance AI",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Add custom CSS for styling
st.markdown("""
    <style>
    body {
        background-color: #f9f9f9;
    }
    .stApp {
        background-color: #ffffff;
        border: 1px solid #d6d6d6;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
    }
    .title-container {
        text-align: center;
    }
    .title-container h1 {
        font-family: 'Arial Black', Gadget, sans-serif;
        color: #0078d7;
    }
    .stButton > button {
        background-color: #0078d7;
        color: white;
        border-radius: 4px;
        padding: 10px 20px;
        border: none;
    }
    .stButton > button:hover {
        background-color: #005a9e;
    }
    </style>
""", unsafe_allow_html=True)

# Header section
st.markdown('<div class="title-container"><h1>Visual Assistance AI</h1></div>', unsafe_allow_html=True)
st.markdown("""
    Welcome to AI-powered application for assisting visually impaired individuals! 
    Upload an image, choose a prompt, and let our model generate helpful insights tailored for your needs.
""")

# Upload Image
uploaded_file = st.file_uploader("📤 Upload an Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open and display the uploaded image
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image")
    
    # Prompt selection
    st.subheader("🔍 Select Assistance Type")
    prompt_options = [
        "Object Recognition",
        "Reading Labels or Text",
        "Environment Understanding",
        "Personalized Assistance",
        "Providing Task-Specific Information"
    ]
    
    selected_prompt = st.selectbox("Select a Prompt", prompt_options)

    # Display the description of the selected prompt
    prompt_descriptions = {
        "Object Recognition": '''Analyze the uploaded image. Identify all visible objects and describe each object, including its color, 
              shape, and possible purpose. Provide additional context on how these objects could be relevant for a visually 
              impaired individual in this setting.''',
        
        "Reading Labels or Text": '''From the uploaded image, extract and read any visible text, labels, or signs. Provide the text clearly 
              and explain its context or significance. For example, if it is a product label, describe the product details 
              and how it might be useful.''',
        
        "Environment Understanding": '''Analyze the uploaded image. Describe the overall environment, including the layout, objects, and any 
              potential obstacles or points of interest. Provide actionable suggestions for a visually impaired person 
              to navigate or interact with this environment safely.''',
        
        "Personalized Assistance": '''Examine the uploaded image and provide guidance for completing the task described below. For example, 
              if the task is to identify a specific object or understand a situation, explain what is visible and suggest 
              steps to achieve the task effectively.''',
        
        "Providing Task-Specific Information": '''Based on the uploaded image, assist with the following task: [Insert task description here, e.g., 
              'find a can of soup on a shelf' or 'identify the medication bottle with the name X']. Provide clear, 
              step-by-step guidance tailored for a visually impaired user.''',
    }

    # Show the description based on selected prompt
    st.text_area("Prompt Description", prompt_descriptions[selected_prompt], height=200)

    # Button to generate response
    if st.button("✨ Generate Assistance"):
        with st.spinner("Generating response..."):
            response_text = assist_with_image(model, img, selected_prompt)
        st.success("Response Generated!")
        st.subheader("📝 Generated Response")
        st.write(response_text)

else:
    st.info("Please upload an image to get started.")
