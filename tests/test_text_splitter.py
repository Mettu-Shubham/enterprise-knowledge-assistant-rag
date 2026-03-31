import unittest

from src.processing.text_splitter import split_text_with_metadata


class TextSplitterTests(unittest.TestCase):

    def test_split_text_with_metadata_returns_chunk_metadata(self):
        text = "This is a short ethics policy. It explains expected staff behavior."

        chunks = split_text_with_metadata(text, "policy.txt")

        self.assertGreaterEqual(len(chunks), 1)
        self.assertEqual(chunks[0]["metadata"]["source"], "policy.txt")
        self.assertIn("chunk_id", chunks[0]["metadata"])
        self.assertIn("length", chunks[0]["metadata"])

    def test_split_text_with_metadata_skips_blank_input(self):
        self.assertEqual(split_text_with_metadata("   ", "empty.txt"), [])


if __name__ == "__main__":
    unittest.main()
