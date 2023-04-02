from flask import Flask, render_template, request, redirect, url_for
import pandas as pd 
import boto3
from io import StringIO

s3 = boto3.client('s3')
app = Flask(__name__)

def getDF():
    csv_obj = s3.get_object(Bucket='yash-all-csv-bucket', Key='completeDf.csv')
    body = csv_obj['Body']
    csv_string = body.read().decode('utf-8')
    df = pd.read_csv(StringIO(csv_string))
    return df

@app.route('/', methods=['GET', 'POST'])
def homeQ():
    if request.method == 'POST':
        if request.form.get('Query') == 'done':
            star=request.form.get('star')
            word=request.form.get('word')
            df = getDF()
            df = df.drop_duplicates()
            df = df.query(f'{star}.str.contains("{word}")', engine='python').filter(items=request.form.getlist('Column'))
            return render_template("dataQuery.html",tables=[df.to_html(classes='data')], titles=df.columns.values)
    return render_template("index.html")


@app.route('/all',methods=['GET', 'POST'])
def dfAll():
    df = getDF()
    if request.method == 'GET':
        return render_template("dataQuery.html",tables=[df.to_html(classes='data')], titles=df.columns.values)

if __name__ == '__main__':
    app.run(debug=True)












# @app.route('/dbf')
# def queryFine(dbf):
#     df = dbf
#     return render_template("dataQuery.html",tables=[df.to_html(classes='data')], titles=df.columns.values)




# def hello_world():
#     if request.method == 'POST':
#         if request.form.get('action1') == 'VALUE1':
#             # return render_template('data.html',form_data = form_data)
#             text01 =  request.form.get('Column')
#             print(text01)
#             # return text01
#             pass # do something
#         elif  request.form.get('action2') == 'VALUE2':
#             pass # do something else
#         else:
#             pass # unknown
#     elif request.method == 'GET':
#         return render_template('index.html')
#     return render_template("index.html")


# def queryData():
#     csv_obj = s3.get_object(Bucket='yash-all-csv-bucket', Key='completeDf.csv')
#     body = csv_obj['Body']
#     csv_string = body.read().decode('utf-8')
#     df = pd.read_csv(StringIO(csv_string))
#     df = df.drop_duplicates()
#     df = df.query('name.str.contains(".com")', engine='python').filter(items=request.form.getlist('Column'))
#     return render_template(df)
    # return render_template("dataQuery.html",tables=[df.to_html(classes='data')], titles=df.columns.values)


