"""
CLI Entry Point Launcher for RAG Evaluation.
"""
from src.config.settings import get_settings
from src.pipeline.rag_pipeline import RAGPipeline
from scripts.evaluation.evaluator import RAGEvaluator
from scripts.evaluation.reporter import print_evaluation_report, save_evaluation_json


def main():
    settings = get_settings()
    pipeline = RAGPipeline(settings)
    evaluator = RAGEvaluator(pipeline)

    print("Running enterprise RAG benchmark evaluation...")
    summary = evaluator.run_full_evaluation()
    save_evaluation_json(summary)
    print_evaluation_report(summary)


if __name__ == "__main__":
    main()
