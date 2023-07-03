from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Set up MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['form_data']
collection = db['submissions']


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        submission = {
            'name': request.form['name'],
            'rollno': request.form['rollno'],
            'college': request.form['college'],
            'course': request.form['course'],
            'branch': request.form['branch'],
            'year': request.form['year']
        }

        # Insert the document into MongoDB
        result = collection.insert_one(submission)
        inserted_id = str(result.inserted_id)  # Convert the ObjectId to string

        return redirect(f'/thankyou/{inserted_id}')

    return render_template('form.html')


@app.route('/thankyou/<submission_id>')
def thankyou(submission_id):
    return render_template('thankyou.html', submission_id=submission_id)


@app.route('/view/<submission_id>')
def view_submission(submission_id):
    submission = collection.find_one({'_id': ObjectId(submission_id)})
    return render_template('view_submission.html', submission=submission, submission_id=submission_id)


@app.route('/update/<submission_id>', methods=['GET', 'POST'])
def update_submission(submission_id):
    if request.method == 'POST':
        submission = {
            'name': request.form['name'],
            'rollno': request.form['rollno'],
            'college': request.form['college'],
            'course': request.form['course'],
            'branch': request.form['branch'],
            'year': request.form['year']
        }

        # Update the document in MongoDB
        collection.update_one({'_id': ObjectId(submission_id)}, {'$set': submission})

        return redirect(f'/thankyou/{submission_id}')

    submission = collection.find_one({'_id': ObjectId(submission_id)})
    return render_template('update_submission.html', submission=submission, submission_id=submission_id)


if __name__ == '__main__':
    app.run(debug=True)
