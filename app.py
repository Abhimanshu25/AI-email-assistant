import streamlit as st

from email_analyzer import analyze_email
from email_reply import generate_reply


st.set_page_config(
    page_title="AI Email Assistant",
    page_icon="📧",
    layout="centered"
)


st.title("📧 AI Email Assistant")

st.write(
    "Paste an email below to analyze it and generate a reply."
)


# Initialize session state

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "email_text" not in st.session_state:
    st.session_state.email_text = ""


# Email input

email_text = st.text_area(
    "Paste your email here:",
    height=250,
    placeholder="Paste the email you want to analyze..."
)


# Analyze button

if st.button("🔍 Analyze Email", use_container_width=True):

    if not email_text.strip():

        st.warning(
            "Please enter an email first."
        )

    else:

        try:

            with st.spinner("AI is analyzing the email..."):

                analysis = analyze_email(email_text)

                st.session_state.analysis = analysis
                st.session_state.email_text = email_text

        except Exception as e:

            st.error(str(e))


# Display analysis

if st.session_state.analysis:

    analysis = st.session_state.analysis

    st.divider()

    st.subheader("📊 Email Analysis")

    st.write(
        "### Summary"
    )

    st.write(
        analysis["summary"]
    )


    col1, col2 = st.columns(2)

    with col1:

        st.write("### Category")

        st.info(
            analysis["category"]
        )

    with col2:

        st.write("### Priority")

        priority = analysis["priority"]

        if priority == "High":

            st.error(priority)

        elif priority == "Medium":

            st.warning(priority)

        else:

            st.success(priority)


    st.write("### Action Required")

    if analysis["action_required"]:

        st.warning("Yes")

    else:

        st.success("No")


    st.write("### Action Items")

    if analysis["action_items"]:

        for item in analysis["action_items"]:

            st.write(
                f"• {item}"
            )

    else:

        st.write(
            "No action items found."
        )


    st.write("### Deadline")

    if analysis["deadline"]:

        st.info(
            analysis["deadline"]
        )

    else:

        st.write(
            "Not specified"
        )


    st.divider()

    st.subheader("✍️ Generate Reply")


    tone = st.selectbox(

        "Select reply tone:",

        [
            "Professional",
            "Friendly",
            "Concise",
            "Formal"
        ]
    )


    if st.button(
        "✨ Generate Reply",
        use_container_width=True
    ):

        try:

            with st.spinner(
                "Generating reply..."
            ):

                reply = generate_reply(
                    st.session_state.email_text,
                    st.session_state.analysis,
                    tone
                )

                st.session_state.reply = reply

        except Exception as e:

            st.error(
                str(e)
            )


# Display reply

if "reply" in st.session_state:

    st.divider()

    st.subheader("📨 Suggested Reply")

    st.text_area(
        "You can edit the reply below:",
        value=st.session_state.reply,
        height=250
    )