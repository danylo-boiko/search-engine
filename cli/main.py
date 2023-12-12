from argparse import ArgumentParser
from asyncio import get_event_loop
from os.path import join, dirname
from sys import path


path.append(join(dirname(__file__), ".."))
path.append(dirname(__file__))


if __name__ == "__main__":
    from cli.core import settings
    from crawler import Crawler
    from crawler.utils import extract_domain

    parser = ArgumentParser(prog=settings.PROJECT_TITLE)

    parser.add_argument("-u", "--url", type=str, help="Url of the website to crawl")
    parser.add_argument("-q", "--queue", type=str, help="Crawler queue prefix (full website domain)")
    parser.add_argument("-t", "--threads", type=int, default=settings.DEFAULT_THREADS_COUNT, help="Count of parallel threads")

    args = parser.parse_args()

    if args.url and not extract_domain(args.url):
        raise ValueError("Url is invalid")

    if not args.url and not args.queue:
        raise ValueError("Url or queue prefix must be provided")

    if args.url and args.queue and extract_domain(args.url) != args.queue:
        raise ValueError("Url domain and queue prefix do not match")

    crawler = Crawler(args.url, args.queue, args.threads)
    event_loop = get_event_loop()

    try:
        crawler.start()
        event_loop.run_forever()
    except KeyboardInterrupt:
        crawler.stop()
    finally:
        event_loop.close()
