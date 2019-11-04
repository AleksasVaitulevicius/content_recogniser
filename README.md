# Content recogniser web service

This api extracts information from data.

## Startup instructions

1. Clone project `git clone https://github.com/AleksasVaitulevicius/content_recogniser.git`
2. Install Python >3.6 <https://www.python.org/downloads/>
3. Run `pip install -r requirements`
4. Run `python -m pip install git+https://github.com/acrcloud/acrcloud_sdk_python`
5. Fill credentials for cloud services in file `config.py`
6. Run `python manage.py runserver`
7. Access web via <http://127.0.0.1:8000/>

## Use instructions and documentation

To login use  HTTP, method: __POST__, path: __/login__, body: 
``
{
    "username": "<your-user-name>",
    "password": "<your-password>"
}
``
Api returns cookies for authorization. __Note__: You are also required to set header `X-CSRFToken` with value from 
cookie: `csrftoken`

To get result use HTTP, method: __PUT__, path: __/__, body: __form-data__.
Api returns result as JSON object with keys taken from submitted form keys and
corresponding values as content descriptions.

## Supported forms of data

* Images of most popular formats
* Sound recordings of most popular formats
* Text files
* Plain text

## Cloud services used for recognizing content of data


* In images:[Imagga](https://imagga.com/). Used Imagga's services:
    + tags - determines image content
    + text - detects alphanumeric symbols in images
    + colors - determins what kind of colours are in image
* For sound recordings:
    + [AcrCloud](https://www.acrcloud.com/music-recognition/) for music recognition
    + [IBM Watson](https://www.ibm.com/cloud/watson-speech-to-text) for speech to text
* For plain texts:
    + [detectlanguage](https://detectlanguage.com/) for language detection
    + [IBM Watson](https://www.ibm.com/watson/services/tone-analyzer/) for tone analysis