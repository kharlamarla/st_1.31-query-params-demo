import streamlit as st


def main():
    st.title("Query Params Bug Test - Second Page")

    st.divider()
    
    if st.session_state.get("is_test", False):
        st.write("Is Test")
        st.caption("curr query params:")
        st.json((st.query_params.get_all("is_test")))

    else:
        st.write("Is Not Test")
        st.caption("curr query params:")
        st.json((st.query_params.get_all("is_test")))

    st.divider()

    
    

if __name__ == '__main__':
    main()
    