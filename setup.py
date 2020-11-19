import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MAPS_test",
    version="0.0.21",
    author="Noah Alex",
    author_email="noah.alex@sorensonimpact.com",
    description="A data scraper for the MAPS Project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sorenson-impact/MAPS",
    # packages=setuptools.find_packages(),
    packages = ['scraper'],
    package_dir = {'scraper':'src/scraper'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.1',
    # include_package_data=True,
    install_requires=['parsel' , 'pygsheets', 'bs4' , 'pandas' , 'plotly' , 'numpy', 'oauth2client', 'gspread', 'backports.datetime_fromisoformat'],

    package_data={  # Optional
        'scraper': ['testdata/smallset/*', 'testdata/tinyset/*', 
                'testdata/mediumset/*','testdata/fullset/*', 
                'config/drive_creds.json', 'config/credentials.json',
                'config/credentials','config/numthreads', 'pickles/ALL_SEARCHES.pkl', 
                'pickles/TIMEDOUT_SEARCHES.pkl', 'pickles/FAILED_QUERIES.pkl', 'pickles/PDF_URLS.pkl']
            }
    #package_data={'capitalize': ['data/cap_data.txt']},
)