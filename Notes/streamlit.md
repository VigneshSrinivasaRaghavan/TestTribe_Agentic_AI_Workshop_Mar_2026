- Streamlit + Core Concepts
    
    ### What is Streamlit?
    
    - A Python library that turns a `.py` file into a web app
    - No HTML, no JavaScript, no frontend knowledge needed
    - Every time a user interacts with a widget (button, dropdown, text input), Streamlit **reruns the entire script** from top to bottom
    - Used heavily in AI/ML teams for internal tooling, demos, and dashboards
    - Install: `pip install streamlit` → Run: `streamlit run app.py`
    
    ---
    
    ### Why Streamlit and Not Something Else?
    
    **vs Flask/FastAPI + React** — Needs a separate frontend app, REST endpoints, JSON serialization, CORS setup. Overkill for internal AI tooling.
    
    **vs Gradio** — Designed for single model demos (one input → one output). Doesn't handle multi-pipeline apps with different input types cleanly.
    
    **vs Jupyter Notebook** — Great for exploration, bad for sharing. Users need Python installed, no proper UI widgets, doesn't look like an app.
    
    **Streamlit wins here because:**
    
    - Entire app is one Python file
    - Runs in any browser — no Python knowledge needed to use it
    - Native support for `st.dataframe`, `st.file_uploader`, `st.tabs` — exactly what we need
    - Industry standard for internal AI tooling prototypes (used at OpenAI, Hugging Face, etc.)
    
    ---
    
    ### Folder Structure We Are Building
    
    ```
    project_root/
    ├── app.py                         ← Streamlit entrypoint       (Section 3)
    ├── src/
    │   ├── ui/
    │   │   ├── __init__.py            ← empty package marker       (Section 3)
    │   │   ├── components.py          ← reusable output renderer   (Section 3)
    │   │   └── pipeline_registry.py  ← pipeline wiring            (Section 3–7)
    │   └── graph/                     ← existing pipelines, untouched
    └── requirement.txt                ← add streamlit               (Section 3)
    ```
    
    `src/ui/` is the dedicated home for all UI logic. `app.py` at the root is the single entry point — this is the Streamlit convention.
    
    ---
    
    ### The Pipeline Selector Concept
    
    The app has one sidebar dropdown. The user picks a pipeline → the main panel shows the right input form and output area for that pipeline.
    
    ```
    Sidebar                      Main Panel
    ────────────────             ────────────────────────────────
    Select Pipeline:             [ Input form for selected pipeline ]
    ▼ Incident Response
      Jira → TestRail → Slack   [ Run button ]
    
                                 [ Output: tabs + download ]
    ```
    
    Only 2 pipelines will be wired up. Video 2 explains why the other 4 pipelines in the repo cannot be used directly in a web UI.
    
    ---
    
    ### The Rerun Model — Most Important Concept
    
    Every time a user clicks a button, types in a box, or picks a dropdown — **Streamlit reruns the entire `app.py` script from line 1**.
    
    This means:
    
    - Local variables are wiped on every rerun
    - If you store pipeline results in a regular variable, they disappear the moment the user touches anything
    - Solution: `st.session_state` — a dict that **survives reruns**
    
    ```python
    # Wrong — result disappears on next rerun
    result = run_pipeline(input)
    
    # Correct — result persists across reruns
    st.session_state["result"] = run_pipeline(input)
    ```
    
    ---
    
    ### Widgets We Use and Why
    
    **`st.selectbox` — Pipeline Picker**
    
    ```python
    selected = st.selectbox("Select Pipeline", PIPELINES)
    ```
    
    Returns the currently selected string. Triggers a rerun when changed.
    
    ---
    
    **`st.text_area` — Log Content Input**
    
    ```python
    log_content = st.text_area("Paste Log Content", height=200)
    ```
    
    Multi-line text input. Used for pasting raw log content into the Incident Response pipeline.
    
    ---
    
    **`st.file_uploader` — Log File Upload**
    
    ```python
    uploaded = st.file_uploader("Upload Log File", type=["txt", "log"])
    if uploaded:
        log_content = uploaded.read().decode("utf-8")
    ```
    
    Returns a file-like object. We decode it to a string and pass directly into pipeline state.
    
    ---
    
    **`st.text_input` — Jira Key Input**
    
    ```python
    jira_key = st.text_input("Jira Issue Key", placeholder="QA-1")
    ```
    
    Single-line input. Used for the Jira → TestRail → Slack pipeline.
    
    ---
    
    **`st.button` — Run Trigger**
    
    ```python
    if st.button("Run Pipeline"):
        st.session_state["result"] = run_pipeline(input)
    ```
    
    Returns `True` only on the rerun caused by clicking it.
    
    ---
    
    **`st.spinner` — LLM Wait Indicator**
    
    ```python
    with st.spinner("Running pipeline..."):
        result = run_pipeline(input)
    ```
    
    Shows a loading spinner while the `with` block is executing. Wraps the `graph.invoke()` call.
    
    ---
    
    **`st.tabs` — Multiple Output Views**
    
    ```python
    tab1, tab2 = st.tabs(["Report", "Raw Data"])
    with tab1:
        st.markdown(report_text)
    with tab2:
        st.json(result)
    ```
    
    Used in the output panel to show the formatted report and the full raw result side by side.
    
    ---
    
    **`st.dataframe` — Structured Data Table**
    
    ```python
    import pandas as pd
    st.dataframe(pd.DataFrame(test_cases), use_container_width=True)
    ```
    
    Renders a list of dicts as an interactive sortable table.
    
    ---
    
    **`st.download_button` — Export Results**
    
    ```python
    st.download_button("Download Report", data=report_text, file_name="report.txt")
    ```
    
    Lets users save the output locally. No server needed — Streamlit handles it in the browser.
    
    ---
    
    **`st.success` / `st.error` / `st.warning` — Status Banners**
    
    ```python
    st.success("Pipeline completed!")
    st.error(f"Error: {message}")
    ```
    
    Coloured banners for pipeline status feedback.
    
    ---
    
    ### Output Panel Pattern
    
    Every pipeline in this app follows the same output structure. This is why we extract it into `components.py` in Video 3 — so each pipeline calls one function instead of repeating the same tab/download logic.
    
    ```
    st.success("Pipeline completed!")
    
    st.tabs(["Report", "Raw Data"])
      Tab 1 → st.markdown(report_text)
      Tab 2 → st.json(full_result_dict)
    
    st.download_button("Download Report", ...)
    ```