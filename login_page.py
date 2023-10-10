import streamlit as st
import sqlite3
from passlib.hash import pbkdf2_sha256
import subprocess


# Create a connection to the SQLite database
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create a table to store user information (if it doesn't exist)
c.execute('''
          CREATE TABLE IF NOT EXISTS users 
          (id INTEGER PRIMARY KEY AUTOINCREMENT, 
          username TEXT, 
          email TEXT, 
          password TEXT)
          ''')
conn.commit()

st.set_page_config(page_title='TESLA Stock Analysis Login Page', page_icon=':chart_with_upwards_trend:')
custom_css = """
<style>
.zoom-text {
    font-family: 'Arial', sans-serif;
    font-size: 50px;
    text-align: center;
    position: relative;
    color: #ff4500; /* Tesla brand color */
    text-transform: uppercase;
    animation: zoom 5s infinite alternate ease-in-out;
    }

    @keyframes zoom {
        0% {
            transform: scale(1);
        }
        100% {
        transform: scale(1.1);
        }
    }
</style>
"""

# Display the zooming in and out title
st.markdown(custom_css, unsafe_allow_html=True)
st.markdown('<div class="zoom-text">TESLA Stock Analysis and Prediction</div>', unsafe_allow_html=True)


# Functions for database interactions
def create_user(username, email, password):
    hashed_password = pbkdf2_sha256.hash(password)
    c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, hashed_password))
    conn.commit()

def verify_user(username, password):
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    if user and pbkdf2_sha256.verify(password, user[3]):
        return True
    return False

# Selectbox for Login and Sign Up options
selection = st.selectbox("Select Option(sign up/login)", ["Login", "Sign Up"])

# Login Section
if selection == "Login":
    st.header("Login")
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        if verify_user(username, password):
            st.success(f'Welcome, {username}!')
            
            # Run shiny.py and display the output here
            subprocess.run(["streamlit", "run", "tesla.py"])
# Signup Section
else:
    st.header("Sign Up")
    new_username = st.text_input('Create Username')
    new_email = st.text_input('Email')
    new_password = st.text_input('Create Password', type='password')
    if st.button('Sign Up'):
        create_user(new_username, new_email, new_password)
        st.success(f'Account created for {new_username}! You can now login.')

# Close the database connection
conn.close()
