from setuptools import setup, find_packages

setup(
    name="smog_usage_stats",
    verion="0.1.0",
    author="stu-gotz (Alan Nardo)",
    author_email="<nardo.alan@outlook.com>",
    description="Python wrapper to access Smogon's Pokemon Showdown usage statistics.",
    install_requires=[
        "beautifulsoup4",
        "blinker",
        "certifi",
        "charset-normalizer",
        "click",
        "colorama",
        "Flask",
        "idna",
        "itsdangerous",
        "Jinja2",
        "MarkupSafe",
        "pathlib",
        "psycopg",
        "psycopg-binary",
        "psycopg2",
        "python-dateutil",
        "python-dotenv",
        "pytz",
        "requests",
        "six",
        "soupsieve",
        "typing_extensions",
        "tzdata",
        "urllib3",
        "Werkzeug",
    ],
    packages=find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ]
)
