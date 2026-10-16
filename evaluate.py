from triage import generate_draft_reply, evaluate_draft_with_jev, make_final_decision
import json
from datetime import datetime

# Small set of test tickets
test_tickets = [
    {
        "id": 1,
        "ticket": "I was charged twice for my annual plan this morning and I still don't have access. This is the third time this has happened. If you don't fix it today I'm cancelling.",
        "expected": "ESCALATE"
    },
    {
        "id": 2,
        "ticket": "Hi, I just wanted to know the difference between the Pro and Enterprise plans. Can you help?",
        "expected": "AUTO-SEND or REVIEW"
    },
    {
        "id": 3,
        "ticket": "My login is not working after the password reset. I've tried three times already.",
        "expected": "ESCALATE or REVIEW"
    },
    {
        "id": 4,
        "ticket": "Thank you for the quick help last week. Everything is working fine now.",
        "expected": "AUTO-SEND"
    },
    {
        "id": 5,
        "ticket": "I need a refund for last month's charge. The product didn't work as advertised.",
        "expected": "ESCALATE or REVIEW"
    }
]

def run_evaluation():
    results = []

    print("Running evaluation on test tickets...\n")

    for item in test_tickets:
        print(f"Testing ticket {item['id']}...")

        draft = generate_draft_reply(item["ticket"])
        evaluation = evaluate_draft_with_jev(item["ticket"], draft)
        decision = make_final_decision(evaluation)

        result = {
            "id": item["id"],
            "ticket": item["ticket"],
            "expected": item["expected"],
            "decision": decision,
            "evaluation": evaluation,
            "draft": draft
        }
        results.append(result)

        print(f"  → Decision: {decision}\n")

    # Save results
    with open("evaluation_results.json", "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "results": results
        }, f, indent=2)

    print("Evaluation complete. Results saved to evaluation_results.json")
    return results

if __name__ == "__main__":
    run_evaluation()
