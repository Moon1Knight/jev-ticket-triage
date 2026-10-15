from typesafe_sdk import Choice, Noul, Score, TypeSafeClient
from dotenv import load_dotenv
import os
import json
from datetime import datetime


load_dotenv()

client = TypeSafeClient(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api",
        model="~typesafe/jev-latest"
)

def triage_ticket(ticket_text: str):

    response = client.system_one(
            state=ticket_text,
            questions={
                "team": Choice(
                    instructions="Which team should handle this ticket?",
                    criteria={
                        "billing": "Charges, refunds, invoices, payments, subscriptions",
                        "technical": "Bugs, errors, product not working, integrations",
                        "account": "Login problems, password, access, permissions",
                        "sales": "Pricing questions, upgrades, new plans, demos"
                    }
                ),
                "urgency": Score(
                    instructions="How urgent is this ticket?",
                    criteria=[
                        "Can wait a few days",
                        "Should be handled today",
                        "Needs immediate attention"
                    ]
                ),
                "escalate": Noul(
                    instructions="Should this ticket be escalated to a human agent right now?"
                ),
                "churn_risk": Noul(
                    instructions="Does the customer sound like they might cancel or leave?"
                )
            }
        )


    answers = response.answers
    return {
            "team": answers["team"].choice,
            "team_confidence": answers["team"].confidence,
            "urgency_score": answers["urgency"].score,
            "escalate": answers["escalate"].noul,
            "churn_risk": answers["churn_risk"].noul
        }

def make_decision(result: dict):
    """
    Simple rules based on Jev's answers.
    """
    if result["escalate"] > 0.75 or result["churn_risk"] > 0.80:
        return "ESCALATE TO HUMAN"
    elif result["team_confidence"] < 0.70:
        return "SEND TO REVIEW (low confidence)"
    else:
        return f"AUTO-ROUTE TO {result['team'].upper()}"


def save_log(ticket : str , result : dict , decision : str):
    log_entry = {
        "timestamp" : datetime.now().isoformat(),
        "ticket" : ticket,
        "result" : result,
        "decision" : decision
    }

    if os.path.exists("logs.json"):
        with open("logs.json", "r") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(log_entry)

    with open("logs.json", "w") as f:
        json.dump(logs, f, indent=2)

    print("Log saved successfully")


# This part runs when you execute the file
if __name__ == "__main__":

    print("=== Smart Ticket Triage (Phase 1) ===")
    ticket = input("\nPaste the customer ticket here:\n> ")

    print("\nSending to Jev... please wait...")
    result = triage_ticket(ticket)
    decision = make_decision(result)

    save_log(ticket, result, decision)

    print("\n---------- RESULTS ----------")
    print(f"Recommended Team     : {result['team']}")
    print(f"Team Confidence      : {result['team_confidence']:.2f}")
    print(f"Urgency Score        : {result['urgency_score']:.2f}")
    print(f"Escalate Probability : {result['escalate']:.2f}")
    print(f"Churn Risk           : {result['churn_risk']:.2f}")
    print(f"\nFinal Decision       : {decision}")
    print("-----------------------------")
