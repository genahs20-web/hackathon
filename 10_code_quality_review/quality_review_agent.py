"""Deliverable 10: Code Quality Review Agent.

A Streamlit app that reviews uploaded source files against the quality
checklist (deliverables/06_specs + this project's coding standards) using
the Claude API, then reports a 0-100 quality score with severity-ranked
findings and actionable recommendations.

Run with: streamlit run quality_review_agent.py
"""

import io
import json
import os

import anthropic
import pandas as pd
import streamlit as st

from quality_checklist import POINTS_PER_ITEM, QUALITY_CHECKLIST

MAX_CHARS_PER_FILE = 12000
CLAUDE_MODEL = "claude-sonnet-5"


def parse_files(uploaded_files: list) -> dict[str, str]:
    """Read uploaded Streamlit file objects into {filename: content} text."""
    contents: dict[str, str] = {}
    for uploaded_file in uploaded_files:
        raw = uploaded_file.read()
        contents[uploaded_file.name] = raw.decode("utf-8", errors="ignore")[:MAX_CHARS_PER_FILE]
    return contents


def create_prompt_for_review(file_name: str, code: str) -> str:
    """Build the review prompt: checklist categories/items plus the code to review."""
    checklist_text = "\n".join(
        f"### {category}\n" + "\n".join(f"- {item}" for item in items)
        for category, items in QUALITY_CHECKLIST.items()
    )

    return f"""You are a senior code reviewer. Review the file `{file_name}` against this checklist:

{checklist_text}

For EACH checklist item, decide: pass, warning, or fail, with a one-sentence note.
Also list concrete issues found, each with: severity (CRITICAL/MAJOR/MINOR/INFO),
description, an approximate line number if identifiable, and an actionable
recommendation (not "improve error handling" — specify exactly what to add/change).

Respond with ONLY valid JSON in this exact shape:
{{
  "category_results": {{
    "<category name>": [{{"item": "<item text>", "status": "pass|warning|fail", "note": "<note>"}}]
  }},
  "issues": [
    {{"severity": "CRITICAL|MAJOR|MINOR|INFO", "description": "<desc>", "line": <int or null>, "recommendation": "<specific fix>"}}
  ]
}}

Code:
```
{code}
```"""


def call_claude_api(client: anthropic.Anthropic, prompt: str) -> dict:
    """Call the Claude API and parse the JSON review response."""
    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    raw_text = response.content[0].text
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        start, end = raw_text.find("{"), raw_text.rfind("}") + 1
        return json.loads(raw_text[start:end])


def calculate_quality_score(category_results: dict[str, list[dict]]) -> tuple[int, dict[str, int]]:
    """Normalize pass/warning/fail counts into an overall 0-100 score and per-category scores."""
    category_scores: dict[str, int] = {}
    total_points, total_possible = 0, 0

    for category, items in category_results.items():
        max_points = len(items) * POINTS_PER_ITEM["pass"]
        earned = sum(POINTS_PER_ITEM.get(item.get("status", "fail"), 0) for item in items)
        category_scores[category] = round((earned / max_points) * 100) if max_points else 0
        total_points += earned
        total_possible += max_points

    overall_score = round((total_points / total_possible) * 100) if total_possible else 0
    return overall_score, category_scores


def display_report(file_name: str, review: dict) -> None:
    """Render one file's review results in the Streamlit UI."""
    category_results = review.get("category_results", {})
    issues = review.get("issues", [])
    overall_score, category_scores = calculate_quality_score(category_results)

    st.subheader(f"{file_name} — Quality Score: {overall_score}/100")

    severity_counts = {"CRITICAL": 0, "MAJOR": 0, "MINOR": 0, "INFO": 0}
    for issue in issues:
        severity_counts[issue.get("severity", "INFO")] = severity_counts.get(issue.get("severity", "INFO"), 0) + 1

    cols = st.columns(4)
    for col, severity in zip(cols, severity_counts):
        col.metric(severity.title(), severity_counts[severity])

    for category, score in category_scores.items():
        st.progress(score / 100, text=f"{category}: {score}/100")

    if issues:
        st.markdown("**Findings** (most severe first)")
        severity_order = {"CRITICAL": 0, "MAJOR": 1, "MINOR": 2, "INFO": 3}
        for issue in sorted(issues, key=lambda i: severity_order.get(i.get("severity", "INFO"), 3)):
            with st.expander(f"[{issue.get('severity')}] {issue.get('description')}"):
                st.write(f"Line: {issue.get('line', 'N/A')}")
                st.write(f"Recommendation: {issue.get('recommendation')}")


def export_report(all_reviews: dict[str, dict]) -> bytes:
    """Flatten all findings into a CSV for download/tracking."""
    rows = []
    for file_name, review in all_reviews.items():
        overall_score, _ = calculate_quality_score(review.get("category_results", {}))
        for issue in review.get("issues", []):
            rows.append(
                {
                    "file": file_name,
                    "quality_score": overall_score,
                    "severity": issue.get("severity"),
                    "description": issue.get("description"),
                    "line": issue.get("line"),
                    "recommendation": issue.get("recommendation"),
                }
            )
    buffer = io.StringIO()
    pd.DataFrame(rows).to_csv(buffer, index=False)
    return buffer.getvalue().encode("utf-8")


def main() -> None:
    st.set_page_config(page_title="Code Quality Review Agent", layout="wide")
    st.title("Code Quality Review Agent")
    st.caption("Reviews uploaded source files against the project's 10-category quality checklist using Claude.")

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        st.warning("Set the ANTHROPIC_API_KEY environment variable before running a review.")

    uploaded_files = st.file_uploader(
        "Upload source files to review", accept_multiple_files=True, type=["py", "ts", "tsx", "js", "jsx"]
    )

    if uploaded_files and st.button("Run Quality Review", disabled=not api_key):
        client = anthropic.Anthropic(api_key=api_key)
        file_contents = parse_files(uploaded_files)
        all_reviews: dict[str, dict] = {}

        with st.spinner("Reviewing files..."):
            for file_name, code in file_contents.items():
                prompt = create_prompt_for_review(file_name, code)
                try:
                    all_reviews[file_name] = call_claude_api(client, prompt)
                except Exception as exc:  # noqa: BLE001 - surfaced to the user, not swallowed
                    st.error(f"Review failed for {file_name}: {exc}")

        st.session_state["all_reviews"] = all_reviews

    if "all_reviews" in st.session_state:
        for file_name, review in st.session_state["all_reviews"].items():
            display_report(file_name, review)

        csv_bytes = export_report(st.session_state["all_reviews"])
        st.download_button("Export Findings (CSV)", data=csv_bytes, file_name="quality_review_findings.csv")


if __name__ == "__main__":
    main()
