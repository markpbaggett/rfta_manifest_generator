from csv import DictReader
import arrow
from uuid import uuid4


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
        return {"label": {"en": ["Narrators"]}, "value": {"en": narrators}}

    def get_interviewer(self):
        """Use value in interviewer field to get interviewers for metadata section of a IIIF v3 metadata profile"""
        interviewers = [
            interviewer
            for interviewer in [
                self.csv_data["Interviewer Name"],
            ]
            if interviewer != ""
        ]
        return {"label": {"en": ["Interviewers"]}, "value": {"en": interviewers}}

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
            "value": {"en": [self.csv_data["Location Recorded"].split("\n")[0]]},
        }

    def get_narrator_location(self):
        """Get location of narrator for manifest"""
        return {
            "label": {"en": ["Narrator Location Recorded"]},
            "value": {"en": [self.csv_data["Narrator Location Recorded"]]},
        }

    def get_aat_format(self):
        """Process AAT Format column to get format for manifest"""
        return {
            "label": {"en": ["AAT Format"]},
            "value": {
                "en": [
                    self.csv_data["AAT Format "]
                    .split("http://vocab.getty.edu/aat/")[0]
                    .rstrip()
                ]
            },
        }

    def get_topics(self):
        """Use values in topic fields to get topics to metadata section of a IIIF v3 metadata profile"""
        topics = [
            topic
            for topic in [
                self.csv_data["LCSH_Topic_1"],
                self.csv_data["LCSH_Topic_2"],
                self.csv_data["LCSH_Topic_3"],
            ]
            if topic != ""
        ]
        return {"label": {"en": ["Topics"]}, "value": {"en": topics}}

    def get_places(self):
        """Use values in geographic subject fields to get places to metadata section of a IIIF v3 metadata profile"""
        places = [
            place
            for place in [
                self.csv_data["LCSH_Geo_1"],
                self.csv_data["LCSH_Geo_2"],
            ]
            if place != ""
        ]
        return {"label": {"en": ["Places"]}, "value": {"en": places}}

    def get_names(self):
        """Use values in name subject fields to get names to metadata section of a IIIF v3 metadata profile"""
        names = [
            name
            for name in [
                self.csv_data["LCSH_Name_1"],
                self.csv_data["LCSH_Name_2"],
            ]
            if name != ""
        ]
        return {"label": {"en": ["Subject Names"]}, "value": {"en": names}}

    def __get_duration_pair(self, next_value):
        if next_value.rstrip() == "":
            return self.csv_data["Interview Stop TC"]
        else:
            return next_value

    def get_interview_questions(self):
        """Build interview questions from CSV metadata."""
        canvas_id = (
            "https://digital.lib.utk.edu/collections/islandora/PID/datastream/PROXY"
        )
        keys = [
            key
            for key, value in self.csv_data.items()
            if key.startswith("Interview_Question_") and "TC" not in key
        ]
        interview_questions = [
            (
                self.csv_data[key],
                self.csv_data[f"{key}_TC"],
                self.__get_duration_pair(
                    self.csv_data[
                        f"{key.replace(key.split('_')[2],str(int(key.split('_')[2])+1))}_TC"
                    ]
                ),
            )
            for key in keys
            if self.csv_data[key].rstrip() != ""
        ]
        if len(interview_questions) > 0:
            return {
                "type": "Range",
                "id": canvas_id,
                "label": {"en": ["Interview Questions"]},
                "items": [
                    MediaFragment(
                        question[0], canvas_id, question[1], question[2]
                    ).build_range()
                    for question in interview_questions
                ],
            }
        else:
            return {}

    # def get_chapters(self):
    #     """Build chapters from CSV metadata."""
    #     canvas_id = (
    #         "https://digital.lib.utk.edu/collections/islandora/PID/datastream/PROXY"
    #     )
    #     keys = [
    #         key
    #         for key, value in self.csv_data.items()
    #         if key.startswith("Chapter_") and "TC" not in key
    #     ]
    #     chapters = [
    #         (self.csv_data[key], self.csv_data[f"{key}_TC"])
    #         for key in keys
    #         if self.csv_data[key].rstrip() != ""
    #     ]
    #     if len(chapters) > 0:
    #         return {
    #             "type": "Range",
    #             "id": canvas_id,
    #             "label": {"en": ["Chapters"]},
    #             "items": [
    #                 MediaFragment(chapter, canvas_id).build_range()
    #                 for chapter in chapters
    #             ],
    #         }
    #     else:
    #         return {}

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
            "aat_format": self.get_aat_format(),
            "topics": self.get_topics(),
            "places": self.get_places(),
            "names": self.get_names(),
            "interview question": self.get_interview_questions(),
            # "chapters": self.get_chapters(),
        }


class MediaFragment:
    def __init__(self, label, canvas_id, start, end):
        self.range_id = uuid4()
        self.label = label
        self.canvas_id = canvas_id
        print(f"Start: {start}")
        print(f"End: {end}")
        print(self.label)
        self.start = self.__get_duration(start.replace("~", ""))
        self.end = self.__get_duration(end.replace("~", ""))

    def build_range(self):
        return {
            "type": "Range",
            "id": f"http://{self.range_id}",
            "label": {"en": [self.label.rstrip()]},
            "items": [
                {"type": "Canvas", "id": f"{self.canvas_id}#t={self.start},{self.end}"}
            ],
        }

    @staticmethod
    def __get_duration(timestamp):
        duration_split = timestamp.split(":")
        hours = int(duration_split[0]) * 60 * 60
        minutes = int(duration_split[1]) * 60
        return hours + minutes + int(duration_split[2])


if __name__ == "__main__":
    print(MetadataReader("data/metadata.csv").interviews[-2])
