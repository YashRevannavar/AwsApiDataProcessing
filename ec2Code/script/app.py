from flask import Flask, render_template, request, redirect, url_for
import pandas as pd 
import boto3
from io import StringIO

# Create an S3 client
s3 = boto3.client('s3')

# Create a Flask app
app = Flask(__name__)

def getDF():
    """
    Retrieves a Pandas DataFrame from an S3 bucket.
    Returns:
    Pandas DataFrame: The DataFrame retrieved from S3.
    """
    csv_obj = s3.get_object(Bucket='yash-all-csv-bucket', Key='completeDf.csv')
    body = csv_obj['Body']
    csv_string = body.read().decode('utf-8')
    df = pd.read_csv(StringIO(csv_string))
    return df

@app.route('/', methods=['GET', 'POST'])
def homeQ():
    """
    Renders the home page and processes user queries.
    Returns:
    str: The HTML content to be displayed.
    """
    if request.method == 'POST':
        if request.form.get('Query') == 'done':
            # Get the search parameters from the user
            star=request.form.get('star')
            word=request.form.get('word')
            # Query the DataFrame for articles matching the search parameters
            df = getDF()
            df = df.drop_duplicates()
            df = df.query(f'{star}.str.contains("{word}")', engine='python').filter(items=request.form.getlist('Column'))
            # Render the data query page with the results
            return render_template("dataQuery.html",tables=[df.to_html(classes='data')], titles=df.columns.values)
    # Render the home page
    return render_template("index.html")


@app.route('/all',methods=['GET', 'POST'])
def dfAll():
    """
    Renders a page displaying the entire DataFrame.
    Returns:
    str: The HTML content to be displayed.
    """
    # Retrieve the DataFrame from S3
    df = getDF()
    # Render the data query page with the entire DataFrame
    if request.method == 'GET':
        return render_template("dataQuery.html",tables=[df.to_html(classes='data')], titles=df.columns.values)

if __name__ == '__main__':
    # Start the Flask app
    app.run(debug=True)
