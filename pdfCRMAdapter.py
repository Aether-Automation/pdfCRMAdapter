from flask import Flask, jsonify, request
import requests
import subprocess
import multiprocessing
# import dataset
import time
import random
import sys


app = Flask(__name__)

"""
Flow:
DONE - -> CRM kicks-off process from 'Generate Quote' button action.
DONE - -> Images, details are spooled.  Images are accessible online, details are used to fill in an HTML page.
DONE - -> Call to endpoint occurs; the posted parameters are 'filename' 'htmltext' 'quoteId'
DONE-> Endpoint forks a separate python method:
DONE    --> This method invokes curl to turn the HTML into a PDF, and then invokes curl to attach in CRM.

"""

# Phase 3 -- final, attach.
def attachPdfToCrm(authToken, htmlText, module, recordId, filename):
    url = 'https://www.zohoapis.com/crm/v2/' + module + '/' + recordId + '/Attachments'
    headers = {
        'Authorization': authToken
    }
    request_body = {
        'file': open(
            filename + '.pdf',
            'rb')
    }
    # print("filename => " + filename)
    response = requests.post(url=url, files=request_body, headers=headers)
    # if response is not None:
    #     print("HTTP Status Code : " + str(response.status_code))
    #     print(response.json())
    return True

# Phase 2 -- convert HTML to PDF.
def convertHtmlToPdf(authToken, htmlText, module, recordId, filename):
    # print("convertHtmlToPdf convertHtmlToPdf convertHtmlToPdf convertHtmlToPdf !!! ")
    time.sleep(15)  # Ensures the files are copied first.
    orgHtml = open(filename + '.html', "w")
    htmlFilename = filename + '.html'
    orgHtml.write(htmlText)
    orgHtml.close()
    result = subprocess.run(["curl", "-v", "-X", "POST", "-d",
                             "@" + htmlFilename, "-JLO",
                             "http://138.197.166.196:5001/pdf?filename=" + filename + ".pdf"])
    attachPdfToCrm(authToken, htmlText, module, recordId, filename)
    return True


# Headers: Need 'Authorization: Zoho-oauthtoken'
# Phase 1 -- get the headers and relevant data to service the request.
@app.route('/', methods=['POST'])
def index():
    # print("Authorization header => " + request.headers['Authorization'])
    # print("Given QuoteID => " + request.form["quoteId"])
    # print("Given filename => " + request.form["filename"])
    # print("Given HTML => " + request.form["htmltext"])
    authToken = request.headers['Authorization']
    recordId = request.form["recordId"]
    module = request.form["module"]
    outputFilename = request.form["filename"]
    htmlText = request.form["htmltext"]


    thread = multiprocessing.Process(target=convertHtmlToPdf, args=(authToken,htmlText,module,recordId,outputFilename))
    thread.start()
    return "Hello, World."


if __name__ == '__main__':
    app.run(debug=True)
