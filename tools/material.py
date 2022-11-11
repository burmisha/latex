import library
# from library.logging import cm, color
import tools.download
import attr
import yaml

import logging
log = logging.getLogger(__name__)


def run(args):
    download_cfg = library.files.load_yaml_data('download.yaml')
    videos = tools.download.get_pavel_viktor_videos(download_cfg['PavelVictor'])

    materials = [
        library.material.material.Material(
            source_format=library.material.material.SourceFormat.Video._value,
            raw_title=video.title,
            url=video.url,
        )
        for video in videos
    ]

    if args.save:
        with open(library.location.root('data', 'materials_raw.yaml'), 'w') as f:
            data = [attr.asdict(material) for material in materials]
            print([data[0], type(data[0])])
            yaml.safe_dump(data, f, encoding='utf-8', allow_unicode=True)

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
