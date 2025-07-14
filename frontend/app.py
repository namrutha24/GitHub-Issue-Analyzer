import streamlit as st
import requests

st.title("GitHub Issue Analyzer")

repo_url = st.text_input("GitHub Repository URL", "https://github.com/facebook/react")
issue_number = st.number_input("Issue Number", min_value=1, step=1)

if st.button("Analyze Issue"):
    if repo_url and issue_number:
        with st.spinner("Analyzing..."):
            try:
                response = requests.post(
                    "http://localhost:8000/analyze",
                    json={"repo_url": repo_url, "issue_number": int(issue_number)},
                    timeout=30
                )
                
                st.write("Raw response:", response)  # Debug output
                
                if response.status_code == 200:
                    result = response.json()
                    if "error" in result:
                        st.error(f"Analysis error: {result.get('raw_response', 'Unknown error')}")
                    else:
                        st.success("Analysis complete!")
                        st.json(result)
                else:
                    st.error(f"API Error ({response.status_code}): {response.text}")
                    
            except requests.exceptions.RequestException as e:
                st.error(f"Connection failed: {str(e)}")
            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")
    else:
        st.warning("Please enter both a repository URL and an issue number.")