##import all the required libs

import base64
import sqlite3 
import streamlit as st 
import pandas as pd 
import matplotlib
matplotlib.use('Agg')
import seaborn as sns 
import pickle
import joblib
import matplotlib.pyplot as plt
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
tfidf = TfidfVectorizer()
clf = LinearSVC()
import spacy
from spacy import displacy
nlp = spacy.load("en_core_web_sm")
HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.0rem; padding: 1rem">{}</div>"""

# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

#DB Managment

conn = sqlite3.connect('data1.db')
c = conn.cursor()
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable (username TEXT, password TEXT)')
    
def add_userdata(username, password):
    c.execute('INSERT INTO userstable (username,password) VALUES (?,?)', (username, password))
    conn.commit()

def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username = ? AND password = ?', (username, password))
    data = c.fetchall()
    return data

def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data

pipe = joblib.load(open('modelSVM.pkl','rb'))


def predict_(docx):
	results = pipe.predict([docx])
	return results[0]

def analyze_text(x):
    return nlp(x)

##Creating the frontend
##login page

def main():
    st.title("IOTE Classzo")
    menu = ["Home","Login","SignUp"]
    choice = st.sidebar.selectbox("Menu",menu)
    if choice == 'Home':
        st.subheader('Welcome to IOTE')
        st.write('With the Internet of Things taking over human lives, automation has made lives simpler and homes smarter. Smart homes are the base to smart cities and a much secure lifestyle. It is a connected home technology that is designed to automate functions and grant you control over the property.The home control mechanism gives you access to control the security of the house. It works on mobile application control, which can be integrated with the security systems installed. You can set a schedule, and the rest is automated, based on your personal preferences. It is convenient, also giving you total control and hence a financially economical solution, with an overall smarter home.Home automation can also alert you to events that you might want to know about if you are not around at that time, for instance, an unexpected water leak, a lit bulb, a  running A/C and more')
        st.write('for more information refer to www.ioteverythin.com')
    elif choice == 'Login':
        st.subheader('Login Section')

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password",type='password')
        if st.sidebar.checkbox("Login"):
            hashed_pswd = make_hashes(password)
            result = login_user(username,check_hashes(password,hashed_pswd))

            if result:
                st.success("Logged In as {}".format(username))
                st.title(" News Classifier and NER")
                activties = ["Predictor", "About"]
                choice = st.sidebar.selectbox("Options", activties)


    

                if choice == "Predictor":
                    st.subheader("Built with TRUST")
                    with st.form(key='mlform'):
                        raw_text = st.text_area("News")
                        submit_message = st.form_submit_button(label='Classify') 


                        if submit_message:
                            col1,col2  = st.columns(2)
                            prediction = predict_(raw_text)
                            with col1:
                                st.success('Original Text')
                                st.write(raw_text)

                            st.success('Prediction')
                            st.write("{}".format(prediction))

                            with col2:
                                st.success('Entity Recognition')
                                docx = analyze_text(raw_text)
                                html = displacy.render(docx,style='ent')
                                html = html.replace("\n\n","\n")
                                st.write(HTML_WRAPPER.format(html),unsafe_allow_html=True)


                 ## Creating the about us page
                if choice =='About':
                    st.write('Thank you')
                    st.write('Built by Joel and Joshua')
                    
                    
                    #elif task == "Profiles":
                            #st.subheader("User Profiles")
                            #user_result = view_all_users()
                            #clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
                            #st.dataframe(clean_db)


            else:

                st.warning("Incorrect Username/Password")

    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password",type='password')
        
        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user,make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")








if __name__ == '__main__':
    main()
