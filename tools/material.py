import library.location
import library.material
import library.files
import library.normalize
import library.topic
import tools.download
import attr
import yaml
import collections
from typing import List
from tqdm import tqdm

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


class MaterialHandler:
    def __init__(self):
        self.raw_file = library.location.root('data', 'materials_raw.yaml')
        self.ready_file = library.location.root('data', 'materials_ready.yaml')

    def save(self):
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
        data = [{k: v for k, v in attr.asdict(material).items() if v} for material in materials]
        serialized = serialize_list_of_dicts(data)
        with open(self.raw_file, 'w') as f:
            f.write(serialized)

    def prepare(self):
        canonizer = library.normalize.TitleCanonizer()
        topic_detector = library.topic.TopicDetector()

        rows = library.files.load_yaml_data('materials_raw.yaml')
        materials = [library.material.material.Material(**row) for row in rows]

        for material in tqdm(materials):
            material.canonized_title = canonizer.Canonize(material.title)
            for search_key in [
                f'{material.canonized_title}',
                f'{material.canonized_title} {material.extra_title}',
            ]:
                topic = topic_detector.get_topic_index(search_key, grade=material.grade)
                if topic:
                    material.topic = f'{topic.index} - {topic.ChapterTitle} - {topic.PartTitle}'
                    break

        data = [{k: v for k, v in attr.asdict(material).items() if v} for material in materials]
        serialized = serialize_list_of_dicts(data)
        with open(self.ready_file, 'w') as f:
            f.write(serialized)


def run(args):
    material_handler = MaterialHandler()
    if args.save:
        material_handler.save()
    if args.prepare:
        material_handler.prepare()


def populate_parser(parser):
    parser.add_argument('-s', '--save', help='Save yaml', action='store_true')
    parser.add_argument('-p', '--prepare', help='Prepare material', action='store_true')
    parser.set_defaults(func=run)
