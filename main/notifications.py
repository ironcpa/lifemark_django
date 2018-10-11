import urllib
from main.models import Lifemark


def create_dued_lifemarks(curr_datehour, is_daily=False):
    if is_daily:
        dued_lifemarks = Lifemark.objects.get_dued_lifemarks(curr_datehour)
    else:
        dued_lifemarks = Lifemark.objects.get_hourly_dued_lifemarks(curr_datehour)

    if dued_lifemarks:
        print('dued items : ', len(dued_lifemarks))
        print(dued_lifemarks)

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

        print('message sent', message)

        return created_lifemark
