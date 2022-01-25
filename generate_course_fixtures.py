import json
import requests
from pathlib import Path

COURSES_URL = 'https://api.devhub.virginia.edu/v1/courses'
# the above URL is our 3rd party API and is also where we got the course list / column titles from. 

DESIRED_TERM_DESCS = [
    '2021 Fall',
] # We will have to add to this list if we want to continue into next semester.


def get_courses() -> list:
    # The next line is from https://www.kite.com/python/answers/how-to-get-a-json-from-a-webpage-in-python 
    course_data = requests.get(COURSES_URL).json()['class_schedules']
    columns, records = course_data['columns'], course_data['records']
    courses = [dict(zip(columns, record)) for record in records]
    return courses




if __name__ == '__main__':
    all_courses = get_courses()
    desired_courses = [course for course in all_courses if course['term_desc'] in DESIRED_TERM_DESCS]
    desired_courses = list(set(desired_courses))

    # How to provide initial data taken from https://docs.djangoproject.com/en/3.2/howto/initial-data/#providing-data-with-fixtures
    course_fixtures = []
    class_titles = []
    for index, course in enumerate(desired_courses):
        class_title = course['class_title']
        if class_title not in class_titles:
            fixture = {
                'model': 'google_oauth_app.course',
                'pk': index,
                'fields': course
            }
            course_fixtures.append(fixture)
            class_titles.append(class_title)

    course_json = json.dumps(course_fixtures)
    # This is the end of what is from the last link

    file = Path('course_fixtures.json')
    file.write_text(course_json)



# The following commands are taken from https://docs.djangoproject.com/en/3.2/ref/django-admin/#loaddata
# They don't actually go in the code, just the terminal / Heroku bash, so I wasn't sure where else to put the citation
# heroku run bash
# python manage.py loaddata course_fixtures.json