from app import app
from flask import render_template
from flask import request
import Query_Handler

@app.route('/')
def index():
    user_input = request.args.get('query')
    if user_input != None and user_input != '':
        results = Query_Handler.search(user_input)
        number_of_results = len(results[0])
        print(user_input)
        return render_template('results.html', results=results[0], number_of_results=number_of_results, user_input=user_input, suggestion=' '.join(results[1]))
    else:
        return render_template('index.html')