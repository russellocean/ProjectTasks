from setuptools import find_packages, setup

setup(
    name='ProjectTasks',
    version='0.1',
    description='A Trac plugin to dynamically display tasks for each project',
    author='Russell Welch',
    author_email='russellwelch17@gmail.com',
    url='',
    packages=find_packages(exclude=['*.tests*']),
    entry_points={
        'trac.plugins': [
            'project_tasks = project_tasks.project_tasks:ProjectTasksMacro'
        ]
    },
)
