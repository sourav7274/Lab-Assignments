import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask,render_template,request
from pandas import read_csv

app = Flask(__name__)

def studentData(id):
    df = pd.read_csv('data (1).csv')
    return df[df['Student id'].astype(str).str.strip() == str(id).strip()]

def courseData(id):
    df = read_csv("data (1).csv")
    return df[df[' Course id'].astype(str).str.strip() == str(id).strip()]

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        id_type = request.form.get('ID')
        id_value = request.form.get('id_value')
        if id_type == 'student_id':
            data = studentData(id_value)
            if not data.empty:
                tMarks = data[' Marks'].sum()
                return render_template('student.html', data=data.to_dict(orient='records'), tMarks=tMarks), 200
            else:
                return render_template('default.html'), 200
        elif id_type == 'course_id':
            data = courseData(id_value)
            if not data.empty:
                total = data[' Marks'].sum()
                avg = total/len(data)
                maxS = data[' Marks'].max()

                plt.figure(figsize=(8,5))
                plt.hist(data[' Marks'], bins=10)
                plt.ylabel('Frequency')
                plt.savefig('static/plot.png')
                plt.close()

                return render_template('course.html',avg=avg,maxS=maxS), 200
            else:
                return render_template('default.html'), 200
        else:
            return render_template('default.html'), 200
    return render_template('index.html'), 200

if __name__ == '__main__':
    app.run()
