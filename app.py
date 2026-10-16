
import os
import html

import streamlit as st
from dotenv import load_dotenv

# Load .env before importing application modules.
load_dotenv(override=True)

from services.prune_client import PruneAPIError
from graph.workflow import build_workflow


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Research Intelligence",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# STYLING
# --------------------------------------------------

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }

    .hero-title {
        font-size: 2rem;
        font-weight: 750;
        letter-spacing: -0.7px;
        margin-bottom: 0.25rem;
    }

    .hero-subtitle {
        color: var(--text-color);
        opacity: 0.72;
        font-size: 0.98rem;
        margin-bottom: 1.5rem;
    }

    .metric-card {
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 12px;
        padding: 16px 18px;
        background: var(--secondary-background-color);
        min-height: 100px;
    }

    .metric-label {
        font-size: 0.78rem;
        opacity: 0.7;
        margin-bottom: 8px;
    }

    .metric-value {
        color: var(--text-color);
        font-size: 1.25rem;
        font-weight: 750;
        overflow-wrap: anywhere;
    }

    div[data-testid="stForm"] {
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 12px;
        padding: 1rem;
        background: transparent;
        box-shadow: none;
    }

    .section-caption {
        font-size: 0.85rem;
        opacity: 0.7;
    }

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def metric_card(label: str, value: str) -> None:
    """Render a small dashboard metric."""
    safe_label = html.escape(str(label))
    safe_value = html.escape(str(value))

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{safe_label}</div>
            <div class="metric-value">{safe_value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def display_items(title: str, items) -> None:
    """Display a list of research items safely."""
    st.markdown(f"#### {title}")

    if not items:
        st.info("No items available.")
        return

    if isinstance(items, str):
        st.markdown(items)
        return

    for item in items:
        st.markdown(f"- {item}")


def display_critique(critique) -> None:
    """Display the critic output whether it is a dict or text."""
    if isinstance(critique, dict):
        decision = str(critique.get("decision", "Not available"))
        issues = critique.get("issues", [])
        feedback = critique.get("feedback", "")

        if decision.upper() == "PASS":
            st.success(f"Review decision: {decision}")
        elif decision.upper() == "REVISE":
            st.warning(f"Review decision: {decision}")
        else:
            st.info(f"Review decision: {decision}")

        if issues:
            display_items("Issues identified", issues)
        else:
            st.write("No explicit issues reported.")

        if feedback:
            st.markdown("**Feedback**")
            st.write(feedback)
    elif critique:
        st.write(critique)
    else:
        st.info("No critic feedback is available.")


def display_prune_error(exc: PruneAPIError) -> None:
    """Display structured Prune errors without losing technical details."""
    st.error("A request was rejected by Prune.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**HTTP status**")
        st.code(str(exc.status_code))

    with col2:
        st.markdown("**Error code**")
        st.code(str(exc.code))

    st.markdown("**Reason**")
    st.write(exc.message)

    if exc.docs_url:
        st.markdown(f"[View Prune documentation]({exc.docs_url})")

    st.warning(
        "The research workflow stopped because a gateway request failed. "
        "Earlier stages, such as planning, may already have completed. "
        "This error alone does not establish whether an earlier request "
        "reached an upstream model provider."
    )

    with st.expander("Technical error details"):
        st.code(
            f"HTTP status: {exc.status_code}\n"
            f"Error code: {exc.code}\n"
            f"Reason: {exc.message}\n"
            f"Documentation: {exc.docs_url or 'Not provided'}\n"
            f"Raw response: {exc.raw_body or 'Not available'}",
            language="text",
        )


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

test_mode = os.getenv("LLM_TEST_MODE", "false").lower() == "true"
model_name = os.getenv("PRUNE_MODEL", "Not configured")
base_url = os.getenv("PRUNE_BASE_URL", "https://api.withprune.com/v1")

with st.sidebar:
    st.markdown("## Research Intelligence")
    st.caption("AUTONOMOUS RESEARCH WORKSPACE")

    st.divider()

    st.markdown("### Agent workflow")
    st.markdown(
        """
        1. **Planner** — breaks down the question
        2. **Researcher** — retrieves relevant evidence
        3. **Analyst** — evaluates the findings
        4. **Critic** — reviews the analysis
        5. **Revision** — addresses feedback if needed
        6. **Synthesizer** — prepares the final report
        """
    )

    st.divider()

    st.markdown("### Knowledge retrieval")
    st.caption("Local embeddings · ChromaDB · RAG")

    st.divider()

    st.markdown("### LLM gateway")
    st.caption("Application → LLMService → Prune → Provider")

    st.divider()

    if test_mode:
        st.info("Mock mode active — no external LLM requests from LLMService.")
    else:
        st.warning("Live mode configured — gateway requests may incur usage.")

    st.caption(f"Model: `{model_name}`")
    st.caption(f"Gateway: `{base_url}`")


# --------------------------------------------------
# MAIN HEADER
# --------------------------------------------------

st.markdown(
    '<div class="hero-title">Autonomous Research Agent</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="hero-subtitle">'
    "Turn a research question into a structured report using "
    "multi-agent orchestration, local retrieval, and an AI gateway."
    "</div>",
    unsafe_allow_html=True,
)


# --------------------------------------------------
# METRICS
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    metric_card("Execution mode", "Mock" if test_mode else "Live")

with col2:
    metric_card("Configured model", model_name)

with col3:
    metric_card("Knowledge base", "Local RAG · ChromaDB")


# --------------------------------------------------
# RESEARCH INPUT
# --------------------------------------------------

st.markdown("### Start a research task")

with st.form("research_form"):
    user_query = st.text_area(
        "What would you like to research?",
        placeholder=(
            "Example: What are the main benefits and limitations of RAG?"
        ),
        height=120,
    )

    submitted = st.form_submit_button(
        "Start research",
        type="primary",
        use_container_width=True,
    )


# --------------------------------------------------
# RUN WORKFLOW
# --------------------------------------------------

if submitted:
    st.session_state.pop("research_result", None)
    st.session_state.pop("research_error", None)
    if not user_query.strip():
        st.warning("Enter a research question before starting.")
    else:
        initial_state = {"user_query": user_query.strip()}

        try:
            with st.spinner("Researching, analyzing, and reviewing findings..."):
                workflow = build_workflow()
                result = workflow.invoke(initial_state)

            st.session_state["research_result"] = result
            st.session_state["research_query"] = user_query.strip()
            st.session_state.pop("research_error", None)

        except PruneAPIError as exc:
            st.session_state.pop("research_result", None)
            st.session_state["research_error"] = {
                "type": "prune",
                "status_code": exc.status_code,
                "code": exc.code,
                "message": exc.message,
                "docs_url": exc.docs_url,
                "raw_body": exc.raw_body,
            }

            print("\n===== PRUNE ERROR IN STREAMLIT =====")
            print("Status:", exc.status_code)
            print("Code:", exc.code)
            print("Reason:", exc.message)
            print("====================================\n")

        except Exception as exc:
            st.session_state.pop("research_result", None)
            st.session_state["research_error"] = {
                "type": "general",
                "message": str(exc),
            }

            print("\n===== WORKFLOW ERROR =====")
            print(repr(exc))
            print("==========================\n")


# --------------------------------------------------
# DISPLAY ERRORS
# --------------------------------------------------

error = st.session_state.get("research_error")

if error:
    if error["type"] == "prune":
        st.error("The research workflow stopped because Prune rejected a request.")

        error_col1, error_col2 = st.columns(2)

        with error_col1:
            st.markdown("**HTTP status**")
            st.code(str(error["status_code"]))

        with error_col2:
            st.markdown("**Error code**")
            st.code(str(error["code"]))

        st.markdown("**Reason**")
        st.write(error["message"])

        if error.get("docs_url"):
            st.markdown(
                f"[View Prune documentation]({error['docs_url']})"
            )

        st.warning(
            "The planner may have completed before a later request was "
            "blocked. A gateway rejection does not, by itself, prove "
            "whether a previous workflow stage reached a provider."
        )

        with st.expander("Technical error details"):
            st.code(
                f"HTTP status: {error['status_code']}\n"
                f"Error code: {error['code']}\n"
                f"Reason: {error['message']}\n"
                f"Documentation: {error.get('docs_url') or 'Not provided'}\n"
                f"Raw response: {error.get('raw_body') or 'Not available'}",
                language="text",
            )
    else:
        st.error("The research workflow failed.")

        with st.expander("Technical error details"):
            st.code(error.get("message", "Unknown error"), language="text")


# --------------------------------------------------
# RESULTS
# --------------------------------------------------

result = st.session_state.get("research_result")

if result:
    st.divider()
    st.markdown("## Research results")

    st.caption(
        "Results for: "
        + st.session_state.get("research_query", "Previous research task")
    )

    if test_mode:
        st.info(
            "Mock mode is active. LLM responses are simulated; "
            "local document retrieval may still run."
        )

    final_tab, evidence_tab, critic_tab, workflow_tab = st.tabs(
        [
            "Final Report",
            "Research Evidence",
            "Critic Review",
            "Workflow Details",
        ]
    )

    with final_tab:
        final_answer = result.get("final_answer", "")

        if final_answer:
            st.markdown(final_answer)
        else:
            st.info("No final report was returned.")

    with evidence_tab:
        research_results = result.get("research_results", [])

        if research_results:
            for index, research_item in enumerate(research_results, start=1):
                with st.expander(f"Research task {index}", expanded=True):
                    st.markdown(
                        research_item
                        if isinstance(research_item, str)
                        else str(research_item)
                    )
        else:
            st.info("No research results were returned.")

    with critic_tab:
        display_critique(result.get("critique"))

        st.markdown("**Revision count**")
        st.write(result.get("revision_count", 0))

    with workflow_tab:
        display_items("Research tasks", result.get("research_tasks", []))

        st.markdown("#### Analysis")
        analysis = result.get("analysis", "")

        if analysis:
            st.markdown(analysis)
        else:
            st.info("No analysis is available.")

        with st.expander("Complete workflow state"):
            st.json(result)