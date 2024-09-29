import json
from docifyai.utils import utils
def main():
    ret_string = """
            ```json
            {
                "Introduction to the Project": [
                    "main.py",
                    "requirements.txt"
                ],
                "Setting Up the Environment": [
                    "requirements.txt"
                ],
                "Uploading Video Files": [
                    "main.py",
                    "process_video.py"
                ],
                "Subtitle Extraction": [
                    "process_video.py",
                    "send_data.py",
                    "sub_search.py"
                ],
                "Database Management": [
                    "get_database.py",
                    "query.py",
                    "send_data.py"
                ],
                "Cloud Storage Integration": [
                    "save_to_blob.py",
                    "process_video.py"
                ],
                "Querying Subtitles": [
                    "query.py",
                    "main.py"
                ],
                "Health Monitoring": [
                    "main.py"
                ],
                "Conclusion and Future Improvements": []
            }
        ```
        """
    # utils.get_json_from_gpt_response(ret_string)
    real_end = ret_string.rfind("}")
    real_start = ret_string.find("{")
    # ret_string = data[start + 3:end]
    return_string = ret_string[real_start: real_end+1]
    print(return_string)
    print(json.JSONDecoder().decode(return_string))

if __name__ == "__main__":
    main()