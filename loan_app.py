import streamlit as st 
import pandas as pd 
import numpy as np 
import pickle

import base64

# Caching mechanism that allows the app to stay perfomant
@st.cache_resource ()
def get_fvalue (val, feature_dict) :
    for key, value in feature_dict.items () :
        if val == key :
            return value

@st.cache_data ()
def get_value (val, dict) :
    for key, value in dict.items () :
        if val == key :
            return value

app_mode = st.sidebar.selectbox ('Select Page', ['Home', 'Prediction'])

if app_mode == 'Home' :
    st.title ('Loan Prediction :')
    st.image ('loan_image.jpg')
    st.markdown ('Dataset :')
    data = pd.read_csv ('loan_dataset.csv')
    st.write (data.head ())
    st.markdown ('Applicant Income Vs. Loan Amount')
    st.bar_chart (data [['ApplicantIncome', 'LoanAmount']].head (20))
elif app_mode == 'Prediction' :
    st.image ('slider-short-1.png')
    st.subheader ('Sir/Mme, YOU need to fill all necessaty informations in order to get a loan request !')
    st.sidebar.header ("Information about the client :")
    gender_dict = {
        'Male' : 1,
        'Female' : 2
    }
    feature_dict = {
        'No' : 1,
        'Yes' : 2
    }
    edu = {
        'Graduate' : 1,
        'Not Graduate' : 2
    }
    prop = {
        'Rural' : 1,
        'Urban' : 2,
        'Semiurban' : 3
    }
    feature_dict = {
        'No' : 1,
        'Yes' : 2
    }
    dependents_dict = {
        '0' : 0.0,
        '1' : 1.0,
        '2' : 2.0,
        '3+' : 3.0
    }
    Gender = st.sidebar.radio ('Gender', tuple(gender_dict.keys ()))
    Married = st.sidebar.radio ('Married', tuple (feature_dict.keys ()))
    Dependents = st.sidebar.radio ('Dependents', options = ['0', '1', '2', '3+'])
    Education = st.sidebar.radio ('Education', tuple (edu.keys ()))
    Self_Employed = st.sidebar.radio ('Self Employed', tuple (feature_dict.keys ()))
    ApplicantIncome = st.sidebar.slider ('ApplicantIncome', 0,10000,0)
    CoapplicantIncome = st.sidebar.slider ('CoapplicantIncome', 0,10000,0)
    LoanAmount = st.sidebar.slider ('LoanAmount in K$', 9.0,700.0,200.0)
    Loan_Amount_Term = st.sidebar.selectbox ('Loan_Amount_Term', (12.0,36.0,60.0,84.0,120.0,180.0,240.0,300.0,360.0))
    Credit_History = st.sidebar.radio ('Credit_History', (0.0,1.0))
    Property_Area = st.sidebar.radio ('Property Area', tuple (prop.keys ()))
    Total_Income = st.sidebar.slider('Total_Income', 0, 20000, (ApplicantIncome + CoapplicantIncome))

    class_0, class_1, class_2, class_3 = 0, 0, 0, 0
    if Dependents == '0' :
        class_0 = 1
    elif Dependents == '1' :
        class_1 = 1
    elif Dependents == '2' :
        class_2 = 1
    else :
        class_3 = 1

    Gender_Male, Gender_Female = 0, 0
    if Gender == 'Male' :
        Gender_Male = 1
    else :
        Gender_Female = 1

    Married_No, Married_Yes = 0, 0
    if Married == 'No' :
        Married_No = 1
    else :
        Married_Yes = 1

    Education_Graduate, Education_NotGraduate = 0,0
    if Education == 'Graduate' :
        Education_Graduate = 1
    else :
        Education_NotGraduate = 1

    Self_Employed_Yes, Self_Employed_No = 0, 0
    if Self_Employed == 'No' :
        Self_Employed_No = 1
    else :
        Self_Employed_Yes = 1

    Property_Area_Rural, Property_Area_Urban, Property_Area_Semiurban = 0, 0, 0
    if Property_Area == 'Urban' :
        Property_Area_Urban = 1
    elif Property_Area == 'Semiurban' :
        Property_Area_Semiurban = 1
    else :
        Property_Area_Rural = 1

    data1 = {
        'Gender' : [Gender_Female, Gender_Male],
        'Married' : [Married_No, Married_Yes],
        'Education' : [Education_Graduate, Education_NotGraduate],
        'Self Employed' : [Self_Employed_No, Self_Employed_Yes],
        'Property_Area' : [Property_Area_Rural, Property_Area_Urban, Property_Area_Semiurban]
    }

    feature_list = [
        get_fvalue (Dependents, dependents_dict), ApplicantIncome, CoapplicantIncome, LoanAmount,
        Loan_Amount_Term, Credit_History, Total_Income, data1 ['Gender'][0], data1 ['Gender'][1],
        data1 ['Married'][0], data1 ['Married'][1], data1 ['Education'][0], data1 ['Education'][1],
        data1 ['Self Employed'][0], data1 ['Self Employed'][1],
        data1 ['Property_Area'][0], data1 ['Property_Area'][1], data1 ['Property_Area'][2]
    ]
    single_sample = np.array (feature_list).reshape (1, -1)

    if st.sidebar.button("Predict"):
        file_ = open("6m-rain.gif", "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()
        file = open("green-cola-no.gif", "rb")
        contents = file.read()
        data_url_no = base64.b64encode(contents).decode("utf-8")
        file.close()
        loaded_model = pickle.load(open('Random_Forest.sav', 'rb'))
        prediction = loaded_model.predict(single_sample)
        print (prediction [0])
        if prediction[0] == 'N' :
            st.error(    'According to our Calculations, you will not get the loan from Bank'    )
            st.markdown(    f'<img src="data:image/gif;base64,{data_url_no}" alt="cat gif">',    unsafe_allow_html=True,)
        elif prediction[0] == 'Y' :
            st.success(    'Congratulations!! you will get the loan from Bank'    )
            st.markdown(    f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',    unsafe_allow_html=True,    )

st.markdown ('Made by H. Moustapha Ousmane'
)
