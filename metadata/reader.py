from csv import DictReader
import arrow


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

    def get_interviewer(self):
        """Use value in interviewer field to get interviewers for metadata section of a IIIF v3 metadata profile"""
        interviewers = [
            interviewer
            for interviewer in [
                self.csv_data["Interviewer Name"],
            ]
            if interviewer != ""
        ]
        return {"label": {"en": ["Narrator"]}, "value": {"en": interviewers}}

    def get_navigation_date(self):
        """Use date recorded as navDate for manifest"""
        try:
            split_date = self.csv_data["Date Recorded"].split("/")
            for i, unit in enumerate(split_date):
                if len(unit) == 1:
                    split_date[i] = f"0{unit}"
            return f"{str(arrow.get('/'.join(split_date), 'MM/DD/YYYY').format('YYYY-MM-DD'))}T00:00:00Z"
        except arrow.parser.ParserMatchError:
            return ""

    def get_interviewer_location(self):
        """Get location of interviewer for manifest"""
        return {
            "label": {"en": ["Location Recorded"]},
            "value": {"en": [self.csv_data["Location Recorded"]]},
        }

    def get_narrator_location(self):
        """Get location of narrator for manifest"""
        return {
            "label": {"en": ["Narrator Location Recorded"]},
            "value": {"en": [self.csv_data["Narrator Location Recorded"]]},
        }

    def __generate_interview(self):
        return {
            "label": self.get_interview_label(),
            "rights": self.get_rights(),
            "summary": self.get_summary(),
            "narrators": self.get_narrators(),
            "interviewer": self.get_interviewer(),
            "navDate": self.get_navigation_date(),
            "interviewer_location": self.get_interviewer_location(),
            "narrator_location": self.get_narrator_location(),
        }


if __name__ == "__main__":
    print(MetadataReader("data/metadata.csv").interviews)
