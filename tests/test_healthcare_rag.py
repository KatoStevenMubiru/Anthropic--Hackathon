import unittest
from rag.healthcare_utils import categorize_query, format_healthcare_response

class TestHealthcareRAG(unittest.TestCase):
    def test_categorize_query(self):
        self.assertEqual(categorize_query("What are the symptoms of COVID-19?"), "diagnosis")
        self.assertEqual(categorize_query("Latest research on cancer treatments"), "research")
        self.assertEqual(categorize_query("How to manage diabetes?"), "patient_education")

    def test_format_healthcare_response(self):
        self.assertTrue(format_healthcare_response("Test response", "diagnosis").startswith("Diagnostic Information: "))
        self.assertTrue(format_healthcare_response("Test response", "treatment").startswith("Treatment Suggestion: "))
        self.assertTrue(format_healthcare_response("Test response", "general").startswith("Healthcare Information: "))

if __name__ == '__main__':
    unittest.main()
