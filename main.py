import json, asyncio, requests
from datetime import datetime, timedelta, timezone
from src.EmailAPI import report
from src.YoutubeAPI import FetchNewComments
from src.logger import logger

comments = []

async def main():
    global config
    with open('config.json', 'r') as fp:
        config = json.load(fp)
    while True:
        await asyncio.gather(checker(), asyncio.sleep(15))

async def checker():
    global config, comments
    NewComments = FetchNewComments(config['VideoId'])
    await MergeComments(NewComments)
    result = await FindJackpot()
    if result:
        logger.info('Sending report...')
        await report(result)
        logger.info('Flushing cache...')
        comments = []
    await PurgeOldComments()

async def MergeComments(NewComments):
    global comments
    logger.info('Merging new comments to cache...')
    if not comments:
        logger.info('No comments were in cache.')
        logger.info(f'{len(NewComments)} new comments are fetched to cache.')
        comments = list(NewComments)
        return
    while NewComments:
        if comments[-1]['id'] == NewComments[0]['id']:
            NewComments = NewComments[1:]
            break;
        if comments[-1]['publishedAt'] < NewComments[0]['publishedAt']: break
        NewComments = NewComments[1:]
    comments = NewComments + comments
    logger.info(f'{len(NewComments)} new comments are pushed to cache.')

async def FindJackpot():
    global config, comments
    logger.info('Finding jackpot comment from cache...')
    for i in range(len(comments) - 2, 0, -1):
        gap = comments[i]['publishedAt'] - comments[i + 1]['publishedAt']
        if gap > config['interval']:
            logger.info('Jackpot!!')
            return comments[i]
    logger.info('No jackpot found.')

async def PurgeOldComments():
    global config, comments
    if len(comments) <= config['CACHE_SIZE']: return
    logger.info(f'The {len(comments) - config["CACHE_SIZE"]} oldest comments are purged from cache.')
    comments = comments[:config['CACHE_SIZE']]

if __name__ == '__main__': asyncio.run(main())
