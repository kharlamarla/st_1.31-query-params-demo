import streamlit as st


def main():
    st.title("Query Params Bug Test")
    
    st.divider()
    
    st.session_state["is_test"] = st.checkbox(
        "Is Test",
        value=st.session_state.get("is_test", False),
        key="is_test_widget",
    )
    
    if st.session_state.get("is_test", False):
        st.write("Is Test")
        
        st.query_params["is_test"] = "yes"
        
        st.caption("curr query params:")
        st.json((st.query_params.get_all("is_test")))
    else:
        st.write("Is Not Test")
        st.caption("curr query params:")
        st.json((st.query_params.get_all("is_test")))

        try:
            del st.query_params["is_test"]
        except KeyError:
            pass
        

if __name__ == '__main__':
    main()
