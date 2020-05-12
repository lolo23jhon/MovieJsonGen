import json
import argparse
from random import choice, randrange


class VideoGenerator:
    #####################################################
    #####################################################

    VIDEO_TYPE = {
        "movie": {
            "id_base": "M{global_entry_num}G{genre}"
        },
        "episode": {
            "id_base": "E{episode_num}S{season_num}S{global_entry_num}G{genre}"
        }
    }

    LENGTH = {
        "movie": (5400, 9000),
        "episode": (10, 3600)
    }

    GENRE = {
        "drama": 0,
        "action": 1,
        "mystery": 2
    }

    VIDEO_TEMPLATE = {
        "id": "",
        "type": "",
        "name": "",
        "length": 0,
        "genre": "",
        "ratings": [],
    }

    EPISODE_TEMPLATE_EXT = {
        "series": "",
        "season": 1,
        "episode_num": 1,
    }

    NUM_SEASONS = (1, 12)
    NUM_EPISODES_PER_SEASON = (5, 30)
    NUM_RATINGS = (0, 251)

    #####################################################
    #####################################################

    #####################################################
    def __init__(self, video_names_file):
        videos_json = {}
        with open(video_names_file, "r") as file:
            videos_json = json.load(file)

        self._video_names = [name for name in videos_json["names"]]
        self._global_id_num = 1

    # TODO: implement generate_file_content
    #####################################################
    def generate_file_content(num_movies, num_series):
        videos = []
        for t, num in videos_dict.itesm():
            if t == "movie"
            for _ in range(num):
                videos.append(generate_video(video_type, video_args))

            elif vt == "episode":
                for i in range(num):
                    num_ssns = randrange(*NUM_SEAONS)
                    num_ssns_eps = randrange(*NUM_EPISODES_PER_SEASON)

    #####################################################
    def generate_video(self, video_type, name=choice(VIDEO_NAMES), genre=choice(GENRE), extra_args):
        if video_type not in VIDEO_TYPE:
            raise ValueError(
                "Video type \"{}\" does not exist.".format(video_type))
        if genre not in GENRE:
            raise ValueError("Genre \"{}\" does not exist".format(genre))

        new_video = VIDEO_TEMPLATE.copy()
        new_video["type"] = video_type
        new_video["name"] = name
        new_video["duration"] = randrange(*LENGTH[video_type])
        new_video["ratings"] = [rating for rating in randrange(*NUM_RATINGS)]
        new_video["duration"] = randrange(*LENGTH[video_type])

        for key, val in extra_args.items():
            new_video[key] = val

        new_video["id"] = _generate_id(new_video)

        return new_video

    #####################################################
    def _generate_id(self, video)
    vt = video["type"]
    id_args = {
        "global_entry_num": self._global_id_num,
        "genre" = GENRE[video["genre"]]
    }

    if (vt == "episode"){
        id_args["episode_num"] = video["episode_num"]
        id_args["season_num"] = video["season"]
    }

    id = VIDEO_TYPE[vt]["id_base"].format(**id_args)
    self._global_id_num += 1
    return id


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", required=True,
                        help="output filename")
    args = vars(ap.parse_args())

    with open(args["filename"], "w") as file:
        file.write(generare_file_content())
