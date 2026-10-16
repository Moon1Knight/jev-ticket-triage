from typesafe_sdk import Choice, Noul, Score, TypeSafeClient
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from datetime import datetime

load_dotenv()

# Jev client (decision model)
jev_client = TypeSafeClient(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api",
    model="~typesafe/jev-latest"
)

# Generative LLM client (Gemma free)
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found. Please check your .env file.")

llm_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

def generate_draft_reply(ticket: str) -> str:
    """Generate a polite support reply using free Gemma model"""
    response = llm_client.chat.completions.create(
        model="nvidia/nemotron-3-super-120b-a12b:free",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful and professional customer support agent. Write a short, polite, and empathetic reply to the customer ticket. Do not promise specific timelines or refunds unless clearly appropriate. Keep the reply under 120 words."
            },
            {
                "role": "user",
                "content": ticket
            }
        ],
        max_tokens=300,
        temperature=0.4
    )
    return response.choices[0].message.content.strip()


def evaluate_draft_with_jev(ticket: str, draft: str):
    """Ask Jev to evaluate the generated draft"""
    state = {
        "original_ticket": ticket,
        "draft_reply": draft
    }

    response = jev_client.system_one(
        state=state,
        questions={
            "tone_ok": Noul(instructions="Is the tone of the draft reply professional and empathetic?"),
            "safe_to_send": Noul(instructions="Is it safe to send this reply without human review?"),
            "risk_of_escalation": Noul(instructions="Does this reply risk making the customer more upset?"),
            "policy_safe": Noul(instructions="Does the reply avoid making unsafe promises (like guaranteed refunds or exact timelines)?")
        }
    )

    answers = response.answers
    return {
        "tone_ok": answers["tone_ok"].noul,
        "safe_to_send": answers["safe_to_send"].noul,
        "risk_of_escalation": answers["risk_of_escalation"].noul,
        "policy_safe": answers["policy_safe"].noul
    }


def make_final_decision(eval_result: dict) -> str:
    if eval_result["safe_to_send"] > 0.80 and eval_result["risk_of_escalation"] < 0.35 and eval_result["policy_safe"] > 0.75:
        return "AUTO-SEND REPLY"
    elif eval_result["risk_of_escalation"] > 0.70:
        return "ESCALATE TO HUMAN"
    else:
        return "NEEDS REVISION / HUMAN REVIEW"


def save_log(ticket: str, draft: str, eval_result: dict, decision: str):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "ticket": ticket,
        "draft_reply": draft,
        "evaluation": eval_result,
        "decision": decision
    }

    if os.path.exists("logs.json"):
        with open("logs.json", "r") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(log_entry)

    with open("logs.json", "w") as f:
        json.dump(logs, f, indent=2)


# For testing in terminal
if __name__ == "__main__":
    print("=== Hybrid Ticket System (Phase 4) ===")
    ticket = input("\nPaste the customer ticket:\n> ")

    print("\n1. Generating draft reply with Gemma...")
    draft = generate_draft_reply(ticket)
    print("\nDraft Reply:")
    print(draft)

    print("\n2. Evaluating draft with Jev...")
    evaluation = evaluate_draft_with_jev(ticket, draft)
    decision = make_final_decision(evaluation)

    save_log(ticket, draft, evaluation, decision)

    print("\n---------- EVALUATION ----------")
    print(f"Tone OK            : {evaluation['tone_ok']:.2f}")
    print(f"Safe to Send       : {evaluation['safe_to_send']:.2f}")
    print(f"Risk of Escalation : {evaluation['risk_of_escalation']:.2f}")
    print(f"Policy Safe        : {evaluation['policy_safe']:.2f}")
    print(f"\nFinal Decision     : {decision}")
    print("--------------------------------")
