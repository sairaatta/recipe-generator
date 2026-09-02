import logging

from src.recipe_generator.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

import os
import tempfile
import time

import streamlit as st

from src.recipe_generator.logging_config import setup_logging
from src.recipe_generator.graph import build_recipe_graph
from src.recipe_generator.state import RecipeState


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Recipe Generator",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #FFF9EC;
    }

    h1, h2, h3 {
        color: #3A2418;
        font-weight: 750;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #B91C1C 0%,
            #8F1515 100%
        );
        border-right: none;
    }

    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #FFFFFF;
        font-weight: 700;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span {
        color: #FFF7E6 !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.25);
    }

    [data-testid="stSidebar"] [data-testid="stAlert"] {
        background-color: rgba(255, 255, 255, 0.12);
        color: #FFFFFF;
        border-radius: 12px;
    }

    .main-title {
        color: #3A2418;
        font-size: 44px;
        font-weight: 850;
        letter-spacing: -1px;
        margin-bottom: 4px;
    }

    .main-title span {
        color: #D62828;
    }

    .subtitle {
        color: #806B55;
        font-size: 17px;
        margin-bottom: 28px;
    }

    div[role="radiogroup"] {
        background-color: #FFFFFF;
        border: 2px solid #F3D37A;
        border-radius: 14px;
        padding: 10px 14px;
        margin-bottom: 20px;
    }

    div[data-baseweb="input"] {
        border-radius: 12px;
        border: 1px solid #E8D8B8;
        background-color: #FFFFFF;
    }

    div[data-baseweb="input"]:focus-within {
        border-color: #D62828;
    }

    textarea {
        border-radius: 12px !important;
    }

    [data-testid="stFileUploader"] {
        background-color: #FFFFFF;
        border: 2px dashed #F3C74F;
        border-radius: 14px;
        padding: 10px;
    }

    .stButton > button {
        width: 100%;
        background: linear-gradient(
            135deg,
            #D62828 0%,
            #F04444 100%
        );
        color: #FFFFFF;
        border: none;
        border-radius: 12px;
        padding: 13px 20px;
        font-size: 16px;
        font-weight: 750;
        box-shadow: 0 5px 14px rgba(214, 40, 40, 0.25);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 9px 20px rgba(214, 40, 40, 0.35);
        color: #FFFFFF;
    }

    .recipe-card-title {
        background-color: #FFF0D6;
        color: #C22121;
        font-size: 12px;
        font-weight: 750;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 5px 12px;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 8px;
    }

    .recipe-title {
        color: #3A2418;
        font-size: 26px;
        font-weight: 800;
        margin-bottom: 10px;
    }

    [data-testid="stMetric"] {
        background-color: #FFF9EC;
        border: 1px solid #F0DFC0;
        border-radius: 12px;
        padding: 14px;
    }

    [data-testid="stMetricLabel"] {
        color: #806B55 !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetricValue"] {
        color: #3A2418 !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        border-bottom: 2px solid #F0DFC0;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 10px 10px 0 0;
        padding: 10px 18px;
        color: #806B55;
        font-weight: 650;
    }

    .stTabs [aria-selected="true"] {
        background-color: #FFF0D6;
        color: #D62828 !important;
        border-bottom: 3px solid #D62828;
    }

    .info-box {
        background-color: #FFF4CC;
        border-left: 5px solid #F2B705;
        padding: 14px 16px;
        border-radius: 10px;
        margin-bottom: 20px;
        color: #4A3520;
    }

    .section-divider {
        border: none;
        border-top: 2px solid #F0DFC0;
        margin: 30px 0;
    }

    .footer {
        text-align: center;
        color: #A99578;
        margin-top: 50px;
        padding: 20px;
        font-size: 13px;
        border-top: 1px solid #F0DFC0;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🍳 AI Recipe Generator")

    st.divider()

    st.markdown("### 👨‍🍳 Recipe Workflow")

    st.write(
        "**Dynamic AI Chefs**  \n"
        "One chef processes each requested dish sequentially."
    )

    st.write(
        "**Example**  \n"
        "5 dishes → 5 chef executions → 5 recipes"
    )

    st.divider()

    st.markdown("### 🧠 AI Stack")

    st.write(
        "Model: openai/gpt-oss-20b"
    )

    st.write(
        "Provider: Groq"
    )

    st.write(
        "Research: Food Recipe MCP"
    )

    st.write(
        "Workflow: LangGraph"
    )

    st.write(
        "Weather: Open-Meteo"
    )

    st.write(
        "Vision: Local Vision Model"
    )

    st.divider()

    st.info(
        "Recipes are generated using LangGraph, "
        "MCP research, weather context when needed, "
        "vision input when provided, and AI recipe generation."
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">'
    'AI <span>Recipe Generator</span>'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'Tell us what you want to cook, describe your mood, '
    'or upload a food image.'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# MODE SELECTION
# ============================================================

st.markdown("### How would you like to get recipes?")

input_type = st.radio(
    "Recipe mode",
    [
        "🍽️ Recipe Request",
        "😊 Mood Based",
    ],
    horizontal=True,
    label_visibility="collapsed",
)


# ============================================================
# DEFAULT VALUES
# ============================================================

uploaded_image = None


# ============================================================
# RECIPE REQUEST MODE
# ============================================================

if input_type == "🍽️ Recipe Request":

    st.markdown(
        '<div class="info-box">'
        '<b>Recipe Request</b><br>'
        'Tell the AI system what recipes you want. '
        'You can request one or multiple dishes. '
        'You can also upload one food image.'
        '</div>',
        unsafe_allow_html=True,
    )

    user_request = st.text_input(
        "What recipe would you like?",
        placeholder=(
            "e.g. Give me recipes for pizza, pasta, "
            "burger and tacos"
        ),
    )

    st.markdown("#### 📷 Optional food image")

    uploaded_image = st.file_uploader(
        "Upload food image",
        type=[
            "png",
            "jpg",
            "jpeg",
            "webp",
            "avif",
        ],
        accept_multiple_files=False,
        label_visibility="collapsed",
        help=(
            "Upload one food image. "
            "The vision model will identify the dish."
        ),
    )

    if uploaded_image:

        st.image(
            uploaded_image,
            caption="Reference image",
            width="stretch",
        )

        st.success(
            "Image detected. The vision model will identify the dish."
        )

    generate_button = st.button(
        "🔥 Generate Recipe",
        type="primary",
    )


# ============================================================
# MOOD MODE
# ============================================================

else:

    st.markdown(
        '<div class="info-box">'
        '<b>Mood Based Recommendations</b><br>'
        'Tell the system how you feel. If you provide a '
        'location, current weather can be used to personalize '
        'the recommendations.'
        '</div>',
        unsafe_allow_html=True,
    )

    user_request = st.text_input(
        "How are you feeling today?",
        placeholder=(
            "e.g. I am in Miami and feeling sad. "
            "Suggest me some recipes."
        ),
    )

    st.markdown(
        "Examples: "
        "`I am excited today` · "
        "`I want something comforting` · "
        "`I am in Miami and feeling sad`"
    )

    generate_button = st.button(
        "✨ Suggest Recipes",
        type="primary",
    )


# ============================================================
# GENERATE RECIPES
# ============================================================

if generate_button:

    # --------------------------------------------------------
    # VALIDATE INPUT
    # --------------------------------------------------------

    if not user_request.strip() and not uploaded_image:

        st.warning(
            "Please enter a recipe request or upload a food image."
        )

    else:

        logger.info(
            "Streamlit request received: %s",
            user_request,
        )

        image_path = None

        # ----------------------------------------------------
        # IMAGE HANDLING
        # ----------------------------------------------------

        if (
            input_type == "🍽️ Recipe Request"
            and uploaded_image
        ):

            suffix = (
                os.path.splitext(
                    uploaded_image.name
                )[1]
                or ".png"
            )

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix,
            ) as tmp_file:

                tmp_file.write(
                    uploaded_image.getbuffer()
                )

                image_path = tmp_file.name

            logger.info(
                "Saved uploaded image: %s",
                image_path,
            )

        # ----------------------------------------------------
        # PROGRESS
        # ----------------------------------------------------

        progress = st.progress(
            0,
            text="Starting recipe workflow...",
        )

        status = st.empty()

        try:

            # ------------------------------------------------
            # BUILD GRAPH
            # ------------------------------------------------

            progress.progress(
                10,
                text="Preparing LangGraph workflow...",
            )

            graph = build_recipe_graph()
            
            

            # ------------------------------------------------
            # STATUS
            # ------------------------------------------------

            if image_path:

                status.info(
                    "🔍 Identifying dish from image..."
                )

                progress.progress(
                    20,
                    text="Vision model is identifying the dish...",
                )

            elif input_type == "😊 Mood Based":

                status.info(
                    "🧠 Understanding your mood..."
                )

                progress.progress(
                    20,
                    text="Preparing personalized recommendations...",
                )

            else:

                status.info(
                    "🔎 Preparing MCP recipe research..."
                )

                progress.progress(
                    20,
                    text="Researching requested dishes...",
                )

            # ------------------------------------------------
            # INITIAL STATE
            # ------------------------------------------------

            initial_state = RecipeState(
                user_request=user_request.strip(),
                image_path=image_path,
            )

            # ------------------------------------------------
            # RUN GRAPH
            # ------------------------------------------------

            status.info(
                "🚀 Running LangGraph workflow..."
            )

            progress.progress(
                40,
                text="AI workflow is running...",
            )

            workflow_start = time.perf_counter()

            final_state = graph.invoke(
                initial_state
            )

            workflow_time = (
                time.perf_counter()
                - workflow_start
            )

            logger.info(
                "Total recipe workflow completed in %.2f seconds",
                workflow_time,
            )

            progress.progress(
                100,
                text="Recipes completed!",
            )

            status.success(
                "Recipes generated successfully!"
            )

        except Exception as exc:

            logger.exception(
                "Recipe generation failed"
            )

            progress.empty()
            status.empty()

            st.error(
                "Recipe generation failed."
            )

            st.exception(exc)

            if image_path and os.path.exists(image_path):

                os.remove(image_path)

            st.stop()

        # ====================================================
        # CONVERT RESULT IF NECESSARY
        # ====================================================

        # LangGraph normally returns a dictionary.
        # Support both dict and RecipeState for safety.

        if isinstance(final_state, RecipeState):

            result = final_state.model_dump()

        else:

            result = final_state

        # ====================================================
        # WORKFLOW SUMMARY
        # ====================================================

        st.markdown(
            '<hr class="section-divider">',
            unsafe_allow_html=True,
        )

        st.header("📊 Workflow Summary")

        dishes = result.get(
            "dishes",
            [],
        )

        recipes = result.get(
            "recipes",
            [],
        )

        research = result.get(
            "research",
            [],
        )

        input_mode = result.get(
            "input_mode",
            "unknown",
        )

        summary_col1, summary_col2, summary_col3, summary_col4 = (
            st.columns(4)
        )

        with summary_col1:

            st.metric(
                "🍽️ Dishes",
                len(dishes),
            )

        with summary_col2:

            st.metric(
                "👨‍🍳 Recipes",
                len(recipes),
            )

        with summary_col3:

            st.metric(
                "🔎 MCP Results",
                len(research),
            )

        with summary_col4:

            st.metric(
                "📌 Input Mode",
                input_mode.title(),
            )

        # ====================================================
        # REQUESTED / DETECTED DISHES
        # ====================================================

        if dishes:

            st.markdown("### 🍽️ Dishes")

            for index, dish in enumerate(
                dishes,
                start=1,
            ):

                st.write(
                    f"**{index}.** {dish}"
                )

        # ====================================================
        # IMAGE RESULT
        # ====================================================

        image_dish = result.get(
            "image_dish"
        )

        if image_dish:

            st.markdown(
                '<hr class="section-divider">',
                unsafe_allow_html=True,
            )

            st.markdown(
                "### 🔍 Identified Dish"
            )

            if image_dish.lower() == "unknown":

                st.warning(
                    "The vision model could not identify the dish."
                )

            else:

                st.success(
                    f"🍽️ {image_dish}"
                )

        # ====================================================
        # WEATHER RESULT
        # ====================================================

        weather_context = result.get(
            "weather_context"
        )

        if weather_context:

            st.markdown(
                '<hr class="section-divider">',
                unsafe_allow_html=True,
            )

            st.header("🌤️ Weather Context")

            weather_col1, weather_col2, weather_col3 = (
                st.columns(3)
            )

            with weather_col1:

                st.metric(
                    "📍 Location",
                    weather_context.get(
                        "location",
                        "Unknown",
                    ),
                )

            with weather_col2:

                st.metric(
                    "🌡️ Temperature",
                    f"{weather_context.get('temperature', 'N/A')} °C",
                )

            with weather_col3:

                st.metric(
                    "💧 Humidity",
                    f"{weather_context.get('humidity', 'N/A')} %",
                )

            precipitation = weather_context.get(
                "precipitation"
            )

            weather_code = weather_context.get(
                "weather_code"
            )

            st.write(
                f"**Precipitation:** {precipitation} mm"
            )

            st.write(
                f"**Weather Code:** {weather_code}"
            )

        # ====================================================
        # RECIPES
        # ====================================================

        st.markdown(
            '<hr class="section-divider">',
            unsafe_allow_html=True,
        )

        if input_type == "😊 Mood Based":

            st.header(
                "✨ Recipes For Your Mood"
            )

        elif image_path:

            st.header(
                "📷 Recipes From Your Image"
            )

        else:

            st.header(
                "👨‍🍳 Your AI Chef Recipes"
            )

        # ====================================================
        # DYNAMIC RECIPES
        # ====================================================

        if recipes:

            # Convert Pydantic recipes to objects when
            # necessary.

            normalized_recipes = []

            for recipe in recipes:

                if isinstance(recipe, dict):

                    normalized_recipes.append(
                        recipe
                    )

                else:

                    normalized_recipes.append(
                        recipe.model_dump()
                    )

            # ------------------------------------------------
            # CREATE DYNAMIC TABS
            # ------------------------------------------------

            tab_names = []

            for index, recipe in enumerate(
                normalized_recipes,
                start=1,
            ):

                dish_name = (
                    dishes[index - 1]
                    if index - 1 < len(dishes)
                    else f"Dish {index}"
                )

                tab_names.append(
                    f"Chef {index} · {dish_name}"
                )

            tabs = st.tabs(
                tab_names
            )

            # ------------------------------------------------
            # DISPLAY EACH RECIPE
            # ------------------------------------------------

            for index, (
                tab,
                recipe,
            ) in enumerate(
                zip(
                    tabs,
                    normalized_recipes,
                ),
                start=1,
            ):

                with tab:

                    dish_name = (
                        dishes[index - 1]
                        if index - 1 < len(dishes)
                        else f"Dish {index}"
                    )

                    st.markdown(
                        f'<div class="recipe-card-title">'
                        f'Chef {index} · {dish_name}'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

                    st.markdown(
                        f'<div class="recipe-title">'
                        f'{recipe.get("name", "Unnamed Recipe")}'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

                    st.write(
                        recipe.get(
                            "description",
                            "",
                        )
                    )

                    # ----------------------------------------
                    # RECIPE INFORMATION
                    # ----------------------------------------

                    col1, col2 = st.columns(2)

                    with col1:

                        st.metric(
                            "🍽️ Servings",
                            recipe.get(
                                "servings",
                                "N/A",
                            ),
                        )

                    with col2:

                        st.metric(
                            "⏱️ Cook Time",
                            f"{recipe.get('cooking_time_minutes', 'N/A')} min",
                        )

                    # ----------------------------------------
                    # INGREDIENTS
                    # ----------------------------------------

                    st.markdown(
                        "### 🥕 Ingredients"
                    )

                    ingredients = recipe.get(
                        "ingredients",
                        [],
                    )

                    for ingredient_index, ingredient in enumerate(
                        ingredients
                    ):

                        if isinstance(
                            ingredient,
                            dict,
                        ):

                            ingredient_name = ingredient.get(
                                "name",
                                "Ingredient",
                            )

                            quantity = ingredient.get(
                                "quantity",
                                "",
                            )

                        else:

                            ingredient_name = getattr(
                                ingredient,
                                "name",
                                "Ingredient",
                            )

                            quantity = getattr(
                                ingredient,
                                "quantity",
                                "",
                            )

                        st.checkbox(
                            f"{quantity} {ingredient_name}",
                            key=(
                                f"recipe_{index}_"
                                f"ingredient_{ingredient_index}"
                            ),
                        )

                    # ----------------------------------------
                    # INSTRUCTIONS
                    # ----------------------------------------

                    st.markdown(
                        "### 👩‍🍳 Instructions"
                    )

                    instructions = recipe.get(
                        "instructions",
                        [],
                    )

                    for instruction_index, instruction in enumerate(
                        instructions,
                        start=1,
                    ):

                        with st.expander(
                            f"Step {instruction_index}"
                        ):

                            st.write(
                                instruction
                            )

        else:

            st.warning(
                "No recipes were generated."
            )
        # ====================================================
        # RECIPE SUMMARY
        # ====================================================
        
        recipe_summary = result.get(
            "recipe_summary"
        )
        
        if recipe_summary:
        
            st.markdown(
                '<hr class="section-divider">',
                unsafe_allow_html=True,
            )
        
            st.header("🧑‍🍳 Summary Chef")
        
            st.info(
                "This section provides a neutral summary of all "
                "chef recipes. It does not recommend or rank any recipe."
            )
        
            st.markdown(recipe_summary)
        # ====================================================
        # TOKEN USAGE & COST
        # ====================================================

        st.markdown(
            '<hr class="section-divider">',
            unsafe_allow_html=True,
        )

        st.header(
            "💰 Input, Output Tokens per Chef"
        )

        cost_estimates = result.get(
            "cost_estimates",
            {},
        )

        if cost_estimates:

            # ------------------------------------------------
            # PER CHEF COST
            # ------------------------------------------------

            for chef_name, data in cost_estimates.items():

                if chef_name == "total":
                    continue

                st.markdown(
                    f"### 👨‍🍳 {chef_name}"
                )

                cost_col1, cost_col2, cost_col3 = (
                    st.columns(3)
                )

                with cost_col1:

                    st.metric(
                        "Input Tokens",
                        data.get(
                            "input_tokens",
                            0,
                        ),
                    )

                with cost_col2:

                    st.metric(
                        "Output Tokens",
                        data.get(
                            "output_tokens",
                            0,
                        ),
                    )


            # ------------------------------------------------
            # TOTAL COST
            # ------------------------------------------------

            total_data = cost_estimates.get(
                "total",
                {},
            )
            
            st.markdown(
                "### 📊 Total Workflow Usage"
            )
            
            total_col1, total_col2, total_col3 = (
                st.columns(3)
            )
            
            with total_col1:
            
                st.metric(
                    "Input Tokens",
                    total_data.get(
                        "input_tokens",
                        0,
                    ),
                )
            
            with total_col2:
            
                st.metric(
                    "Output Tokens",
                    total_data.get(
                        "output_tokens",
                        0,
                    ),
                )
            
            with total_col3:
            
                st.metric(
                    "Total Tokens",
                    total_data.get(
                        "total_tokens",
                        0,
                    ),
                )
            
            # with total_col4:
            
            #     st.metric(
            #         "Estimated Cost",
            #         f"${total_data.get('estimated_cost', 0.0):.6f}",
            #     )
        else:
            
                        st.info(
                            "Token usage information is not available."
                        )
                    

        # ====================================================
        # GENERATION TIME
        # ====================================================

        st.markdown(
            '<hr class="section-divider">',
            unsafe_allow_html=True,
        )

        st.header(
            "⏱️ Generation Time"
        )

        time_col1, time_col2 = st.columns(2)

        with time_col1:

            st.metric(
                "Total Workflow Time",
                f"{workflow_time:.2f} sec",
            )

        with time_col2:

            st.metric(
                "Total Workflow Time",
                f"{workflow_time / 60:.2f} min",
            )

        # ====================================================
        # FINAL STATUS
        # ====================================================

        final_status = result.get(
            "status"
        )

        if final_status:

            st.markdown(
                f"**Workflow Status:** `{final_status}`"
            )

        # ====================================================
        # CLEAN TEMP IMAGE
        # ====================================================

        if image_path:

            if os.path.exists(image_path):

                os.remove(
                    image_path
                )

                logger.info(
                    "Removed temp image: %s",
                    image_path,
                )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        AI Recipe Generator |
        Powered by LangGraph, MCP, Open-Meteo and AI recipe generation
    </div>
    """,
    unsafe_allow_html=True,
)

