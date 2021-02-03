from csv import DictReader


class MetadataReader:
    def __init__(self, metadata_file):
        self.filename = metadata_file
        self.original_interviews = self.__read_data(metadata_file)
        self.interviews = self.__clean_interviews()

    @staticmethod
    def __read_data(path):
        with open(path, "r") as my_csv:
            return [
                interview
                for interview in DictReader(my_csv, delimiter="|", quotechar="%")
            ]

    def __clean_interviews(self):
        return [Interview(interview).metadata for interview in self.original_interviews]


class Interview:
    def __init__(self, interview):
        self.csv_data = interview
        self.metadata = self.__generate_interview()

    def get_interview_label(self):
        """Use Title to generate a label for the Manifest."""
        return self.csv_data["Title"]

    def get_rights(self):
        """Use License to generate rights for the Manifest."""
        return self.csv_data["License"]

    def get_summary(self):
        """Use Abstract to generate a summary for the manifest."""
        return self.csv_data["Abstract"]

    def __generate_interview(self):
        return {
            "label": self.get_interview_label(),
            "rights": self.get_rights(),
            "summary": self.get_summary(),
        }


if __name__ == "__main__":
    print(MetadataReader("data/metadata.csv").interviews)
