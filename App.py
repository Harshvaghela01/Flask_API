from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)
EXTERNAL_API_BASE_URL = "https://app.ylytic.com/ylytic/test"





@app.route('/search', methods=['GET'])
def search_comments():
    try:
        # Extract and validate search parameters from the request
        search_author = request.args.get('search_author')
        at_from = parse_date(request.args.get('at_from'))
        at_to = parse_date(request.args.get('at_to'))
        like_from = request.args.get('like_from')
        like_to = request.args.get('like_to')
        reply_from = request.args.get('reply_from')
        reply_to = request.args.get('reply_to')
        search_text = request.args.get('search_text')

        # Make a request to the existing API
        response = requests.get(EXTERNAL_API_BASE_URL)

        if response.status_code == 200:
            # Parse the response JSON
            comments = response.json()

            # Filter comments based on search criteria
            filtered_comments = filter_comments(comments, search_author, at_from, at_to, like_from, like_to, reply_from, reply_to, search_text)

            return jsonify(filtered_comments)
        else:
            return jsonify({"error": "Failed to fetch comments from the existing API"})
    except Exception as e:
        return jsonify({"error": str(e)})

def parse_date(date_str):
    if date_str:
        try:
            return datetime.strptime(date_str, "%d-%m-%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use 'dd-mm-yyyy'.")

def filter_comments(comments, search_author, at_from, at_to, like_from, like_to, reply_from, reply_to, search_text):
    filtered_comments = []

    for comment in comments:
        # Apply filters based on search parameters
        if search_author and search_author.lower() not in comment['author'].lower():
            continue
        if at_from and comment['at'] < at_from:
            continue
        if at_to and comment['at'] > at_to:
            continue
        if like_from and comment['like'] < int(like_from):
            continue
        if like_to and comment['like'] > int(like_to):
            continue
        if reply_from and comment['reply'] < int(reply_from):
            continue
        if reply_to and comment['reply'] > int(reply_to):
            continue
        if search_text and search_text.lower() not in comment['text'].lower():
            continue



        filtered_comments.append(comment)

    return filtered_comments

if __name__ == '__main__':
    app.run(debug=True)
