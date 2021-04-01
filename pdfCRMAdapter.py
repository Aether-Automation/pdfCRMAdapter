from flask import Flask, jsonify, request
import subprocess
# import multiprocessing
# import dataset
import time
import random

app = Flask(__name__)

"""
Flow:
DONE - -> CRM kicks-off process from 'Generate Quote' button action.
DONE - -> Images, details are spooled.  Images are accessible online, details are used to fill in an HTML page.
DONE - -> Call to endpoint occurs; the posted parameters are 'filename' 'htmltext' 'quoteId'
-> Endpoint forks a separate python method:
    --> This method invokes curl to turn the HTML into a PDF, and then invokes curl to attach in CRM.
* Listens for incoming, and can print parameters.
* Can fork a background task which saves to a specified temp.
* 

"""


def convertHtmlToPdf(htmlText, quoteId, filename):
    """ Takes the HTML in tmpspool/quote.html, and writes out tmpspool/quote.pdf"""
    try:
        retcode = call("mycmd" + " myarg", shell=True)
        if retcode < 0:
            print("Child was terminated by signal", -retcode, file=sys.stderr)
        else:
            print("Child returned", retcode, file=sys.stderr)
    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)
    return True

def attachPdfToCrm(htmlText, quoteId, filename, authtoken):
    """ Renames tmpspool/quote.pdf to the filename, and then attaches it to CRM quote record."""
#    time.sleep(10)  # simulate a long running process
#     try:
#         retcode = call("mycmd" + " myarg", shell=True)
#         if retcode < 0:
#             print("Child was terminated by signal", -retcode, file=sys.stderr)
#         else:
#             print("Child returned", retcode, file=sys.stderr)
#     except OSError as e:
#         print("Execution failed:", e, file=sys.stderr)
    return True


# Headers: Need 'Authorization: Zoho-oauthtoken'
@app.route('/', methods=['POST'])
def index():
    """ Get { HTMLText ... QuoteID ... Filename  - ZAuthToken. }"""
    print("Authorization header => " + request.headers['Authorization'])
    print("Given data => " + request.data)
    # Header and arguments in Flask to base route.
    # thread = multiprocessing.Process(target=update_person, args=(name,))
    # thread.start()



if __name__ == '__main__':
    app.run(debug=True)