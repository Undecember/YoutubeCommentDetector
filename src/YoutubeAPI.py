import os, sys, json, asyncio, pickle, time, signal
from src.logger import logger
from datetime import datetime, timezone

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
config = None
TokenAge = None

def GenYoutube():
    global config, TokenAge
    if not config:
        with open('config.json', 'r') as fp:
            logger.info('Loading config...')
            config = json.load(fp)

    credentials = None
    try:
        with open('token.pickle', 'rb') as fp:
            logger.info('Loading credentials from file...')
            credentials = pickle.load(fp)
    except: pass

    isInvalid = lambda: credentials is None or not credentials.valid
    isExpired = lambda: TokenAge is None or TokenAge + config['TOKEN_LIFE'] < time.time()
    if isInvalid(): logger.info('No valid credentials file.')
    if isExpired(): logger.info('Credentials expired.')

    if isInvalid() or isExpired():
        try:
            logger.info('Refreshing access token...')
            credentials.refresh(Request())
            TokenAge = time.time()
        except: pass
    if isInvalid():
        logger.error('Refresh token expired.')

    logger.info('Building youtube api client...')
    youtube = build('youtube', 'v3', credentials = credentials)
    return youtube

def ReAuth(signum, frame):
    logger.info('Fetching new tokens...')
    flow = InstalledAppFlow.from_client_secrets_file(
        config['CLIENT_SECRET_FILE'], config['API_SCOPES'],
        redirect_uri = 'urn:ietf:wg:oauth:2.0:oob')
    auth_url, _ = flow.authorization_url()
    print('Auth URL :', auth_url)
    while not os.path.isfile('AuthCode.txt'): continue
    with open('AuthCode.txt', 'r') as fp: code = fp.read()
    os.remove('AuthCode.txt')
    flow.fetch_token(code = code)
    credentials = flow.credentials
    with open('token.pickle', 'wb') as fp:
        logger.info('Saving credentials...')
        pickle.dump(credentials, fp)
signal.signal(signal.SIGUSR1, ReAuth)

def FetchNewComments(VideoId):
    youtube = GenYoutube()
    request = youtube.commentThreads().list(
        part = 'snippet',
        maxResults = 100,
        order = 'time',
        videoId = VideoId
    )
    logger.info('Sending commentThreads.list request...')
    response = request.execute()
    logger.info('Fetching comments data from response except pinned one...')
    comments = response['items'][1:]
    for i in range(len(comments)):
        snippet = comments[i]['snippet']['topLevelComment']['snippet']
        comments[i] = { 'id': comments[i]['snippet']['topLevelComment']['id'] }
        comments[i].update(snippet)
        comments[i]['publishedAt'] = int(datetime \
            .strptime(comments[i]['publishedAt'], '%Y-%m-%dT%H:%M:%SZ') \
            .replace(tzinfo = timezone.utc) \
            .timestamp())
    return comments

if __name__ == '__main__':
    with open('config.json', 'r') as fp:
        logger.info('Loading config...')
        config = json.load(fp)
    comments = FetchNewComments(config['VIDEO_ID'])
    print(comments[0])
