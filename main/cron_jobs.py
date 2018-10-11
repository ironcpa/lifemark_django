import os
import time
from datetime import datetime
# import run_scrappers
from slackclient import SlackClient
from main.notifications import create_dued_lifemarks


working_dir = os.environ.get('WORKING_DIR', '')
if len(working_dir) > 0:
    os.chdir(working_dir)

slack_client = SlackClient(os.environ.get('SLACK_TOKEN'))


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

    print('>>>>>>>>> slack noti sent >>>>>>>>>>')


def do_daily():
    curr_datehour = datetime.now().strftime('%Y-%m-%d %H')
    is_daily = int(str(curr_datehour)[11:13]) == 0
    created = create_dued_lifemarks(curr_datehour, is_daily)

    if created:
        send_slack_noti(created.desc)

    print('>>>>>>>>> time by ironcpa >>>>>>>>>>')
    print(time.ctime())

    # todo: run scrappers
    # run_scrappers.main()
