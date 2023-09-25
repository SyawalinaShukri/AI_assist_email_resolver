import os
import re
import openai
import streamlit as st

# Access the OpenAI API key from the secrets.toml file
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Set the API key for OpenAI
openai.api_key = openai_api_key

#def 1
def summarize_key_problems(msg):
    instructions = """
    "Highlight key problems in a concise three-point summary."
    """

    example_output="""
    1.Fraudulent Activity: The customer has detected unauthorized transactions on their account, indicating possible fraud.
    2.Account Security: The customer's account security has been compromised, and immediate action is needed to investigate and rectify the situation.
    3.Resolution Request: The customer is requesting that the company freeze their account, investigate the unauthorized transactions, reverse any fraudulent charges, and enhance the account's security.

    """
    response1 = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that helps analyze the email's content. List the key problems."
            },
            {
                "role": "user",
                "content": instructions
            },
            {
                "role": "assistant",
                "content": example_output
            },
            {
                "role": "user",
                "content": msg
            }
        ],
        max_tokens=1000,
        temperature=0.2
    )

    return response1.choices[0].message['content']

#def 2
def identify_relevant_departments(msg):
    instructions2 = """
    "Identify the relevant department[s] responsible for solving the key problems."
    """

    example_output2 = """
    1.Quality Control Department: Responsible for investigating product quality issues.
    2.Refund Processing Department: Responsible for processing refunds.
    3.Customer Experience Team: Responsible for coordinating the resolution process and communicating with the customer.    
    """

    response2 = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that helps analyze the email's content. List relevant department[s]."
            },
            {
                "role": "user",
                "content": instructions2
            },
            {
                "role": "assistant",
                "content": example_output2
            },
            {
                "role": "user",
                "content": msg
            }
        ],
        max_tokens=1000,
        temperature=0.2
    )

    return response2.choices[0].message['content']


#def3

def generate_customized_email(msg, selected_department):
    instructions3 = """
    "Please analyze the email that has been sent to the customer service team and generate a customized email in text containing the identified customer's issues and recommended solutions, ready to be sent to the selected department."
    """

    # Create a template for the customized email
    email_template = f"""
    Customized Email to {selected_department}:
    
    Dear {selected_department} Team,

    I would like to bring to your attention a customer inquiry that requires your assistance. Here are the details:

    Customer Information:
    
    Customer's Issues:

    Recommended Solutions:

    Timelines and Updates:

    Please review this information and take appropriate action to address the customer's concerns.

    Best regards,
    Customer Service Team
    """

    response3 = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that helps with customer support inquiries. Please provide a customized email about the customer to the selected_department"
            },
            {
                "role": "user",
                "content": instructions3
            },
            {
                "role": "assistant",
                "content": email_template
            }
        ],
        max_tokens=1000,
        temperature=0.6
    )

    return response3.choices[0].message['content']


#def4

def generate_personalized_email(msg):
    instructions4 = """
    "Please analyze the email that has been sent to the customer service team and generate a personalized email in text for the client to acknowledge their concerns and assure them that the issues are being addressed, while allowing the team some time to resolve them satisfactorily."
    """
  
    example_output4 = """
    Personalized Email to Customer: [Personalized email content]
    """
    response4 = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that helps with customer support inquiries. Please provide a concise response and prioritize customer satisfaction."
            },
            {
                "role": "user",
                "content": instructions4
            },
            {
                "role": "assistant",
                "content": example_output4
            },
            {
                "role": "user",
                "content": msg
            }
        ],
        max_tokens=1000,
        temperature=0.6
    )

    return response4.choices[0].message['content']


#def 5

def extract_departments(text):
    # Define a regular expression pattern to match department names
    pattern = r'^([^:]+):'
    
    # Use re.findall to extract department names
    department_names = re.findall(pattern, text, re.MULTILINE)
    
    # Exclude the first line if it exists
    if department_names:
        department_names = department_names[1:]
    
    return department_names


# Define custom CSS style for the title
title_style = """
    font-size: 48px;
    font-weight: bold;
    color: #006400; /* Dark Green */
    text-align: center;
    text-transform: uppercase;
    margin-bottom: 20px;
"""

# Create the title with the custom style
st.markdown(
    f'<h1 style="{title_style}">AI-Assist Email Resolver</h1>',
    unsafe_allow_html=True
)


# Step 1: User input for the customer's email
st.sidebar.title("Issue/Request:")
customer_email = st.sidebar.text_area("Enter the customer's email text:")

# Initialize session state
if 'problems' not in st.session_state:
    st.session_state.problems = None
if 'departments' not in st.session_state:
    st.session_state.departments = None

# Step 2: Generate problems and departments using def1 and def2
if st.sidebar.button("Analyze email"):
    st.session_state.problems = summarize_key_problems(customer_email)
    st.session_state.departments = identify_relevant_departments(customer_email)

if st.session_state.problems:
    st.header("Key Problems:")
    st.write(st.session_state.problems)

if st.session_state.departments:
    st.header("Relevant Departments:")
    st.write(st.session_state.departments)

# Ensure that st.session_state.departments is a string before using it with regular expressions
if isinstance(st.session_state.departments, str):
    department_list = extract_departments(st.session_state.departments)
else:
    department_list = []

# Step 3: Dropdown for department selection
selected_department = st.sidebar.selectbox("Select a department or the client:", ["Client"] + department_list)

# Step 4: Generate customized or personalized email using def3 or def4
if selected_department != "Client":
    if st.sidebar.button("Generate Email"):
        if selected_department in st.session_state.departments:
            customized_email = generate_customized_email(customer_email,selected_department)
            st.header(f"Customized Email for {selected_department} Team:")
            st.write(customized_email)
        else:
            st.warning("Invalid department selection.")
else:
    if st.sidebar.button("Generate Email"):
        personalized_email = generate_personalized_email(customer_email)
        st.header("Personalized Email for the Client:")
        st.write(personalized_email)
