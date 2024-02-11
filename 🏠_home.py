import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.markdown("### Barbie Bell and KENoa")
st.markdown("#### A dynamic duo of elite personal trainer and nutritionist to help you meet your health goals!")
st.markdown("Hacklytics24 Submission by Elijah Nicpon, Julian Nogal, Emil Bajit, & Joshua Watkins")

with st.expander("Your Information", expanded=True):
    with st.form("Form"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            gender = st.selectbox("Gender", ['Select', 'Male', 'Female'])
        with col2:
            age = st.number_input("Age", step=1)
        with col3:
            weight = st.number_input("Weight (Lbs)", step=1)
        with col4:
            height = st.text_input("Height")

        # fitness_goals = st.text_area("What are your fitness goals TODO: examples!")
        # exercise_experience = st.text_area("What exercise experience do you have? TODO: examples!")
        # access_to_equipment = st.text_area("What sorts of exercise equipment do you have access to? TODO: examples!")
        # time_commitment = st.text_area("How often are you available to exercise?")
        preexisting_conditions = st.text_area("Do you have any preexisting medical conditions?")
        additional_information = st.text_area("Any additonal information you would like to have considered?")

        submitted = st.form_submit_button("Submit")
        if submitted:
            st.session_state["health_metrics"] = {
                "gender": gender,
                "age": age,
                "weight": weight,
                "height": height,
                # "fitness_goals": fitness_goals,
                # "exercise_experience": exercise_experience,
                # "access_to_equipment": access_to_equipment,
                # "time_commitment": time_commitment,
                "preexisting_conditions": preexisting_conditions,    
                "additional_info": additional_information
            }
            switch_page("Barbie Bell")