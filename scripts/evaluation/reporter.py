"""
Terminal reporter and JSON file persistence formatter.
"""
import json
import os


def save_evaluation_json(summary: dict, output_path: str = "data/eval_results.json"):
    parent = os.path.dirname(output_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"\n[OK] Evaluation report saved to: {output_path}")


def print_evaluation_report(summary: dict):
    m = summary["metrics"]
    print("\n" + "=" * 80)
    print("            ENTERPRISE RAG BENCHMARK & ACCURACY EVALUATION REPORT")
    print("=" * 80)
    print(f" Timestamp                : {summary['timestamp']}")
    print(f" Test Cases Evaluated     : {summary['test_cases_count']}")
    print("-" * 80)
    print(" METRIC                         | SCORE     | BENCHMARK TARGET | STATUS")
    print("-" * 80)
    print(f" Retrieval Precision @ K        | {m['precision']*100:6.2f}%   | > 80.0%          | {'[PASSED]' if m['precision'] >= 0.8 else '[NEEDS IMP]'}")
    print(f" Retrieval Recall @ K           | {m['recall']*100:6.2f}%   | > 80.0%          | {'[PASSED]' if m['recall'] >= 0.8 else '[NEEDS IMP]'}")
    print(f" Retrieval F1-Score             | {m['f1_score']*100:6.2f}%   | > 80.0%          | {'[PASSED]' if m['f1_score'] >= 0.8 else '[NEEDS IMP]'}")
    print(f" RBAC Security Filter Accuracy  | {m['rbac_security_accuracy_pct']:6.2f}%   | 100.0%           | {'[PASSED]' if m['rbac_security_accuracy_pct'] == 100 else '[FAILED]'}")
    print(f" Average Retrieval Latency      | {m['average_latency_seconds']:6.2f}s   | < 1.50s          | {'[PASSED]' if m['average_latency_seconds'] < 1.5 else '[SLOW]'}")
    print("=" * 80)

