import streamlit as st
from agent import graph, State 
import time

def main():
    """
    This function sets up and runs the Streamlit application with a standard Streamlit look.
    """
    # Configure the page layout and title
    st.set_page_config(
        page_title="Multisource Search Agent", 
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Use standard Streamlit components for title and subtitle
    st.title("🕵️ Multisource Search Agent 🔎")
    st.markdown("I use multiple search engines to find the most comprehensive answers.")

    # About the agent section using an expander
    with st.expander("About this Agent"):
        st.write("This application leverages a multi-agent system built with LangGraph to perform parallel research from Google, Bing, and Reddit. The agent then analyzes and synthesizes the findings to provide a single, comprehensive answer.")
        st.write("The agent's workflow is a multi-step process:")
        st.write("1. **Parallel Search:** Searches across Google, Bing, and Reddit simultaneously.")
        st.write("2. **Reddit Post Retrieval:** Finds and retrieves valuable information from relevant Reddit threads.")
        st.write("3. **Analysis:** analyzes the information from each source independently.")
        st.write("4. **Synthesis:** Combines all analyses to generate a single final answer.")

    st.markdown("---")

    # Main input and button section
    user_input = st.text_input("What would you like me to research?", placeholder="e.g., How to build a solar-powered garden light?", key="user_input")

    if st.button("Start Research"):
        if not user_input:
            st.warning("Please enter a question to start the research.")
            return

        # Use st.status for a clean, expanding progress indicator
        with st.status("Starting research...", expanded=True) as status:
            try:
                status.update(label="Initializing agent...", state="running")
                initial_state = State(
                    messages=[{"role": "user", "content": user_input}],
                    user_question=user_input,
                )
                
                # Use st.progress for a progress bar
                progress_bar = st.progress(0, text="Agent progress...")
                
                # We will store the final answer in this variable as soon as it's generated.
                final_answer = None

                # LangGraph's stream method allows us to get updates as each node finishes
                total_nodes = 9 
                nodes_completed = 0
                
                for step in graph.stream(initial_state):
                    for node_name, node_output in step.items():
                        if node_name == "__end__":
                            continue
                        
                        nodes_completed += 1
                        progress_percentage = min(int((nodes_completed / total_nodes) * 100), 100)
                        progress_bar.progress(progress_percentage, text=f"Executing node: {node_name}...")
                        
                        # Update status with a more specific message for each node
                        if node_name == "google_search":
                            status.update(label="Searching Google...", state="running")
                        elif node_name == "bing_search":
                            status.update(label="Searching Bing...", state="running")
                        elif node_name == "reddit_search":
                            status.update(label="Searching Reddit for relevant threads...", state="running")
                        elif node_name == "analyze_reddit_posts":
                            status.update(label="Analyzing and selecting key Reddit threads...", state="running")
                        elif node_name == "retrieve_reddit_posts":
                            status.update(label="Retrieving comments from selected Reddit threads...", state="running")
                        elif node_name == "analyze_google_results":
                            status.update(label="Analyzing Google search findings...", state="running")
                        elif node_name == "analyze_bing_results":
                            status.update(label="Analyzing Bing search findings...", state="running")
                        elif node_name == "analyze_reddit_results":
                            status.update(label="Analyzing information from Reddit...", state="running")
                        elif node_name == "synthesize_analyses":
                            status.update(label="Synthesizing all analyses into a final answer...", state="running")
                            # This is the key change: Capture the final answer here before the stream ends.
                            final_answer = node_output.get("final_answer")

                progress_bar.progress(100, text="Research complete!")
                time.sleep(1) # Give a moment for the user to see 100%

                if final_answer:
                    status.update(label="✨ Synthesis complete. Displaying final answer.", state="complete", expanded=False)
                    
                    st.markdown("---")
                    st.success("### Final Answer")
                    st.write(final_answer)
                else:
                    status.update(label="⚠️ Failed to generate a final answer.", state="error", expanded=False)
                    st.error("I'm sorry, I was unable to generate a final answer. Please try a different query.")

            except Exception as e:
                status.update(label="❌ An error occurred during the process.", state="error", expanded=False)
                st.error(f"An error occurred: {e}")
                st.info("Please check the terminal for detailed logs.")

if __name__ == "__main__":
    main()