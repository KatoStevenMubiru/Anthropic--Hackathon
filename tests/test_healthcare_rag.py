import unittest
from rag.healthcare_utils import categorize_query, format_healthcare_response, extract_key_points, generate_follow_up_questions
from rag.document_processor import process_healthcare_document
from rag.claude_llm import Claude
import io

class TestHealthcareRAG(unittest.TestCase):
    def setUp(self):
        # Mock Claude instance for testing
        self.claude_instance = Claude("claude-3-5-sonnet-20240620", "mock_api_key")

    def test_categorize_query(self):
        self.assertEqual(categorize_query("What are the symptoms of COVID-19?", self.claude_instance), "diagnosis")
        self.assertEqual(categorize_query("Latest research on cancer treatments", self.claude_instance), "research")
        self.assertEqual(categorize_query("How to manage diabetes?", self.claude_instance), "patient_education")
        self.assertEqual(categorize_query("Random non-medical query", self.claude_instance), "general")

    def test_format_healthcare_response(self):
        self.assertTrue(format_healthcare_response("Test response", "diagnosis", self.claude_instance).startswith("Diagnostic Information: "))
        self.assertTrue(format_healthcare_response("Test response", "treatment", self.claude_instance).startswith("Treatment Suggestion: "))
        self.assertTrue(format_healthcare_response("Test response", "general", self.claude_instance).startswith("Healthcare Information: "))

    def test_extract_key_points(self):
        response = "Point 1. Point 2. Point 3."
        key_points = extract_key_points(response, self.claude_instance)
        self.assertEqual(len(key_points), 3)
        self.assertTrue(all(point.strip() for point in key_points))

    def test_generate_follow_up_questions(self):
        response = "Diabetes is a chronic condition affecting blood sugar levels."
        questions = generate_follow_up_questions(response, "diagnosis", self.claude_instance)
        self.assertEqual(len(questions), 3)
        self.assertTrue(all(question.endswith("?") for question in questions))

    def test_process_healthcare_document(self):
        # Create a mock PDF file
        mock_pdf = io.BytesIO(b"%PDF-1.5\n%\xe2\xe3\xcf\xd3\n1 0 obj\n<</Type/Catalog/Pages 2 0 R>>\nendobj\n2 0 obj\n<</Type/Pages/Count 1/Kids[3 0 R]>>\nendobj\n3 0 obj\n<</Type/Page/MediaBox[0 0 595 842]/Parent 2 0 R/Resources<<>>/Contents 4 0 R>>\nendobj\n4 0 obj\n<</Length 21>>stream\nBT\n/F1 12 Tf\n(Test) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000015 00000 n \n0000000060 00000 n \n0000000111 00000 n \n0000000212 00000 n \ntrailer\n<</Size 5/Root 1 0 R>>\nstartxref\n281\n%%EOF")
        mock_pdf.name = "test.pdf"
        
        documents = process_healthcare_document(mock_pdf, include_vision=True)
        self.assertGreater(len(documents), 0)
        self.assertEqual(documents[0].metadata["source"], "test.pdf")

if __name__ == '__main__':
    unittest.main()