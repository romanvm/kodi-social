import time
from argparse import ArgumentParser
from pathlib import Path

from dotenv import load_dotenv

from kodi_social.database import create_database, insert_posts, post_exists
from kodi_social.email import notify as notify_by_email
from kodi_social.logging import get_logger
from kodi_social.rss import get_posts

THIS_DIR = Path(__file__).resolve().parent
ENV_FILE = THIS_DIR / '.env'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

LOGGER = get_logger()

PROCESSORS = {
    'email': notify_by_email,
}


def get_arguments():
    parser = ArgumentParser(
        prog='Kodi-social',
        description='Post news from kodi.tv to various social media'
    )
    parser.add_argument('-s', '--seed', action='store_true',
                        help='Populate the DB with existing articles')
    parser.add_argument('-u', '--update', action='store_true',
                        help='Scan RSS feed and post new articles if any')
    arguments = parser.parse_args()
    return arguments


def populate_database():
    print('Populating the database...')
    create_database()
    posts = get_posts()
    print(f'Adding {len(posts)} posts...')
    rows = [(p['id'], p['title'], time.strftime(TIME_FORMAT, p['published_parsed'])) for p in posts]
    insert_posts(rows)
    print('Done.')


def execute_processors(title: str, link: str):
    for name, process_func in PROCESSORS.items():
        LOGGER.debug('Executing %s processor', name)
        try:
            process_func(title, link)
        except Exception:
            LOGGER.exception('Error when executing %s processor', name)
            return False
    return True


def process_posts():
    posts = get_posts()
    for post in posts:
        if not post_exists(post['id']):
            is_success = execute_processors(post['title'], post['link'])
            if is_success:
                db_row = (post['id'], post['title'], time.strftime(TIME_FORMAT, post['published_parsed']))
                insert_posts([db_row])


def main():
    load_dotenv(ENV_FILE)
    args = get_arguments()
    if args.seed:
        populate_database()
        return
    if args.update:
        process_posts()


if __name__ == '__main__':
    main()
