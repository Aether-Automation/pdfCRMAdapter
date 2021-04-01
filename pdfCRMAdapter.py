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



def attachPdfToCrm(authToken, htmlText, quoteId, filename):
    url = 'https://www.zohoapis.com/crm/v2/Quotes/" + quoteId + "/Attachments'
    headers = {
        'Authorization': authtoken
    }
    request_body = {
        'file': open(
            '/Users/dylang/Projects/2021-03-31-Nimbis_AA-518/pdfFlaskAdapter/attach_test.pdf',
            'rb')
    }
    response = requests.post(url=url, files=request_body, headers=headers)
    if response is not None:
        print("HTTP Status Code : " + str(response.status_code))
        print(response.json())
    return True


def convertHtmlToPdf(authToken, htmlText, quoteId, filename):
    # Save HTML to ..
    # Execute shell
    print("convertHtmlToPdf convertHtmlToPdf convertHtmlToPdf convertHtmlToPdf !!! ")
    print("Authorization header => " + authToken)
    print("Given QuoteID => " + quoteId)
    print("Given filename => " + filename)
    print("Given HTML => " + htmlText)

    attachPdfToCrm(authToken, htmlText, quoteId, filename)

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
    # TODO save the HTML to tmpspool/$filename
    htmlText = request.form["htmltext"]

    thread = multiprocessing.Process(target=convertHtmlToPdf, args=(authToken,htmlText,quoteId,outputFilename))
    thread.start()



if __name__ == '__main__':
    app.run(debug=True)
