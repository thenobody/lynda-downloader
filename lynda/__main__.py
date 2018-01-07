import requests as r
from lxml import html
from clint.textui import progress
import urlparse
import os
from splinter import Browser
import time
from Tkinter import *
from tkFileDialog import *


def get_course_items(course_url, cookies=dict()):
    result = r.get(course_url, cookies=cookies)
    tree = html.fromstring(result.content)
    items = tree.cssselect('.video-name.item-name')

    count = len(items)
    pos = 0
    for element in items:
        pos += 1
        yield (element.get('href'), pos, count)


def get_video_link(url, cookies=dict()):
    result = r.get(url, cookies=cookies)
    tree = html.fromstring(result.content)
    for player in tree.cssselect('video.player'):
        src = player.get('data-src')
        if src:
            yield src


def filename_from_url(url):
    parsed = urlparse.urlparse(url)
    return os.path.basename(parsed.path)


def download_video(url, output_dir, cookies=dict(), item_pos=None, item_count=None):
    total_progress = '({pos}/{count}) '.format(pos=item_pos, count=item_count) if (item_pos and item_count) else ''
    print '{progress}Downloading from {url}'.format(progress=total_progress, url=url)

    result = r.get(url, cookies=cookies, stream=True)
    path = os.path.normpath('/'.join([output_dir, filename_from_url(url)]))
    print 'Output file: {path}'.format(path=path)

    with open(path, 'wb') as f:
        total_length = int(result.headers.get('content-length'))
        for chunk in progress.bar(result.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
            if chunk:
                f.write(chunk)
                f.flush()


def obtain_session_token_and_course_url(url):
    with Browser('chrome') as browser:
        browser.visit(url)

        while browser.is_element_not_present_by_css("span.account-name"):
            print 'Waiting for browser login...'
            time.sleep(1)

        return browser.cookies['token'], browser.url


def obtain_output_directory():
    root = Tk()
    root.withdraw()

    path = askdirectory(initialdir='.', title='Select output directory')
    root.update()
    root.destroy()
    return str(path)


LYNDA_URL = 'https://www.lynda.com/'

OUTPUT_DIR = obtain_output_directory()

(TOKEN, COURSE_URL) = obtain_session_token_and_course_url(LYNDA_URL)
print 'Obtained session token: {token}'.format(token=TOKEN)
print 'Obtained course URL: {course_url}'.format(course_url=COURSE_URL)
print

COOKIES = dict(
    token=TOKEN
)

for (item, pos, total) in get_course_items(COURSE_URL, cookies=COOKIES):
    for video_link in get_video_link(item, cookies=COOKIES):
        download_video(video_link, OUTPUT_DIR, cookies=COOKIES, item_pos=pos, item_count=total)
        print

print 'DONE!'



