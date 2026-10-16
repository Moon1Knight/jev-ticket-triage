import streamlit as st
from triage import generate_draft_reply, evaluate_draft_with_jev, make_final_decision, save_log

st.set_page_config(page_title="Hybrid Ticket System", page_icon="🎫", layout="centered")

st.title("🎫 Hybrid Support Ticket System")
st.write("LLM generates a reply → Jev evaluates it → System decides")

ticket = st.text_area("Customer Ticket", height=150, placeholder="Paste the customer ticket here...")

if st.button("Analyze & Generate Reply", type="primary"):
    if not ticket.strip():
        st.warning("Please paste a ticket first.")
    else:
        with st.spinner("1. Generating draft reply with Gemma..."):
            draft = generate_draft_reply(ticket)

        with st.spinner("2. Evaluating draft with Jev..."):
            evaluation = evaluate_draft_with_jev(ticket, draft)
            decision = make_final_decision(evaluation)
            save_log(ticket, draft, evaluation, decision)

        st.success("Analysis complete!")

        # Show Draft
        st.subheader("Generated Draft Reply")
        st.info(draft)

        # Show Evaluation
        st.subheader("Jev Evaluation")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Tone OK", f"{evaluation['tone_ok']:.2f}")
            st.metric("Safe to Send", f"{evaluation['safe_to_send']:.2f}")
        with col2:
            st.metric("Risk of Escalation", f"{evaluation['risk_of_escalation']:.2f}")
            st.metric("Policy Safe", f"{evaluation['policy_safe']:.2f}")

        # Final Decision
        st.subheader("Final Decision")
        if "AUTO-SEND" in decision:
            st.success(decision)
        elif "ESCALATE" in decision:
            st.error(decision)
        else:
            st.warning(decision)
