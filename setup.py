from setuptools import setup, find_packages

setup(
    name="dust-lang",
    version="0.1.0",
    packages=find_packages(),
    description="A simple language interpreter written in Python.",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    author='Warith Ogunwoolu',
    author_email='ogunwooluolasunmbo@gmail.com',
    url='https://github.com/Bluewraith04/dust',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts':[
            'dust = dust.main:main'
        ],
        'gui_scripts': [],
    },
    python_requires='>=3.7',
)