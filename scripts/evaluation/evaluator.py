"""
Core calculation engine for Precision@K, Recall@K, F1-Score, RBAC Security Accuracy, and Query Latency.
"""
import time
from datetime import datetime
from scripts.evaluation.benchmark_dataset import BENCHMARK_DATASET


class RAGEvaluator:

    def __init__(self, pipeline, dataset=None):
        self.pipeline = pipeline
        self.dataset = dataset or BENCHMARK_DATASET

    def evaluate_case(self, test_case: dict) -> dict:
        query = test_case["query"]
        role = test_case["role"]
        domain = test_case.get("domain")

        start_time = time.perf_counter()

        if self.pipeline.retriever is None:
            self.pipeline.ensure_index()

        retrieved_docs = []
        if self.pipeline.retriever:
            retrieved_docs = self.pipeline.retriever.retrieve(
                query, role=role, domain=domain
            )

        elapsed_time = time.perf_counter() - start_time

        expected_keywords = set(test_case.get("expected_keywords", []))
        relevant_chunks = 0
        security_violations = 0

        for doc in retrieved_docs:
            content = getattr(doc, "page_content", doc.get("content", "") if isinstance(doc, dict) else str(doc)).lower()
            metadata = getattr(doc, "metadata", doc.get("metadata", {}) if isinstance(doc, dict) else {}) or {}

            if expected_keywords and any(kw.lower() in content for kw in expected_keywords):
                relevant_chunks += 1

            classification = str(metadata.get("classification", "")).lower()
            unauthorized = test_case.get("unauthorized_classifications", [])
            if classification in [u.lower() for u in unauthorized]:
                security_violations += 1

        k = len(retrieved_docs) if retrieved_docs else 1
        precision = (relevant_chunks / k) if expected_keywords else 1.0

        total_expected = max(1, len(expected_keywords))
        recall = min(1.0, (relevant_chunks / total_expected)) if expected_keywords else 1.0

        f1_score = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
        rbac_passed = (security_violations == 0)

        return {
            "id": test_case["id"],
            "query": query,
            "role": role,
            "retrieved_count": len(retrieved_docs),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1_score, 4),
            "security_violations": security_violations,
            "rbac_passed": rbac_passed,
            "latency_seconds": round(elapsed_time, 4)
        }

    def run_full_evaluation(self) -> dict:
        self.pipeline.ensure_index()
        results = []
        total_precision = 0.0
        total_recall = 0.0
        total_f1 = 0.0
        total_latency = 0.0
        rbac_successes = 0

        for test_case in self.dataset:
            res = self.evaluate_case(test_case)
            results.append(res)
            total_precision += res["precision"]
            total_recall += res["recall"]
            total_f1 += res["f1_score"]
            if res["rbac_passed"]:
                rbac_successes += 1
            total_latency += res["latency_seconds"]

        n = len(self.dataset)
        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "test_cases_count": n,
            "metrics": {
                "precision": round(total_precision / n, 4),
                "recall": round(total_recall / n, 4),
                "f1_score": round(total_f1 / n, 4),
                "rbac_security_accuracy_pct": round((rbac_successes / n) * 100, 2),
                "average_latency_seconds": round(total_latency / n, 4)
            },
            "detailed_results": results
        }
