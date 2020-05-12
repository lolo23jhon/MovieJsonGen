import json
import argparse
from random import choice, randrange, uniform


class VideoGenerator:
    #####################################################
    #####################################################

    VIDEO_TYPE = {
        "movie": {
            "id_base": "G{genre}M{global_entry_num}"
        },
        "episode": {
            "id_base": "G{genre}E{episode_num}S{season_num}S{global_entry_num}"
        }
    }

    LENGTH = {
        "movie": (5400, 9000),
        "episode": (10, 3600)
    }

    GENRE = {
        "drama": 1,
        "action": 2,
        "mystery": 3
    }

    GENRE_KEYS = list(GENRE.keys())

    VIDEO_TEMPLATE = {
        "id": "",
        "type": "",
        "name": "",
        "duration": 0,
        "genre": "",
        "ratings": [],
    }

    EPISODE_TEMPLATE_EXT = {
        "series": "",
        "season": 1,
        "episode_num": 1,
    }

    NUM_SEASONS_PER_SERIES = (1, 6)
    NUM_EPISODES_PER_SEASON = (5, 25)
    NUM_RATINGS = (0, 251)
    RATING_SCALE = (0, 5)

    #####################################################
    #####################################################

    #####################################################
    def __init__(self, video_names_file):
        videos_json = {}
        with open(video_names_file, "r") as file:
            videos_json = json.load(file)

        self._video_names = [name for name in videos_json["video_names"]]
        self._series_names = [name for name in videos_json["series_names"]]
        self._global_id_num = 1

    #####################################################
    def _random_video_name(self):
        if not self._video_names:
            raise RuntimeError("Names have not been loaded.")
        return choice(self._video_names)

    #####################################################
    def _random_series_name(self):
        if not self._series_names:
            raise RuntimeError("Names have not been loaded.")
        return choice(self._series_names)

    #####################################################
    @staticmethod
    def _random_genre():
        return choice(VideoGenerator.GENRE_KEYS)

    #####################################################
    def _generate_id(self, video):
        vt = video["type"]
        id_args = {
            "global_entry_num": self._global_id_num,
            "genre": VideoGenerator.GENRE[video["genre"]]
        }

        if vt == "episode":
            id_args["episode_num"] = video["episode_num"]
            id_args["season_num"] = video["season"]

        id = VideoGenerator.VIDEO_TYPE[vt]["id_base"].format(**id_args)
        self._global_id_num += 1
        return id

    #####################################################
    def generate_video(self, video_type, extra_args=None):
        if video_type not in VideoGenerator.VIDEO_TYPE:
            raise ValueError(
                "Video type \"{}\" does not exist.".format(video_type))

        new_video = VideoGenerator.VIDEO_TEMPLATE.copy()
        new_video["type"] = video_type
        new_video["name"] = self._random_video_name()
        new_video["genre"] = VideoGenerator._random_genre()
        new_video["duration"] = randrange(*VideoGenerator.LENGTH[video_type])
        new_video["ratings"] = []
        for _ in range(randrange(*VideoGenerator.NUM_RATINGS)):
            new_video["ratings"].append(
                round(uniform(*VideoGenerator.RATING_SCALE), 1))

        if extra_args:
            for key, val in extra_args.items():
                new_video[key] = val

        new_video["id"] = self._generate_id(new_video)

        return new_video

    #####################################################
    def generate_video_list(self, num_movies, num_series):
        videos = []
        for _ in range(num_movies):
            videos.append(self.generate_video("movie"))

        for _ in range(num_series):
            num_ssns = randrange(*VideoGenerator.NUM_SEASONS_PER_SERIES)
            num_ssns_eps = randrange(*VideoGenerator.NUM_EPISODES_PER_SEASON)

            video_args = VideoGenerator.EPISODE_TEMPLATE_EXT.copy()
            video_args["series"] = self._random_series_name()

            for ssn_num in range(num_ssns):
                video_args["season_num"] = ssn_num
                for ssn_ep_num in range(num_ssns_eps):
                    video_args["episode_num"] = ssn_ep_num
                    videos.append(self.generate_video(
                        video_type="episode", extra_args=video_args))
        return videos

    def write_file(self, num_movies, num_series, filename="videos.json"):
        videos = self.generate_video_list(num_movies, num_series)
        videos_dict = {}
        for i, video in enumerate(videos):
            videos_dict[i+1] = video

        with open(filename, "w") as file:
            json.dump(videos_dict, file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--filename", required=True,
                        help="output filename")
    parser.add_argument("-i", "--input", required=True,
                        help="video names input")
    parser.add_argument("-m", "--movies", required=True,
                        help="number of movies", type=int)
    parser.add_argument("-s", "--series", required=True,
                        help="number of series", type=int)

    args = vars(parser.parse_args())

    generator = VideoGenerator(args["input"])
    generator.write_file(
        filename=args["filename"], num_movies=args["movies"], num_series=args["series"])
    print("Wrote file {}.".format(args["filename"]))
