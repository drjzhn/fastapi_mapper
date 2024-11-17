import streamlit as st
import json
import pickle
from typing import Dict, List

######################################################################################
## TO DO:
## for real data, we should do the following:
## generate source_concept_id on load
## sort by source_concept_count
######################################################################################
# General function explainer
# Data:
# - Mappings kept in .json that contains only id to id mappings + metdata
# - source_concept and target_concept classes are used to hold all other information
# - Simulate objects stored as pickle and being reloaded
# Frontend:
# - The UI displays concept_name via a *lookup*
# - The UI is paginated and shows 20 concepts at a time
# - Updates across entire page are passed to the json at once
# Handling changes:
# - Edits to the page are held in a dict with global index for concepts
# - When page is confirmed, json updated based on index, and entire json is dumped.
######################################################################################

# simulate restoring a session following NLP mapping...
def load_data():
    # source concepts
    with open("data/source_concepts.pkl", "rb") as f:
        source_concepts = pickle.load(f)
        source_lookup = {c.concept_id: c.concept_name for c in source_concepts}

    # target concepts
    with open("data/target_concepts.pkl", "rb") as f:
        target_concepts = pickle.load(f)
        target_lookup = {c.concept_id: c.concept_name for c in target_concepts}
        # list for the select box...
        target_options = [(c.concept_id, c.concept_name) for c in target_concepts]

    # mappings
    with open("data/concept_mappings.json", "r") as f:
        mappings = json.load(f)

    return source_lookup, target_lookup, target_options, mappings

def save_mappings(mappings: List[Dict]):
    # for now, dump everything in one go (even though only 20 are updated)
    # might be more cerebral way to do this
    # need to add error handling
    with open("data/concept_mappings.json", "w") as f:
        json.dump(mappings, f, indent=2)

def main():
    st.title("Validate Mappings")

    if 'page' not in st.session_state:
        st.session_state.page = 0
    if 'modified_mappings' not in st.session_state:
        st.session_state.modified_mappings = {} # this will hold new mappings

    # load data
    source_lookup, target_lookup, target_options, mappings = load_data()

    # pagination
    # index of first item on each page: start_idx = page number * items_per_page
    items_per_page = 20
    start_idx = st.session_state.page * items_per_page
    end_idx = min(start_idx + items_per_page, len(mappings))
    # add 'extra page' for rounding down to catch remainder items
    total_pages = (len(mappings) + (items_per_page - 1)) // items_per_page 

    # show current page
    st.write(f"Showing mappings {start_idx + 1} to {end_idx} of {len(mappings)}")

    # show mapping UI
    for idx, mapping in enumerate(mappings[start_idx:end_idx]):
        global_idx = start_idx + idx # i.e. active concept idx across each dataset  
        source_id = mapping['source_concept_id']
        current_target_id = mapping['target_concept_id']
        
        with st.container():
            cols = st.columns([4, 4, 2, 4])
            
            # source concept - we display via the lookup
            with cols[0]:
                st.write(f"Source Concept: {source_lookup[source_id]}")
            
            # current target via lookup
            with cols[1]:
                st.write(f"Target Concept: {target_lookup[current_target_id]}")
            
            # similarity score
            with cols[2]:
                score = mapping['similarity_score']
                st.write(f"Similarity Score: {score}")
            
            # text entry (autoselect)
            with cols[3]:

                default_idx = 0
                target_choices = [("", "No Change")] + target_options
                
                selected = st.selectbox(
                    "Select new target concept if needed",
                    target_choices,
                    default_idx,
                    format_func=lambda x: x[1] if x[1] else "No Change", # show only names, not IDs
                    key=f"select_{global_idx}"
                )
                
                ## LOGIC TIME
                # if select box is used, then track these updates in global dict 
                if selected[0]:  # i.e. only where new target selected, because default is ""
                    st.session_state.modified_mappings[global_idx] = selected[0]
                # if user goes back to "No Change" then we go to else and the globalidx is removed
                elif global_idx in st.session_state.modified_mappings:
                    del st.session_state.modified_mappings[global_idx]

    # navigation bar
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("< Previous Page", disabled=st.session_state.page == 0):
            st.session_state.page -= 1
            st.rerun()
            
    with col2:
        if st.button("CONFIRM ALL", type="primary"):

            # MAIN BIT...
            # update mapping .json and save 
            for idx, mapping in enumerate(mappings):
                if idx in st.session_state.modified_mappings:
                    mapping['target_concept_id'] = st.session_state.modified_mappings[idx]
                if idx >= start_idx and idx < end_idx:  # If on current page
                    mapping['similarity_score'] = "validated"
    
            save_mappings(mappings)
            
            # clear modified_mappings dict
            st.session_state.modified_mappings = {}

            # automatically move to next page
            if st.session_state.page < total_pages - 1:
                st.session_state.page += 1
                st.success(f"Saved modified mappings. Moving to next page...")
                st.rerun()
            else:
                st.success(f"Saved mappings. This is the last page...")

    with col3:
        if st.button("Next Page >", disabled=st.session_state.page >= total_pages - 1):
            st.session_state.page += 1
            st.rerun()

if __name__ == "__main__":
    main()