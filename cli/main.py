from argparse import ArgumentParser
from os.path import join, dirname
from sys import path


path.append(join(dirname(__file__), ".."))
path.append(dirname(__file__))


if __name__ == "__main__":
    from cli.core import settings

    parser = ArgumentParser(prog=settings.PROJECT_TITLE)

    parser.add_argument("-u", "--url", type=str, default=settings.DEFAULT_CRAWLER_URL, help="Url of the website to crawl")
    parser.add_argument("-t", "--threads", type=int, default=settings.DEFAULT_THREADS_COUNT, help="Count of the crawler's parallel threads")

    args = parser.parse_args()
