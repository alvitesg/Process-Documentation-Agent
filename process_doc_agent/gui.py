import io
import sys
import zipfile
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from process_doc_agent.pipeline import generate_artifacts_from_text


st.set_page_config(page_title="Process Documentation Agent", page_icon="🧭", layout="wide")
st.title("🧭 Process Documentation Agent")
st.caption("Upload .txt process documents and generate an audit narrative, process flowchart, and RCSA.")

uploaded_files = st.file_uploader(
    "Upload one or more .txt files",
    type=["txt"],
    accept_multiple_files=True,
)

if st.button("Generate assessment outputs", type="primary"):
    if not uploaded_files:
        st.error("Please upload at least one .txt file to continue.")
    else:
        texts = []
        for upload in uploaded_files:
            decoded = upload.read().decode("utf-8", errors="ignore").strip()
            if decoded:
                texts.append(f"# Source: {upload.name}\n{decoded}")

        if not texts:
            st.error("Uploaded files were empty after decoding.")
        else:
            source_text = "\n\n".join(texts)
            artifacts = generate_artifacts_from_text(source_text)

            st.success("Outputs generated successfully.")

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Audit Narrative")
                st.markdown(artifacts["audit_narrative.md"])
                st.download_button(
                    "Download audit_narrative.md",
                    data=artifacts["audit_narrative.md"],
                    file_name="audit_narrative.md",
                    mime="text/markdown",
                )

            with col2:
                st.subheader("RCSA")
                st.markdown(artifacts["rcsa.md"])
                st.download_button(
                    "Download rcsa.md",
                    data=artifacts["rcsa.md"],
                    file_name="rcsa.md",
                    mime="text/markdown",
                )

            st.subheader("Process Flowchart (Mermaid)")
            st.code(artifacts["process_flowchart.mmd"], language="mermaid")
            st.download_button(
                "Download process_flowchart.mmd",
                data=artifacts["process_flowchart.mmd"],
                file_name="process_flowchart.mmd",
                mime="text/plain",
            )

            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as archive:
                for filename, content in artifacts.items():
                    archive.writestr(filename, content)

            st.download_button(
                "Download all outputs (.zip)",
                data=zip_buffer.getvalue(),
                file_name="process_assessment_outputs.zip",
                mime="application/zip",
            )
