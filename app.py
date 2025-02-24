import time
import logging
import streamlit as st

from copy import deepcopy
from pymongo import MongoClient
from generate import openai_response

#############################################

if "MODEL_CONFIG" not in st.session_state:
    st.session_state.MODEL_CONFIG = {
        "model_name": "gpt-4o-mini",
        "max_tokens": 256,
        "n": 1,
        "top_p": 1.0,
        "temperature": 0.0,
        "presence_penalty": 0.0,
        "frequency_penalty": 0.0,
    }

if "OPENAI_API_KEY" not in st.session_state:
    st.session_state.OPENAI_API_KEY = "your_api_key"

if "COLLECTION" not in st.session_state:
    st.session_state.COLLECTION = None

if "IS_CONNECTED_DB" not in st.session_state:
    st.session_state.IS_CONNECTED_DB = False

############### APP STREAMLIT ###############


st.set_page_config(
    page_title="Generate Playground",
    page_icon="🌟",
    layout="wide",
)  # Turn on wide layout mode for Playground screen

st.title("Playground For Model Generative AI")  # Title Playground

mongo_db_uri = st.text_input("MongoDB URI", "mongo_db_uri")
database_name = st.text_input("Database name", "database_name")
collection_name = st.text_input("Collection name", "collection_name")


if st.button("Connect to DB"):
    try:
        client = MongoClient(mongo_db_uri, serverSelectionTimeoutMS=5000)
        client.server_info()

        db = client[database_name]
        st.session_state.COLLECTION = db[collection_name]

        st.success("✅ Connect to DB successful !!!")
        st.session_state.IS_CONNECTED_DB = True
    except Exception as e:
        st.error(f"❌ ERROR: {e}")
else:
    if not st.session_state.IS_CONNECTED_DB:
        st.warning("⚠️ Please connect to DB")

layout_left, layout_right = st.columns([5, 2])  # Split screen into 2 frame/layout
# USER PLAYGROUND LAYOUT SECTION
if st.session_state.IS_CONNECTED_DB:
    system_content = ""
    user_content = ""

    with layout_left:
        # SECTION 1: System assignment
        st.subheader("Generate recommendation")

        with st.chat_message("ai"):
            system_query = st.session_state.COLLECTION.find_one(
                {"generate_field": "system_prompt"}
            )

            assume_role = st.text_area(
                "System Assigned Role", system_query["assigned_role"], height=150
            )
            prompt_requirements = st.text_area(
                "Prompt requirements", system_query["prompt_requirements"], height=600
            )

            output_requirements = st.text_area(
                "Output requirements", system_query["output_requirements"], height=250
            )

            system_content = (
                f"{assume_role}\n{prompt_requirements}\n{output_requirements}"
            )
            update_field, response_field = st.columns([2, 4])
            with update_field:
                if st.session_state.IS_CONNECTED_DB:
                    if st.button("Update system"):
                        update_action = {
                            "$set": {
                                "assigned_role": assume_role,
                                "prompt_requirements": prompt_requirements,
                                "output_requirements": output_requirements,
                            }
                        }

                        result = st.session_state.COLLECTION.update_one(
                            {"generate_field": "system_prompt"},
                            update_action,
                            upsert=True,
                        )

                        with response_field:
                            if result.upserted_id:
                                st.success(
                                    f"✅ New Document was created with _id: {result.upserted_id} !!!"
                                )
                            else:
                                st.success("Document was updated system prompt !!!")
                else:
                    st.warning("⚠️ Please connect to DB")

        # SECTION 2: User request
        with st.chat_message("human"):
            user_query = st.session_state.COLLECTION.find_one(
                {"generate_field": "user_prompt"}
            )

            user_request = st.text_area(
                "User request to OpenAI", user_query["user_request"], height=750
            )

            update_field, response_field = st.columns([2, 4])
            with update_field:
                if st.session_state.IS_CONNECTED_DB:
                    if st.button("Update request"):
                        update_action = {
                            "$set": {
                                "user_request": user_request,
                            }
                        }

                        result = st.session_state.COLLECTION.update_one(
                            {"generate_field": "user_prompt"},
                            update_action,
                            upsert=True,
                        )

                        with response_field:
                            if result.upserted_id:
                                st.success(
                                    f"✅ New Document was created with _id: {result.upserted_id} !!!"
                                )
                            else:
                                st.success("Document was updated user prompt !!!")
                else:
                    st.warning("⚠️ Please connect to DB")

        # SECTION 3: Model response
        if st.button("Generate ..."):
            try:
                start = time.time()
                logging.info("Starting...")
                output, tokens = openai_response(
                    user_content=user_request,
                    system_content=system_content,
                    api_key=st.session_state.OPENAI_API_KEY,
                    model_name=st.session_state.MODEL_CONFIG["model_name"],
                    max_tokens=st.session_state.MODEL_CONFIG["max_tokens"],
                    n=st.session_state.MODEL_CONFIG["n"],
                    top_p=st.session_state.MODEL_CONFIG["top_p"],
                    temperature=st.session_state.MODEL_CONFIG["temperature"],
                    frequency_penalty=st.session_state.MODEL_CONFIG[
                        "frequency_penalty"
                    ],
                    presence_penalty=st.session_state.MODEL_CONFIG["presence_penalty"],
                )
                logging.info("Generate Product Recommendation model is success !!!\n")
                logging.debug(f"Prompt (Input) tokens: {tokens.prompt_tokens}")
                logging.debug(f"Completion (Output) tokens: {tokens.completion_tokens}")
                st.write(output)
                time_execute = time.time() - start
                _, response_write = st.columns([6, 2])
                with response_write:
                    markdown_response = f"Execute total {tokens.total_tokens} tokens in {round(time_execute, 2)}s."
                    st.write(markdown_response)
            except ValueError as summary_error:
                st.error(summary_error)

    # MODEL CONFIGURATION AND DATABASE CONFIGURATION LAYOUT SECTION
    with layout_right:
        try:
            # Display model parameters
            st.session_state.OPENAI_API_KEY = st.text_input(
                "OpenAI API Key", "your_api_key", type="password"
            )

            new_model_parameters = deepcopy(st.session_state.MODEL_CONFIG)
            for key, value in st.session_state.MODEL_CONFIG.items():
                if key == "max_tokens":
                    new_model_parameters["max_tokens"] = st.slider(
                        "Max Tokens",
                        min_value=128,
                        max_value=2048,
                        value=st.session_state.MODEL_CONFIG[key],
                        # step=10,
                    )
                else:
                    display_key = [
                        " ".join(word.capitalize() for word in key.split("_"))
                    ]
                    new_model_parameters[key] = st.text_input(display_key[0], value)

            # Save model parameters
            save_cols, params_update_response = st.columns([2, 5])
            with save_cols:
                save_parameter = st.button("Save")
                if save_parameter:
                    # update_model_config(collection, model_name, new_max_tokens)
                    st.session_state.MODEL_CONFIG = deepcopy(new_model_parameters)
                    logging.debug(st.session_state.MODEL_CONFIG)
                    with params_update_response:
                        st.success(
                            "Save model successful !!!",
                            icon="✅",
                        )
        except Exception as e:
            st.error(f"Summary Error: {e}")
