from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

def get_labels(email):
    labels= ['Label 1','Label 2','Label 3', 'Label 4', 
             'Label 5', 'Label 6','Label 7', 'Label 8',
             'Label 9', 'Label 10','Label 11', 'Label 12',
             'Label 13', 'Label 14','Non-Technical'
            ]
    return labels

def load_dataframe():
    file_name = 'emails.csv'
    df = pd.read_csv(file_name)
    return df

def save_dataframe(df):
    file_name = 'emails.csv'
    df.to_csv(file_name, index=False)

def get_email_by_index(df, index):
    email = df.loc[df.index == index, 'body'].iloc[0]
    return email

def get_previous_email_index(df, index):
    #previous_index = df.index[df.index.get_loc(index) - 1] if df.index.get_loc(index) > 0 else index
    previous_index = df.index[df.index.get_loc(index) - 1] if df.index.get_loc(index) > 0 else df.index[-1]
    return previous_index

@app.route('/')
def index():
    df = load_dataframe()
    index = int(request.args.get('index') or 0)
    email = df.loc[index, 'body']
    assigned_label = df.loc[index, 'label'] or 'Not Assigned'
    labels = get_labels(email)

    labeled_indices = df[df['label'].notnull()].index.tolist()
    assigned_index = labeled_indices.index(index) if index in labeled_indices else -1

    return render_template('index.html', email=email, assigned_label=assigned_label, labels=labels, assigned_index=assigned_index, index=index)

def get_next_email_index(df, current_index):
    next_index = df.index[df.index > current_index]
    if next_index.size == 0:
        return None 
    else:    
        return next_index[0]
    
@app.route('/label', methods=['POST'])
def label():
    df = load_dataframe()
    index = int(request.form.get('index') or 0)

    if 'label' in request.form:
        label = request.form['label'].strip()
        df.loc[index, 'label'] = label
        save_dataframe(df)

    direction = request.form.get('direction')
    if direction == 'next':
        next_index = get_next_email_index(df, index)
        if next_index is not None:
            return redirect(url_for('index', index=next_index))
    elif direction == 'prev':
        prev_index = get_prev_email_index(df, index)
        if prev_index is not None:
            return redirect(url_for('index', index=prev_index))
    return redirect(url_for('index', index=index))

elif 'previous_email' in request.form:
try:
        previous_index = get_previous_email_index(df, index)
    except KeyError:
        previous_index = get_previous_email_index(df, index-1)
    return redirect(url_for('index', index=previous_index))
elif 'next_email' in request.form:
    next_index = get_next_email_index(df, index)
    if next_index is not None:
        return redirect(url_for('index', index=next_index))
    else:
        return redirect(url_for('index', index=index)) 
else:
    # Return a default response if no action was taken
    return redirect(url_for('index', index=index))

if __name__ == '__main__':
    app.run(debug=True)