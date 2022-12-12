import streamlit as st
from library import logging

from library.topic import TopicDetector

topic_detector = TopicDetector()

available_grades = [f'{grade} класс' for grade in topic_detector.get_grades]

with st.sidebar:
    grades_str = st.multiselect(
         'Класс',
         available_grades,
         available_grades[len(available_grades) // 2:],
    )
    grades_int = [int(grade.split(' ', 1)[0]) for grade in grades_str]

    available_parts = list(topic_detector.get_parts(grades_int))
    parts = st.multiselect(
         'Темы',
         available_parts,
         [],
    )

    material_types = st.multiselect(
         'Тип материала',
         ['Youtube', 'Статьи', 'Задачи', 'Конспекты'],
         ['Youtube', 'Статьи', 'Задачи', 'Конспекты'],
    )

st.write('You selected:', grades_int)
st.write('You selected:', parts)
st.write('You selected:', material_types)


x = st.slider('Select a value')
st.write(x, 'squared is', x * x)
