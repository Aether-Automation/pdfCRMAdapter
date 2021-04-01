from flask import Flask, jsonify, request
import requests
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
DONE-> Endpoint forks a separate python method:
    --> This method invokes curl to turn the HTML into a PDF, and then invokes curl to attach in CRM.

"""



def attachPdfToCrm(authToken, htmlText, quoteId, filename):
    url = 'https://www.zohoapis.com/crm/v2/Quotes/' + quoteId + '/Attachments'
    headers = {
        'Authorization': authToken
    }
    request_body = {
        'file': open(
            filename + '.pdf',
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
    # print("convertHtmlToPdf convertHtmlToPdf convertHtmlToPdf convertHtmlToPdf !!! ")
    # print("Authorization header => " + authToken)
    # print("Given QuoteID => " + quoteId)
    # print("Given filename => " + filename)
    # print("Given HTML => " + htmlText)

    # Save htmlText to filename.html.
    # Call to conversion URL.
    # Save the result to filename.pdf.

    url = 'http://138.197.166.196:5001/pdf?filename=' + filename + '.pdf'
    request_body = htmlText
    # print(type(request_body))
    response = requests.post(url=url, data=request_body.encode('ascii', 'ignore'))
    if response is not None:
        print("HTTP Status Code : " + str(response.status_code))
        tempFile = open(filename + '.pdf', "w")
        tempFile.write(response.text)
        tempFile.close()
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
    htmlText = request.form["htmltext"]

    thread = multiprocessing.Process(target=convertHtmlToPdf, args=(authToken,htmlText,quoteId,outputFilename))
    thread.start()
    return "Hello, World."


if __name__ == '__main__':
    app.run(debug=True)
