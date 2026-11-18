import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

st.set_page_config(
    page_title="PRD Studio | AI Product Workspace",
    page_icon="✳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# SESSION STATE
# -----------------------------
if "theme" not in st.session_state:
    st.session_state.theme = "Light"

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "product_idea" not in st.session_state:
    st.session_state.product_idea = ""

if "product_name" not in st.session_state:
    st.session_state.product_name = ""

if "target_users" not in st.session_state:
    st.session_state.target_users = ""

if "problem" not in st.session_state:
    st.session_state.problem = ""

if "solution" not in st.session_state:
    st.session_state.solution = ""

if "workspace_created" not in st.session_state:
    st.session_state.workspace_created = False

# -----------------------------
# DESIGN SYSTEM
# -----------------------------
dark = st.session_state.theme == "Dark"

if dark:
    bg = "#0B1718"
    surface = "#122526"
    text = "#E6F3F1"
    muted = "#A3BBB7"
    border = "#254342"
    primary = "#2DD4BF"
    sidebar = "#0E2021"
else:
    bg = "#F4FAF9"
    surface = "#FFFFFF"
    text = "#173B39"
    muted = "#56716D"
    border = "#D7E7E4"
    primary = "#0F766E"
    sidebar = "#FFFFFF"

st.markdown(
    f"""
    <style>
    .stApp {{
        background: {bg};
        color: {text};
    }}
    [data-testid="stSidebar"] {{
        background: {sidebar};
        border-right: 1px solid {border};
    }}
    [data-testid="stHeader"] {{
        background: transparent;
    }}
    h1, h2, h3, h4, p, label {{
        color: {text};
    }}
    .hero {{
        background: {surface};
        border: 1px solid {border};
        border-radius: 18px;
        padding: 30px;
        margin-bottom: 22px;
    }}
    .hero-label {{
        color: {primary};
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }}
    .hero-title {{
        color: {text};
        font-size: 34px;
        font-weight: 750;
        line-height: 1.2;
        margin-top: 12px;
    }}
    .hero-description {{
        color: {muted};
        font-size: 15px;
        line-height: 1.7;
        max-width: 700px;
        margin-top: 12px;
    }}
    .metric-card {{
        background: {surface};
        border: 1px solid {border};
        border-radius: 14px;
        padding: 20px;
        min-height: 115px;
    }}
    .metric-label {{
        color: {muted};
        font-size: 13px;
    }}
    .metric-value {{
        color: {text};
        font-size: 27px;
        font-weight: 700;
        margin-top: 8px;
    }}
    .section-card {{
        background: {surface};
        border: 1px solid {border};
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 12px;
    }}
    .section-title {{
        color: {text};
        font-size: 16px;
        font-weight: 650;
    }}
    .section-description {{
        color: {muted};
        font-size: 13px;
        line-height: 1.6;
        margin-top: 7px;
    }}
    .tag {{
        display: inline-block;
        color: {primary};
        background: {bg};
        border: 1px solid {border};
        border-radius: 20px;
        padding: 5px 10px;
        font-size: 11px;
        font-weight: 650;
        margin-bottom: 10px;
    }}
    div.stButton > button[kind="primary"] {{
        background: {primary};
        border: 1px solid {primary};
        color: white;
        border-radius: 9px;
        font-weight: 650;
        min-height: 42px;
    }}
    div.stButton > button {{
        border-radius: 9px;
    }}
    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea {{
        border-radius: 9px;
    }}
    .small-muted {{
        color: {muted};
        font-size: 12px;
    }}

    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"] {{
        background-color: {{bg}} !important;
    }}
    [data-testid="stSidebar"] > div:first-child {{
        background-color: {{sidebar}} !important;
    }}
    [data-testid="stVerticalBlock"] {{
        color: {{text}};
    }}
    [data-testid="stWidgetLabel"] p,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stCaptionContainer"] {{
        color: {{text}};
    }}
    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea {{
        background-color: {{surface}} !important;
        color: {{text}} !important;
        border: 1px solid {{border}} !important;
    }}
    [data-testid="stRadio"] label,
    [data-testid="stCheckbox"] label {{
        color: {{text}} !important;
    }}
    [data-testid="stAlert"] {{
        background-color: {{surface}} !important;
        color: {{text}} !important;
        border: 1px solid {{border}} !important;
    }}
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {{
        color: {{text}} !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# REUSABLE COMPONENTS
# -----------------------------
def metric_card(label, value, description):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="small-muted">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_card(number, title, description, status="Planned"):
    st.markdown(
        f"""
        <div class="section-card">
            <span class="tag">{number} · {status}</span>
            <div class="section-title">{title}</div>
            <div class="section-description">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def navigate(page):
    st.session_state.page = page


# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.markdown(
        f"""
        <div style="padding: 12px 4px 22px 4px;">
            <div style="font-size: 13px; color: {primary};
                        font-weight: 750; letter-spacing: 1.5px;">
                ✳ PRD STUDIO
            </div>
            <div style="font-size: 12px; color: {muted};
                        margin-top: 5px;">
                AI Product Workspace
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption("WORKSPACE")

    pages = ["Dashboard", "Create PRD", "PRD Workspace"]
    selected = st.radio(
        "Navigation",
        pages,
        index=pages.index(st.session_state.page),
        label_visibility="collapsed",
    )
    st.session_state.page = selected

    st.divider()
    st.caption("APPEARANCE")

    theme_choice = st.radio(
        "Theme",
        ["Light", "Dark"],
        index=0 if st.session_state.theme == "Light" else 1,
        horizontal=True,
        label_visibility="collapsed",
    )

    if theme_choice != st.session_state.theme:
        st.session_state.theme = theme_choice
        st.rerun()

    st.divider()
    st.markdown(
        f"""
        <div style="font-size: 12px; color: {muted}; line-height: 1.8;">
            <b style="color: {text};">PROJECT STATUS</b><br>
            Interface development<br>
            AI integration: Upcoming<br>
            Evaluation: Upcoming
        </div>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------
# DASHBOARD
# -----------------------------
if st.session_state.page == "Dashboard":

    st.markdown(
        """
        <div class="hero">
            <div class="hero-label">YOUR PRODUCT WORKSPACE</div>
            <div class="hero-title">Turn product ideas into<br>structured requirements.</div>
            <div class="hero-description">
                A guided workspace for junior product managers and early-stage
                founders to turn initial ideas into clear, structured product
                requirement documents — with AI assistance and human review.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        metric_card("PRD DOCUMENTS", "0", "Documents created in this workspace")

    with col2:
        metric_card("WORKFLOW", "4 stages", "From idea to structured PRD")

    with col3:
        metric_card("AI EVALUATION", "Upcoming", "Quality testing not yet implemented")

    st.write("")
    left, right = st.columns([1.35, 1])

    with left:
        st.subheader("Start building your PRD")
        st.markdown(
            f"""
            <div class="section-card">
                <div class="section-title">Have a product idea?</div>
                <div class="section-description">
                    Describe the problem, identify your users and define
                    your proposed solution. The guided workflow will help
                    organise your thinking.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("＋ Create a new PRD", type="primary", use_container_width=True):
            navigate("Create PRD")
            st.rerun()

    with right:
        st.subheader("Your workflow")

        section_card("01", "Define the idea", "Capture the product concept and context.")
        section_card("02", "Structure requirements", "Organise problems, users and solutions.")
        section_card("03", "Generate the PRD", "AI-assisted drafting will be integrated next.")
        section_card("04", "Review and refine", "Validate and improve the requirements.")

# -----------------------------
# CREATE PRD
# -----------------------------
elif st.session_state.page == "Create PRD":

    st.markdown(
        """
        <div class="hero">
            <div class="hero-label">STEP 01 · PRODUCT DISCOVERY</div>
            <div class="hero-title">Let's understand your idea.</div>
            <div class="hero-description">
                Start with the product context. Clear inputs help create
                more useful and grounded requirements.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("product_idea_form"):

        st.subheader("Product information")

        product_name = st.text_input(
            "Product name",
            value=st.session_state.product_name,
            placeholder="e.g. Smart Expense Tracker",
        )

        idea = st.text_area(
            "Describe your product idea",
            value=st.session_state.product_idea,
            placeholder="What are you trying to build? Describe the idea in your own words...",
            height=130,
        )

        target_users = st.text_input(
            "Who are your target users?",
            value=st.session_state.target_users,
            placeholder="e.g. University students, freelancers, small businesses",
        )

        problem = st.text_area(
            "What problem are you solving?",
            value=st.session_state.problem,
            placeholder="Describe the specific problem your users experience...",
            height=100,
        )

        solution = st.text_area(
            "What is your proposed solution?",
            value=st.session_state.solution,
            placeholder="How do you imagine your product solving this problem?",
            height=100,
        )

        submitted = st.form_submit_button(
            "Save product context →",
            type="primary",
            use_container_width=True,
        )

        if submitted:
            if not product_name.strip() or not idea.strip():
                st.error("Please provide at least a product name and idea.")
            else:
                st.session_state.product_name = product_name.strip()
                st.session_state.product_idea = idea.strip()
                st.session_state.target_users = target_users.strip()
                st.session_state.problem = problem.strip()
                st.session_state.solution = solution.strip()
                st.session_state.workspace_created = True
                st.session_state.page = "PRD Workspace"
                st.rerun()

# -----------------------------
# PRD WORKSPACE
# -----------------------------
elif st.session_state.page == "PRD Workspace":
    from modules.prd_workspace import render_prd_workspace

    render_prd_workspace(
        navigate=navigate,
        surface=surface,
        text=text,
        primary=primary,
    )
