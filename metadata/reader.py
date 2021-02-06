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
        return [
            Interview(interview).metadata_v3 for interview in self.original_interviews
        ]


class Interview:
    def __init__(self, interview):
        self.csv_data = interview
        self.metadata_v3 = self.__generate_interview()

    def get_interview_label(self):
        """Use Title to generate a label for the manifest according to the IIIF v3 specification"""
        return {"label": {"en": [self.csv_data["Title"]]}}

    def get_rights(self):
        """Use License to generate rights according to the IIIF v3 specification"""
        return {"rights": self.csv_data["License"]}

    def get_summary(self):
        """Use Abstract to generate a summary according to the IIIF v3 specification."""
        return {"summary": {"en": [self.csv_data["Abstract"]]}}

    def get_narrators(self):
        """Use values in narrator fields to get narrators to metadata section of a IIIF v3 metadata profile"""
        narrators = [
            narrator
            for narrator in [
                self.csv_data["Narrator Name"],
                self.csv_data["Narrator Name 2"],
                self.csv_data["Narrator Name 3"],
            ]
            if narrator != ""
        ]
        return {"label": {"en": ["Narrator"]}, "value": {"en": narrators}}

    def __generate_interview(self):
        return {
            "label": self.get_interview_label(),
            "rights": self.get_rights(),
            "summary": self.get_summary(),
            "narrators": self.get_narrators(),
        }


if __name__ == "__main__":
    print(MetadataReader("data/metadata.csv").interviews)
