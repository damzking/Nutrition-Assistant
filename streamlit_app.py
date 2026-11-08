import os

import requests
import streamlit as st


DEFAULT_API_URL = "http://127.0.0.1:5000"
UPLOAD_ENDPOINT = "/api/upload-image"
REQUEST_TIMEOUT_SECONDS = 90


def show_analysis(analysis):
    if not analysis["is_food"]:
        st.warning("No identifiable food or drink was found in this image.")
    else:
        st.subheader("Nutrition estimate")
        calories, protein, carbs, fat = st.columns(4)
        calories.metric("Calories", f'{analysis["calories_kcal"]} kcal')
        protein.metric("Protein", f'{analysis["protein_g"]} g')
        carbs.metric("Carbohydrates", f'{analysis["carbs_g"]} g')
        fat.metric("Fat", f'{analysis["fat_g"]} g')

        st.subheader("Identified items")
        for item in analysis["items"]:
            st.write(f"- {item}")

    st.info(analysis["health_note"])
    st.caption("Nutrition values are approximate estimates.")


st.set_page_config(page_title="Food & Nutrition Analyser", page_icon="🥗")
st.title("Food & Nutrition Analyser")
st.write("Upload a meal photo to estimate its calories and macronutrients.")

api_base_url = st.sidebar.text_input(
    "Flask API address",
    value=os.getenv("FLASK_API_URL", DEFAULT_API_URL),
).strip().rstrip("/")
uploaded_image = st.file_uploader(
    "Choose a food image",
    type=["jpg", "jpeg", "png"],
)

if uploaded_image is not None:
    st.image(uploaded_image, caption=uploaded_image.name, use_container_width=True)

if st.button("Analyse image", disabled=uploaded_image is None):
    if not api_base_url:
        st.error("Enter the address where the Flask API is running.")
    else:
        endpoint = f"{api_base_url}{UPLOAD_ENDPOINT}"
        files = {
            "file": (
                uploaded_image.name,
                uploaded_image.getvalue(),
                uploaded_image.type or "application/octet-stream",
            )
        }

        try:
            with st.spinner("Analysing your image..."):
                response = requests.post(
                    endpoint,
                    files=files,
                    timeout=REQUEST_TIMEOUT_SECONDS,
                )
        except requests.RequestException as error:
            st.error(
                "Could not reach the Flask API. Check that Flask is running "
                f"and the API address is correct. Details: {error}"
            )
        else:
            try:
                result = response.json()
            except ValueError:
                st.error(
                    f"Flask returned an invalid response (HTTP {response.status_code})."
                )
            else:
                if not isinstance(result, dict):
                    st.error("Flask returned an unexpected response.")
                elif not response.ok:
                    error_message = result.get("error")
                    st.error(
                        error_message
                        if isinstance(error_message, str)
                        else "The image analysis failed."
                    )
                else:
                    analysis = result.get("analysis")
                    required_fields = {
                        "is_food",
                        "items",
                        "calories_kcal",
                        "protein_g",
                        "carbs_g",
                        "fat_g",
                        "health_note",
                    }
                    if (
                        not isinstance(analysis, dict)
                        or not required_fields.issubset(analysis)
                    ):
                        st.error("Flask returned an incomplete nutrition analysis.")
                    else:
                        st.success(
                            result.get("message", "Image analysed successfully.")
                        )
                        show_analysis(analysis)
