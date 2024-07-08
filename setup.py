from setuptools import find_packages, setup

setup(
    name='todo',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'rich',
        # Add any other dependencies here
    ],
    entry_points={
        'console_scripts': [
            'todo=todo.app:cli',
        ],
    },
    author='Muhammad Abrar',
    author_email='legendabrar44@gmail.com',
    description='A simple CLI task management tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/abrarishere/todoCliPython',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
