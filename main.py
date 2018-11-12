def central():

    from googleapiclient.discovery import build
    from httplib2 import Http
    from oauth2client import file, client, tools

    import os
    from inspect import getsourcefile
    from os.path import abspath
    import smtplib
    from votecount import calculateVC
    import time
    import datetime

    from datetime import datetime
    from pytz import timezone
    import pytz

    SPREADSHEET_ID = "1VXNu_zrOsuoRPmF72ldW_A17xlu3r3XyFaRsLd_O8HY"

    #Find the curent file location/chdir to current location
    directory = abspath(getsourcefile(lambda:0))
    newDirectory = directory[:(directory.rfind("\\")+1)]
    os.chdir(newDirectory)


    # If modifying these scopes, delete the file token.json.
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

    # The ID and range of a sample spreadsheet.

    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API

    RANGE_NAME = 'Sheet1!I2:L'

    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Page 1, Page 2:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[1]))
            x = row[0]
            y = row[1]
            line = int(row[2])
            gameDay = int(row[3])

    returned = (calculateVC(x,y))

    text = returned[0]
    text2 = returned[1]

    print("Return 1: " + text + "Return 2: " + text2)

    date_format='%m/%d/%Y %H:%M:%S %Z'
    date = datetime.now(tz=pytz.utc)
    date = date.astimezone(timezone('US/Eastern'))
    date  = (date.strftime(date_format))
    RANGE_NAME2 = 'Sheet1!A' + str(line)
    RANGE_NAME3 = 'Sheet1!K2'


    values = [
        [
            date , "", x , y , text , text2 , gameDay
        ],
        # Additional rows ...
    ]
    body = {
        'values': values
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME2,
        valueInputOption="RAW", body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')));




    #---------------------------------
    #Update Line Number


    values = [
        [
            (line+1)
        ],
        # Additional rows ...
    ]
    body = {
        'values': values
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME3,
        valueInputOption="RAW", body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')));
    return
