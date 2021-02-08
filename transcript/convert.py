import webvtt
import os


class SRTConverter:
    def __init__(self, path_to_srt_files, path_to_web_vtt_files="data/web_vtt_files/"):
        self.srt_path = path_to_srt_files
        self.vtt_path = path_to_web_vtt_files
        self.__create_output_path(path_to_web_vtt_files)

    @staticmethod
    def __create_output_path(output_path):
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        return

    def convert_files_to_vtt(self):
        for path, directories, files in os.walk(self.srt_path):
            for file in files:
                webvtt.from_srt(f"{path}/{file}").save(
                    f"{self.vtt_path}{file.replace('srt', 'vtt')}"
                )


if __name__ == "__main__":
    SRTConverter("data/srt_transcripts").convert_files_to_vtt()
