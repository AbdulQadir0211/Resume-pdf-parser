import PyPDF2
from langchain import LLMChain, PromptTemplate
from langchain import LLMChain, PromptTemplate, OpenAI
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import streamlit as st

def read_pdf(file_path):
    try:
        # Open the PDF file
        with open(file_path, 'rb') as file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfFileReader(file)
            
            # Initialize a variable to store the content
            content = ""
            
            # Iterate through all the pages and extract text
            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                content += page.extractText()
            
            return content
    except Exception as e:
        return f"An error occurred: {e}"


prompt_template = PromptTemplate(
    input_variables=["pdf_content"],
    template="""
    You are an AI assistant that takes PDF content as input and parses its content into a structured JSON format. 
    The JSON should include fields such as Name, Contact Information, Summary, Education, Work Experience, Skills, and Certifications. 
    Please parse the following PDF content:

    {pdf_content}

    Output the parsed content in the following JSON structure:

    {{
      "name": "John Doe",
      "contact_information": {{
        "email": "john.doe@example.com",
        "phone": "+123456789",
        "address": "1234 Elm Street, City, State, ZIP"
      }},
      "summary": "Experienced software developer with a strong background in AI and machine learning...",
      "education": [
        {{
          "degree": "Bachelor of Science in Computer Science",
          "institution": "University Name",
          "year": "2020"
        }}
      ],
      "work_experience": [
        {{
          "position": "Software Engineer",
          "company": "Tech Company",
          "duration": "Jan 2021 - Present",
          "responsibilities": [
            "Developed and maintained web applications...",
            "Collaborated with cross-functional teams..."
          ]
        }}
      ],
      "skills": [
        "Python",
        "Machine Learning",
        "Data Analysis"
      ],
      "certifications": [
        {{
          "name": "Certified Machine Learning Specialist",
          "issuing_organization": "Certification Body",
          "year": "2021"
        }}
      ]
    }}
    """
)


llm = OpenAI(api_key="your_openai_api_key")  # Replace with your OpenAI API key
chain = LLMChain(prompt_template=prompt_template, llm=llm)

'''# Load the Gemma model from Hugging Face
Uncomment if you want to check for open source llms
model_name = "google/gemma-2-27b-it" 
tokenizer = AutoTokenizer.from_pretrained(model_name)
llm = AutoModelForCausalLM.from_pretrained(model_name)'''

# Use the chain to parse the PDF content
parsed_content = chain.run(pdf_content=pdf_content)


st.title("PDF Content Parser using LangChain and Hugging Face Models")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Read the uploaded PDF file
    pdf_content = read_pdf(uploaded_file)

    # Display the PDF content
    st.subheader("PDF Content")
    st.text(pdf_content)

    # Parse the PDF content
    with st.spinner('Parsing PDF content...'):
        parsed_content = chain.run(pdf_content=pdf_content)
    
    # Display the parsed content
    st.subheader("Parsed Content")
    st.json(parsed_content)

