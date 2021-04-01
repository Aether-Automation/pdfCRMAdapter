from flask import Flask, jsonify, request
# import subprocess
import multiprocessing
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


def convertHtmlToPdf(authToken, htmlText, quoteId, filename):
    """ Takes the HTML in tmpspool/quote.html, and writes out tmpspool/quote.pdf"""
    # Save HTML to ..
    # Execute shell
    print("convertHtmlToPdf convertHtmlToPdf convertHtmlToPdf convertHtmlToPdf !!! ")
    print("Authorization header => " + authToken)
    print("Given QuoteID => " + quoteId)
    print("Given filename => " + filename)
    print("Given HTML => " + htmlText)

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
    # print("Authorization header => " + request.headers['Authorization'])
    # print("Given QuoteID => " + request.form["quoteId"])
    # print("Given filename => " + request.form["filename"])
    # print("Given HTML => " + request.form["htmltext"])

    authToken = request.headers['Authorization']
    quoteId = request.form["quoteId"]
    outputFilename = request.form["filename"]
    # Also save the HTML to tmpspool/$filename
    htmlText = request.form["htmltext"]

    thread = multiprocessing.Process(target=convertHtmlToPdf, args=(authToken,htmlText,quoteId,outputFilename))
    thread.start()



if __name__ == '__main__':
    app.run(debug=True)
