import string
import binascii
import base64
import datetime

def validateAndFormatTimeFormat(timestamp):
    
    '''
    inputDate = '-'.join(timestamp[0].split("-")[::-1])
    inputTime = '-'.join(timestamp[1].split("-")[::-1])
    print(inputDate)
    print(inputTime)
    print(timestamp)
    '''
    try:
        dateob = datetime.datetime.strptime(timestamp, '%d-%m-%Y:%S-%M-%H')

    except ValueError:
        print("Incorrect data format, should be YYYY-MM-DD:SS-MM-HH")
        return 0
    print("datob:",dateob)
    return dateob

#Function for checking if the given image string is in base64 format
def validateImageFormat(imageString):
    try:
        #print(imageString.encode('ascii'))
        imageB64 = base64.decodestring(imageString.encode('ascii'))
        #print(imageB64)
        return 1
    except binascii.Error:
        return 0

'''
#Function for checking if the upload act arguments are valid or not
def validateActInputFormat(josn_data):
    try:
        json_data["actId"]
    except:
        return 0
'''

def validatePassword(password):
    return all(c in string.hexdigits for c in password) and (len(password)==40)