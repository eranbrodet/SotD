#!/usr/bin/python
import re

import httplib2
from apiclient import discovery

from ui import SotdUI

spreadsheetId = '1syiniMiJF_XOzRxyyVh_yXQPSzOpViIi7nHliPdXfG0'
developerKey = 'AIzaSyA3Gwwe69dEALQuRBzcsKCT7C6LzeRB2Ns'
hyperlink_regex = re.compile(r'=HYPERLINK\("(.*?)","(.*?)"\)')


def get_senders_options(service):
    range_name = 'Calculations!I2:I'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=range_name).execute()
    return [x[0] for x in result.get('values', [])]


def get_data(service):
    range_name = 'Data!B:C'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=range_name, valueRenderOption='FORMULA').execute()
    ret = []
    for value in result.get('values', [])[1:]:
        parsed = hyperlink_regex.match(value[0])
        if not parsed:
            continue
        ret.append((parsed.group(1), parsed.group(2), value[1]))
    return ret


def main():
    discovery_url = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
    service = discovery.build('sheets', 'v4', http=httplib2.Http(),
                              discoveryServiceUrl=discovery_url, developerKey=developerKey)
    sender_options = get_senders_options(service)
    all_data = get_data(service)
    SotdUI(sender_options, all_data)


if __name__ == '__main__':
    main()
