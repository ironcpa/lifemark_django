import os
import time
import urllib
from main.models import Lifemark
from datetime import datetime
# import run_scrappers
from slackclient import SlackClient


working_dir = os.environ.get('WORKING_DIR', '')
if len(working_dir) > 0:
    os.chdir(working_dir)

slack_client = SlackClient(os.environ.get('SLACK_TOKEN'))


def create_dued_lifemarks(curr_datehour, is_daily=False):
    if is_daily:
        dued_lifemarks = Lifemark.objects.get_dued_lifemarks(curr_datehour)
    else:
        dued_lifemarks = Lifemark.objects.get_hourly_dued_lifemarks(curr_datehour)

    if dued_lifemarks:
        message = ''
        for lm in dued_lifemarks:
            message += '{}:{}({}) is dued!\r\n'.format(lm.id,
                                                       lm.title,
                                                       lm.state)

        # if is_daily:
        params = {'target_fields': 'key',
                  'keyword': ' '.join([str(lm.id) for lm in dued_lifemarks])}
        link = 'lifemarks?{}'.format(urllib.parse.urlencode(params, quote_via=urllib.parse.quote))
        created_lifemark = Lifemark.objects.create(
            title='items due tomorrow',
            category='noti',
            link=link,
            desc=message
        )

        return created_lifemark


def get_noti_channel(channel_name):
    channels = slack_client.api_call('channels.list')
    if channels['ok']:
        return next(e['id'] for e in channels['channels'] if e['name'] == channel_name)
    return None


def send_slack_noti(message):
    channel_id = get_noti_channel('noti')
    if not channel_id:
        return

    slack_client.api_call('chat.postMessage', channel=channel_id,
                          text='\n' + message, username='lifemark',
                          icon_emoji=':robot_face:')


def do_hourly_job():
    curr_datehour = datetime.now().strftime('%Y-%m-%d %H')
    is_daily = int(str(curr_datehour)[11:13]) == 0
    created = create_dued_lifemarks(curr_datehour, is_daily)

    if created:
        send_slack_noti(created.desc)

    print('>>>>>>>>> time by ironcpa >>>>>>>>>>')
    print(time.ctime())

    # todo: run scrappers
    # run_scrappers.main()
