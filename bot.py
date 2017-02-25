import time
import vk
import pafy
import re

access_token = 'VK_TOKEN'

session = vk.Session(access_token=access_token)
vkapi = vk.API(session, v='5.62', lang='ru')


def youtube_url_validation(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    youtube_regex_match = re.match(youtube_regex, url)
    if youtube_regex_match:
        return youtube_regex_match.group(6)

    return youtube_regex_match


def sent_toytube_links(url):
    video = pafy.new(url)
    streams = video.streams
    for s in streams:
        text = '{} {} {} {}'.format(s.resolution, s.extension, s.get_filesize(), s.url)
        vkapi.messages.send(user_id=user_id, message=text)


messages = vkapi.messages.get(count=1)
last = messages['items'][0]['id']

while True:
    try:
        messages = vkapi.messages.get(last_message_id=last, timeout=5)
    except Exception as e:
        print(e)
        time.sleep(1)
        continue
    if not messages['items']:
        time.sleep(1)
        continue
    last = messages['items'][0]['id']
    for message in messages['items']:
        link = message['body']
        user_id = message['user_id']
        m = youtube_url_validation(link)
        if m:
            sent_toytube_links(link)
        else:
            vkapi.messages.send(user_id=user_id, message='please send me link to YouTube video')

    time.sleep(1)
