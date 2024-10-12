import sys
import pandas as pd
from jinja2 import Template
import matplotlib.pyplot as plt

# 100 % public test case

defaultTemplate = Template("""
<!DOCTYPE html>
<html>
<body>
<h1>Wrong Inputs</h1>
<p>Something went wrong</p>
</body>
</html>
""")

csvData = pd.read_csv('data.csv', names=['Student id', 'Course id', 'Marks'], dtype={'Student id': str,'Course id':str})
csvData['Course id'] = csvData['Course id'].str.strip().str.lower()

if len(sys.argv) == 3:
    type = sys.argv[1]
    id = sys.argv[2]
else:
    with open('output.html', 'w') as f:
        f.write(defaultTemplate.render())
courseData = csvData[csvData['Course id'] == id]
courseData['Marks'] = courseData['Marks'].astype(int)
tCMarks = courseData['Marks'].sum()
avgMarks = tCMarks/len(courseData)
maxMarks = courseData['Marks'].max()

filterData = csvData[csvData['Student id'] == id]
filterData['Marks'] = filterData['Marks'].astype(int)
tMarks = filterData['Marks'].sum()
studentTemplate = Template("""
<!DOCTYPE html>
<html>
<head>
    <style>
         table{
            border: 1px solid black
        }
        th, td {
            border: 1px solid black; /* Add border to cells */
            padding: 8px; /* Add some padding for better spacing */
            text-align: left; /* Align text to the left */
        }
        th {
            text-align: center; /* Center align the header text */
        }
    </style>
</head>
<body>
<h1>Student Details</h1>
<table>
    <thead>
        <tr>
            <th>Student id</th>
            <th>Course id</th>
            <th>Marks</th>
        </tr>
    </thead>
    <tbody>
        {% for row in data %}
        <tr>
            <td>{{ row['Student id'] }}</td>
            <td>{{ row['Course id'] }}</td>
            <td>{{ row['Marks'] }}</td>
        </tr>
        {% endfor %}
    </tbody>
    <tfoot>
        <tr>
            <td colspan="2" style="text-align: center;">Total Marks:</td>
            <td>{{ total_marks }}</td>
        </tr>
    </tfoot>
</table>
</body>
</html>
""")


courseTemplate = Template("""
<!DOCTYPE html>
<html>
<head>
    <style>
         table{
            border: 1px solid black
        }
        th, td {
            border: 1px solid black; /* Add border to cells */
            padding: 8px; /* Add some padding for better spacing */
            text-align: left; /* Align text to the left */
        }
    </style>
</head>
<body>
<h1>Course Details</h1>
<table>
    <thead>
        <tr>
            <th>Average Marks</th>
            <th>Maximum Marks</th>
         </tr>
    </thead>
    <tbody>
        <tr>
            <td>{{ avg_marks }}</td>
            <td>{{ max_marks }}</td>
        </tr>
    </tbody>   
</table>
<img src="histogram.png" alt="histogram"/>
</body>
</html>
""")

defaultTemplate = Template("""
<!DOCTYPE html>
<html>
<body>
<h1>Wrong Inputs</h1>
<p>Something went wrong</p>
</body>
</html>
""")
if type == '-s' and  not filterData.empty:
    with open('output.html', 'w') as f:
        f.write(studentTemplate.render(id=id,total_marks=tMarks, data=filterData.to_dict(orient='records')))
elif type == '-c' and not courseData.empty:
    plt.figure(figsize=(8,6))
    plt.hist(courseData['Marks'], bins=10)
    plt.xlabel('Marks')
    plt.ylabel('Frequency')
    plt.savefig('histogram.png')
    plt.close()
    with open('output.html', 'w') as f:
        f.write(courseTemplate.render(avg_marks = avgMarks, max_marks = maxMarks))
else:
    with open('output.html', 'w') as f:
        f.write(defaultTemplate.render())
