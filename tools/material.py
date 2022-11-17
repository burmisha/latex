import library
# from library.logging import cm, color
import tools.download
import attr
import yaml
import collections
from typing import List

import logging
log = logging.getLogger(__name__)

def serialize_list_of_dicts(items: List[dict]) -> str:
    serialized = yaml.dump(
        items,
        encoding='utf-8',
        allow_unicode=True,
        width=1000,
        sort_keys=False,
    ).decode()

    replacements = [('\n- ', '\n\n- ')]
    keys = set(key for item in items for key in item.keys())
    max_len = max(len(key) for key in keys)
    for key in keys:
        replacements.append((f' {key}: ', f' {key}:  ' + ' ' * (max_len - len(key))))

    for replace_what, replace_with in replacements:
        serialized = serialized.replace(replace_what, replace_with)

    return serialized


def run(args):
    download_cfg = library.files.load_yaml_data('download.yaml')
    videos = tools.download.get_pavel_viktor_videos(download_cfg['PavelVictor'])

    materials = [
        library.material.material.Material(
            title=video.title,
            url=video.url,
            source_format=library.material.material.SourceFormat.Video.value,
            extra_title=video.extra_title,
        )
        for video in videos
    ]

    if args.save:
        data = [attr.asdict(material) for material in materials]
        serialized = serialize_list_of_dicts(data)
        with open(library.location.root('data', 'materials_raw.yaml'), 'w') as f:
            f.write(serialized)

    # topic_detector = library.topic.TopicDetector()
    # topic_filter =  library.topic.TopicFilter(args.filter)

    # video_with_topics = []
    # for video in videos:
    #     topic_index = topic_detector.get_topic_index(video.title)
    #     video_with_topics.append((video, topic_index))

    # if args.sort:
    #     video_with_topics = [(v, t) for v, t in video_with_topics if t]
    #     video_with_topics.sort(key=lambda video_with_topic: video_with_topic[1])

    # if save_files:
    #     download_videos(
    #         videos=videos,
    #         threads=args.threads,
    #         retries=args.retries,
    #     )
    # else:
    #     for video, topic_index in video_with_topics:
    #         if topic_filter.matches(topic_index):
    #             log.info(f'{video}, {topic_index}')


def populate_parser(parser):
    parser.add_argument('-s', '--save', help='Save yaml', action='store_true')
    parser.set_defaults(func=run)
