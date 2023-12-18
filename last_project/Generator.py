import streamlit as st
import page1
import page2
import page3

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)


def main():
    with st.sidebar:
        page = st.selectbox(
            "",
            ("📝문제 만들기", "📄📱🎨Demo Page", "Code Page"),
        )

    if page == "📝문제 만들기":
        page1.render()
    elif page == "📄📱🎨Demo Page":
        page2.render()
    elif page == "Code Page":
        page3.render()


if __name__ == "__main__":
    main()
