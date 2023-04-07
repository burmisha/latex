import streamlit as st
from library import logging

from library.topic import TopicDetector

topic_detector = TopicDetector()


with st.sidebar:
    grade_tag_by_desc = {tag.description: tag for tag in topic_detector.grade_tags}
    grade_tag_descs = list(grade_tag_by_desc.keys())
    grade_descs = st.multiselect(
        'Класс',
        grade_tag_descs,
        grade_tag_descs[len(grade_tag_descs) // 2:],
    )
    grade_tags = [grade_tag_by_desc[grade_desc] for grade_desc in grade_descs]

    second_tags_by_desc = {tag.description: tag for tag in topic_detector.get_second_tags(grade_tags)}
    second_tags_descs = list(second_tags_by_desc.keys())
    second_descs = st.multiselect(
         'Разделы',
         second_tags_descs,
         second_tags_descs,
    )
    second_tags = [second_tags_by_desc[second_desc] for second_desc in second_descs]

    third_tags_by_desc = {tag.description: tag for tag in topic_detector.get_third_tags(grade_tags, second_tags)}
    third_tags_descs = list(third_tags_by_desc.keys())
    third_descs = st.multiselect(
         'Темы',
         third_tags_descs,
         third_tags_descs[:10],
    )
    third_tags = [third_tags_by_desc[third_desc] for third_desc in third_descs]

    # parts = st.multiselect(
    #      'Темы',
    #      [tt.description for tt in tagged_topics],
    #      [],
    # )

    material_types = st.multiselect(
         'Тип материала',
         ['Youtube', 'Статьи', 'Задачи', 'Конспекты'],
         ['Youtube', 'Статьи', 'Задачи', 'Конспекты'],
    )

# st.write('You selected:', material_types)


x = st.slider('Select a value')
st.write(x, 'squared is', x * x)
