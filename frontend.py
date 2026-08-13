import streamlit as st
import requests

st.set_page_config(page_title="1 REP MAX OPTIMIZER")
st.title("1RM Calculator & OPTIMIZER")

st.divider()
st.subheader("Calculate Your 1RM")

exercise = st.selectbox(
    "Select Exercise", ["Bench Press", "Squat", "Deadlift"])

weight = st.number_input("Weight Lifted (lbs)",
                         min_value=0.0, value=0.0, step=5.0)
reps = st.number_input("Reps Performed", min_value=1,
                       max_value=20, value=1, step=1)

if st.button("Calculate & Save"):
    api_url = f"http://127.0.0.1:8000/calculate-1rm?exercise={exercise}&weight={weight}&reps={reps}"

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()

            st.success(
                f"Your Estimated One Rep Max is {data['one_rep_max']:.2f} lbs")
            st.info(data['status'])
        else:
            st.error("An Error Occurred")

    except requests.exceptions.ConnectionError:
        st.error("An error occurred tring to connect to API")


st.divider()
st.subheader("Target Rep Optimizer")
st.write("Find the best weight and reps for your next session based on your estimated 1RM")

min_reps = st.number_input("Minimum Target Reps",
                           min_value=1, max_value=19, value=6, step=1)
max_reps = st.number_input("Maximum Target Reps",
                           min_value=2, max_value=20, value=12, step=1)

has_small_plates = st.checkbox("I have 1.25lb plates")

if st.button("Calculate"):

    optimizer_url = f"http://127.0.0.1:8000/calculate-optimal-set?weight={weight}&reps={reps}&min_reps={min_reps}&max_reps={max_reps}&has_small_plates={has_small_plates}"

    try:
        response = requests.get(optimizer_url)

        if response.status_code == 200:
            data = response.json()

            if data['best_weight'] == weight and data['best_reps'] == reps:
                st.warning(
                    "No better set found within preferred rep range. \nConsider adjusting your rep range or using smaller plates if available.")
            else:
                st.success(
                    f"Next time try: {data['best_weight']} lbs for {data['best_reps']} reps.")

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to backend.")

st.divider()
st.subheader("Workout History")

if st.button("LOAD HISTORY"):

    history_url = "http://127.0.0.1:8000/history"

    response = requests.get(history_url)

    data = response.json()

    st.dataframe(data["history"])
