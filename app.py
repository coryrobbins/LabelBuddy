from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    # Load the CSV file into a Pandas dataframe
    df = pd.read_csv('emails.csv')

    # Get the next email to label
    email = get_next_email(df)

    # If there are no more emails to label, return a message
    if email is None:
        return 'No emails to label'

    # Render the template with the email and the labels
    return render_template('index.html', email=email, labels=['Label 1', 'Label 2', 'Label 3', 'Label 4', 'Label 5', 'Label 6', 'Label 7'])

@app.route('/label', methods=['POST'])
def label():
    # Load the CSV file into a Pandas dataframe
    df = pd.read_csv('emails.csv')

    # Get the label from the form data
    label = request.form['label']

    # Get the index of the email to label
    index = get_next_email_index(df)

    # Update the label in the dataframe
    df.loc[index, 'label'] = label

    # Save the dataframe back to the CSV file
    df.to_csv('emails.csv', index=False)

    # Redirect back to the index page to show the next email
    return redirect(url_for('index'))

def get_next_email(df):
    # Find the first email that hasn't been labeled yet
    email = df.loc[df['label'].isna(), 'body'].iloc[0]

    return email

def get_next_email_index(df):
    # Find the index of the first email that hasn't been labeled yet
    index = df.loc[df['label'].isna(), 'body'].index[0]

    return index

if __name__ == '__main__':
    app.run(debug=True)

