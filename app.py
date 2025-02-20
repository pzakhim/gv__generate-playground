import json
import time
import traceback
import streamlit as st
from copy import deepcopy

#############################################

SYSTEM_ASSIGNED_ROLE = "Assigned model system ..."
PROMPT_REQUIREMENTS = "Your requirements ..."
OUTPUT_REQUIREMENTS = "Your output format ..."
USER_REQUEST = "Your prompt ..."

OPENAI_API_KEY = "your_api_key"
MODEL_CONFIG = {
    "model_name": "gpt-4o-mini",
    "max_tokens": 256,
    "n": 1,
    "top_p": 1.0,
    "temperature": 0.0,
    "presence_penalty": 0.0,
    "frequency_penalty": 0.0,
}

MONGODB_URI = "your_mongodb_uri"
DATABASE_NAME = "your_database_name"
COLLECTION_NAME = "your_collection_name"

############### APP STREAMLIT ###############


st.set_page_config(
    page_title="Generate Playground",
    page_icon="🌟",
    layout="wide",
)  # Turn on wide layout mode for Playground screen
st.title("Playground For Model Generative AI")  # Title Playground

layout_left, layout_right = st.columns([5, 2])  # Split screen into 2 frame/layout

# USER PLAYGROUND LAYOUT SECTION
with layout_left:
    # SECTION 1: System assignment
    st.subheader("Generate recommendation")
    system_content = ""
    user_content = ""
    with st.chat_message("ai"):
        assume_role = st.text_area(
            "System Assigned Role", SYSTEM_ASSIGNED_ROLE, height=150
        )
        prompt_requirements = st.text_area(
            "Prompt requirements", PROMPT_REQUIREMENTS, height=600
        )

        output_requirements = st.text_area(
            "Output requirements", OUTPUT_REQUIREMENTS, height=250
        )
        system_content = f"{assume_role}\n{prompt_requirements}\n{output_requirements}"
        update_field, response_field = st.columns([2, 4])
        with update_field:
            update = st.button("Update system")
    #             if update:
    #                 try:
    #                     update_system_content(
    #                         system_content_collection,
    #                         assume_role,
    #                         prompt_requirements,
    #                         output_requirements,
    #                         # hotel_information,
    #                     )
    #                     with response_field:
    #                         st.success("System content updated successfully in mongoDB.")
    #                 except Exception as e:
    #                     with response_field:
    #                         st.error(f"Summary Error: {e}")

    # SECTION 2: User request
    with st.chat_message("human"):
        user_request = st.text_area("User request to OpenAI", USER_REQUEST, height=750)
        #
        update_field, response_field = st.columns([2, 4])
        with update_field:
            update = st.button("Update request")

            # if update:
    #                 try:
    #                     update_user_content(
    #                         user_content_collection, hotel_information, "", user_requirement
    #                     )
    #                     with response_field:
    #                         st.success("User content updated successfully in mongoDB.")
    #                 except Exception as e:
    #                     with response_field:
    #                         st.error(f"Summary Error: {e}")

    # SECTION 3: Model response
    if st.button("Generate ..."):
        st.write("Starting...")
        # try:
#             start = time.time()
#             print("Starting...")
#             output, tokens = openai_response(user_content, system_content)
#             print("Generate Product Recommendation model is success !!!\n")
#             st.write(output)
#             print(output)
#             time_execute = time.time() - start
#             _, response_write = st.columns([5, 1])
#             with response_write:
#                 markdown_response = (
#                     f"Execute {tokens} tokens in {round(time_execute, 2)}s."
#                 )
#                 usage_statistic_collection = CONFIG_DATABASE[
#                     MONGODB["usage_statistic_collection"]
#                 ]
#                 update_usage_statistics(usage_statistic_collection, tokens)
#                 st.markdown(
#                     f"""
#                         <div style="border: 1px solid #ddd;
#                                     padding: 5px;
#                                     border-radius: 5px;
#                                     background-color: #DDDDDD;
#                                     margin-bottom: 15px;
#                                     text-align: center;">
#                         <i style='font-size:15px; color:#000;'>{markdown_response}</i>
#                         </div>
#                         """,
#                     unsafe_allow_html=True,
#                 )
#         except ValueError as summary_error:
#             st.error(summary_error)
#             st.error(f"Detail Error: {traceback.format_exc()}")

# MODEL CONFIGURATION AND DATABASE CONFIGURATION LAYOUT SECTION
with layout_right:
    try:
        # Display model parameters
        OPENAI_API_KEY = st.text_input(
            "OpenAI API Key", "your_api_key", type="password"
        )
        new_model_parameters = deepcopy(MODEL_CONFIG)
        for key, value in MODEL_CONFIG.items():
            if key == "max_tokens":
                new_model_parameters["max_tokens"] = st.slider(
                    "Max Tokens",
                    min_value=128,
                    max_value=2048,
                    value=MODEL_CONFIG[key],
                    # step=10,
                )
            else:
                display_key = [" ".join(word.capitalize() for word in key.split("_"))]
                st.text_input(display_key[0], value)
                new_model_parameters[key] = value

        # Save model parameters
        save_cols, params_update_response = st.columns([2, 5])
        with save_cols:
            save_parameter = st.button("Save")
            if save_parameter:
                # update_model_config(collection, model_name, new_max_tokens)
                MODEL_CONFIG = deepcopy(new_model_parameters)
                with params_update_response:
                    st.success(
                        "Save model successful !!!",
                        icon="✅",
                    )
    except Exception as e:
        st.error(f"Summary Error: {e}")
