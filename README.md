# Youtube Comment Detector
## _Youtube comment detector for [this event video](https://youtu.be/_gKmYOLKQBg)_

Youtube Comment Detector detects if there are comments that have been registered for a certain period of time without additional comments.

## Features

- Fetches recent comments of video
- Check if there's 1 minute or more gap between adjacent two comments
- Report the result to configured email address

## Tech

Youtube Comment Detector uses a number of open source projects to work properly:

- [Google API](https://github.com/googleapis/google-api-python-client) - Google API module for python
- [Google Auth](https://github.com/googleapis/google-auth-library-python) - Google Oauth2 module for python

## Installation

Youtube Comment Alarm requires Python 3.9.12 and Ubuntu 20.04 LTS is recommended.
All python venv requirements are in the file `requirements`

For development environments
```sh
make venv
```

To install service
```sh
make service
```

## Contribution

Feel free to contribute!

## License

GPL
