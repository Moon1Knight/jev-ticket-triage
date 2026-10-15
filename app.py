import streamlit as st
from triage import triage_ticket, make_decision, save_log

st.set_page_config(page_title="Smart Ticket Triage", page_icon="🎫")

st.title("🎫 Smart Ticket Triage System")
st.write("Paste a customer support ticket below. Jev will analyze it.")

ticket = st.text_area("Customer Ticket", height=150, placeholder="Paste the ticket here...")

if st.button("Analyze Ticket"):
    if not ticket.strip():
        st.warning("Please paste a ticket first.")
    else:
        with st.spinner("Sending to Jev..."):
            result = triage_ticket(ticket)
            decision = make_decision(result)
            save_log(ticket, result, decision)

        st.success("Analysis complete!")

        st.subheader("Results")
        st.write(f"**Recommended Team:** {result['team']}")
        st.write(f"**Team Confidence:** {result['team_confidence']:.2f}")
        st.write(f"**Urgency Score:** {result['urgency_score']:.2f}")
        st.write(f"**Escalate Probability:** {result['escalate']:.2f}")
        st.write(f"**Churn Risk:** {result['churn_risk']:.2f}")

        st.markdown("---")
        st.subheader("Final Decision")
        if "ESCALATE" in decision:
            st.error(decision)
        else:
            st.success(decision)
