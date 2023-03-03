from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
#import pdb; pdb.set_trace()

app = Flask(__name__)
labels = ['Label 1','Label 2','Label 3', 'Label 4', 
          'Label 5', 'Label 6','Label 7', 'Label 8',
          'Label 9', 'Label 10','Label 11', 'Label 12',
          'Label 13', 'Label 14','Non-Technical'
          ]

def load_dataframe():
    file_name = 'emails.csv'
    df = pd.read_csv(file_name)
    return df

def get_email_by_index(df, index):
    email = df.loc[df.index == index, 'body'].iloc[0]
    return email

def get_previous_email_index(df, index):
    previous_index = df.index[df.index < index][-1]if df.index[df.index < index].size > 0 else index
    return previous_index

@app.route('/')
@app.route('/index/<int:index>')
def index(index=None):
    df = load_dataframe()
    if index is None:
        index = get_next_email_index(df, -1)
    if index is None:
        return "No more emails to label."
    email = get_email_by_index(df, index)
    assigned_label = df.loc[index, 'label']
    if pd.isna(assigned_label):
        assigned_label = 'Not Assigned'
    return render_template("index.html", email=email, labels=labels, assigned_index=index, assigned_label=assigned_label)

def get_next_email_index(df, index):
    """
    Get the next email index greater than the given index.

    Args:
        df (pandas.DataFrame): Dataframe containing the email data.
        index (int or callable): Index of the email to get the next index for.

    Returns:
        int: Next email index.
    """
    if callable(index):
        index = index()
    next_index = df.index[df.index > index]
    if next_index.size == 0:
        return "No more emails to label." 
    else:    
        return next_index[0]
    
@app.route('/label', methods=['POST'])
def label():
    df = load_dataframe()
    index = request.form.get('index', 0)
    index = int(index)
    print(f"Index: {index}")
    if 'label' in request.form:
        label = request.form['label'].strip()
        if label in labels:
            print(f"Index: {index}")
            df.loc[index, 'label'] = label
            df.to_csv('emails.csv', index=False)
            next_index = get_next_email_index(df, index)
            print(f"Next Index: {next_index}")
            return redirect(url_for('index', index=next_index))
    elif 'next_email' in request.form:
        print(f"Before calling get_next_email_index: index = {index}")
        next_index = get_next_email_index(df, index)
        print(f"After calling get_next_email_index: next_index = {next_index}")
        return redirect(url_for('index', index=next_index))
    elif 'previous_email' in request.form:
        previous_index = get_previous_email_index(df, index)
        print(f"Previous Index: {previous_index}")
        return redirect(url_for('index', index=previous_index))
    return redirect(url_for('index', index=index))

if __name__ == '__main__':
    app.run(debug=True)