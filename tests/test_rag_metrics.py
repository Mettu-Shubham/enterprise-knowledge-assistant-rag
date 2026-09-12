"""
Unit tests for RAGEvaluator metrics calculation and RBAC security assertions.
"""
import unittest
from scripts.evaluation.benchmark_dataset import BENCHMARK_DATASET
from scripts.evaluation.evaluator import RAGEvaluator


class MockRetriever:
    def retrieve(self, query, role="client", domain=None):
        if role == "client":
            return [
                {
                    "page_content": "Public policy document for all users.",
                    "metadata": {"classification": "public", "domain": "govt_policy"}
                }
            ]
        return [
            {
                "page_content": "Code of ethics outlines staff behavior, integrity, and respect.",
                "metadata": {"classification": "internal", "domain": "govt_policy"}
            }
        ]


class MockPipeline:
    def __init__(self):
        self.retriever = MockRetriever()

    def ensure_index(self):
        pass


class RAGMetricsTests(unittest.TestCase):

    def setUp(self):
        self.evaluator = RAGEvaluator(pipeline=MockPipeline(), dataset=BENCHMARK_DATASET)

    def test_evaluate_single_case_returns_valid_metrics(self):
        case = BENCHMARK_DATASET[0]
        res = self.evaluator.evaluate_case(case)

        self.assertIn("precision", res)
        self.assertIn("recall", res)
        self.assertIn("f1_score", res)
        self.assertTrue(res["rbac_passed"])
        self.assertEqual(res["security_violations"], 0)

    def test_rbac_security_filtering_blocks_unauthorized_classifications(self):
        client_case = {
            "id": 99,
            "query": "Confidential financial strategy",
            "role": "client",
            "domain": None,
            "expected_keywords": [],
            "unauthorized_classifications": ["internal", "confidential"]
        }
        res = self.evaluator.evaluate_case(client_case)
        self.assertTrue(res["rbac_passed"])
        self.assertEqual(res["security_violations"], 0)

    def test_run_full_evaluation_generates_valid_summary(self):
        summary = self.evaluator.run_full_evaluation()

        self.assertIn("metrics", summary)
        self.assertGreaterEqual(summary["metrics"]["precision"], 0.0)
        self.assertEqual(summary["metrics"]["rbac_security_accuracy_pct"], 100.0)


if __name__ == "__main__":
    unittest.main()
