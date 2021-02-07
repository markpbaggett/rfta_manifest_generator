import unittest
from metadata.reader import Interview
from metadata.sample_interview_data import interview_data


class CheckDescriptiveMetadata(unittest.TestCase):
    def __init__(self, metadata_element):
        self.metadata_element = metadata_element

    def check_label(self):
        self.assertIn("label", self.metadata_element)
        self.assertIn("en", self.metadata_element["label"])
        self.assertIsInstance(self.metadata_element["label"]["en"], list)

    def check_value(self):
        self.assertIn("value", self.metadata_element)
        self.assertIn("en", self.metadata_element["value"])
        self.assertIsInstance(self.metadata_element["value"]["en"], list)


class TestDescriptiveMetadata(unittest.TestCase):
    def test_narrator(self):
        CheckDescriptiveMetadata(
            Interview(interview_data).get_narrators()
        ).check_label()
        CheckDescriptiveMetadata(
            Interview(interview_data).get_narrators()
        ).check_value()

    def test_interviewer(self):
        CheckDescriptiveMetadata(
            Interview(interview_data).get_interviewer()
        ).check_label()
        CheckDescriptiveMetadata(
            Interview(interview_data).get_interviewer()
        ).check_value()

    def test_interviewer_location(self):
        CheckDescriptiveMetadata(
            Interview(interview_data).get_interviewer_location()
        ).check_label()
        CheckDescriptiveMetadata(
            Interview(interview_data).get_interviewer_location()
        ).check_value()

    def test_narrator_location(self):
        CheckDescriptiveMetadata(
            Interview(interview_data).get_narrator_location()
        ).check_label()
        CheckDescriptiveMetadata(
            Interview(interview_data).get_narrator_location()
        ).check_value()

    def test_aat_format(self):
        CheckDescriptiveMetadata(
            Interview(interview_data).get_aat_format()
        ).check_label()
        CheckDescriptiveMetadata(
            Interview(interview_data).get_aat_format()
        ).check_value()


if __name__ == "__main__":
    unittest.main()
