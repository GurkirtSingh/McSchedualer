import base64
import gmailAPI
import calendarAPI
import re
import datetime
## file - main.py
## description - This is startup file for mcscheduler. which will
## start all the other services.

# regex to extract shift detail from schedule
shiftRe = re.compile(r'([a-zA-Z]{1,9}), ([A-Za-z]+) (\d{1,2}), (\d{4}) (\d{1,2}:\d{2} [AP]M) - (\d{1,2}:\d{2} [AP]M)')

def parseShiftsFromMessage(message: str):
    shifts = []
    sliceStart = message.find('Here is your schedule for the week of')
    sliceEnd = message.find('You have a total of')
    for line in message[sliceStart:sliceEnd].splitlines():
        shift = shiftRe.search(line)
        if shift:
            # create utc format date and time
            startDate = datetime.datetime.strptime(shift.group(1)+ ' ' +
                shift.group(2) + ' ' +
                shift.group(3) + ' ' +
                shift.group(4) + ' ' +
                shift.group(5),
                '%A %B %d %Y %I:%M %p')
            endDate = datetime.datetime.strptime(shift.group(1)+ ' ' +
                shift.group(2) + ' ' +
                shift.group(3) + ' ' +
                shift.group(4) + ' ' +
                shift.group(6),
                '%A %B %d %Y %I:%M %p')
            shifts.append({
                'startDate' : startDate.isoformat(),
                'endDate' : endDate.isoformat()
            })
    return shifts

def decodeMessage():
    base64_message = gmailAPI.gmailAccess()

    # decoding message from base64 to ascii
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.urlsafe_b64decode(base64_bytes)
    return message_bytes.decode('ascii', errors='ignore')

## step 1 - Login to Gmail
## step 2 - store the crediantial for future use
## step 3 - Read the latest email sent by mcd13687@ext.mcdonalds.com ( is uniqe by the restorent)
## step 4 - confirm the Subjact of email is 'Your next week's schedule'
## step 5 - parse the events (shifts) with date, time and position
shifts = parseShiftsFromMessage(decodeMessage())
## step 6 - Access the calender with same email
for s in shifts:
    print(s)
    calendarAPI.CreateEvent("Mcdonald's",s['startDate'], s['endDate'])
## step 7 - creaet new events in the calender from the parsed events
## Success

## Subscribe to the gmail's new eamil event for seamless performance