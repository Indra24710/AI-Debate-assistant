from metaphor_python import Metaphor
from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS
from negate import Negator
from bs4 import BeautifulSoup


app = Flask(__name__)
CORS(app, resources={r"/submit": {"origins": "http://localhost:4200"}})

def get_results_from_metaphor(query = ""):
    metaphor = Metaphor("API Key")

    for_response = metaphor.search(query, use_autoprompt = False)
    contents_for_response = for_response.get_contents()
    negator = Negator()
    negated_sentence = negator.negate_sentence(query)
    against_response = metaphor.search( negated_sentence, use_autoprompt = False)
    print("negated sentence",negated_sentence)
    contents_against_response = against_response.get_contents()
    response = {"for":[],"against":[],"negated_sentence":negated_sentence}
    # Print content for each result
    for content in contents_for_response.contents:
        htmlContent = content.extract
        soup = BeautifulSoup(htmlContent, 'html.parser')
        cleanContent = ""
        for tags in soup.find_all():
            cleanContent += tags.get_text() + " "


        response["for"].append([content.url, cleanContent])

    for content in contents_against_response.contents:
        htmlContent = content.extract
        soup = BeautifulSoup(htmlContent, 'html.parser')
        cleanContent = ""
        for tags in soup.find_all():
            cleanContent += tags.get_text() + " "


        response["against"].append([content.url, cleanContent])

    return response

@app.route('/submit', methods=['GET'])
def submit():
    if request.method == 'GET':
        
        query = request.args.get('query', '')
        print("got query", query)
        response = get_results_from_metaphor(query)

        return response


if __name__ == '__main__':
    app.run(debug=True)
