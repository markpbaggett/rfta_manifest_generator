from csv import DictReader


class MetadataReader:
    def __init__(self, metadata_file):
        self.filename = metadata_file
        self.interviews = self.__read_data(metadata_file)

    @staticmethod
    def __read_data(path):
        with open(path, 'r') as my_csv:
            return [interview for interview in DictReader(my_csv, delimiter="|", quotechar="%")]


if __name__ == "__main__":
    print(MetadataReader("data/metadata.csv").interviews)
