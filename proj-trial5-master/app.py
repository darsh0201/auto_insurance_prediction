import flask
import pickle
import pandas as pd
import yaml
from flask_mysqldb import MySQL


# Use pickle to load in the pre-trained model
with open(f'proj-trial5-master\model\model6.pkl', 'rb') as f:
    model = pickle.load(f)

# Initialise the Flask app
app = flask.Flask(__name__, template_folder='templates')

# Configure db
db = yaml.safe_load(open(
    'C:/Users/Darsh/OneDrive/Desktop/auto_insurance_mysql/proj-trial5-master/db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']


mysql = MySQL(app)

# Set up the main route


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if flask.request.method == 'POST':
        # Fetch form data
        userDetails = flask.request.form
        name = userDetails['name']
        email = userDetails['email']
        phone = userDetails['phone']
        subject = userDetails['subject']
        comments = userDetails['comments']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO customers(name, email, phone, subject, comments) VALUES(%s, %s, %s, %s, %s)",
                    (name, email, phone, subject, comments))
        mysql.connection.commit()
        cur.close()
        return 'We will contact you soon'

        # Just render the contact form, to get input
    return(flask.render_template('contact.html'))


@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('main.html'))

    if flask.request.method == 'POST':
        # Extract the input
        CustomerLifetimeValue = flask.request.form['CustomerLifetimeValue']
        Coverage = flask.request.form['Coverage']
        Education = flask.request.form['Education']
        EmploymentStatus = flask.request.form['EmploymentStatus']
        Gender = flask.request.form['Gender']
        Income = flask.request.form['Income']
        MaritalStatus = flask.request.form['MaritalStatus']
        MonthsSinceLastClaim = flask.request.form['MonthsSinceLastClaim']
        MonthsSincePolicyInception = flask.request.form['MonthsSincePolicyInception']
        NumberofOpenComplaints = flask.request.form['NumberofOpenComplaints']
        TotalClaimAmount = flask.request.form['TotalClaimAmount']
        VehicleClass = flask.request.form['VehicleClass']
        VehicleSize = flask.request.form['VehicleSize']

        # Make DataFrame for model
        input_variables = pd.DataFrame([[CustomerLifetimeValue, Coverage, Education, EmploymentStatus, Gender, Income, MaritalStatus, MonthsSinceLastClaim, MonthsSincePolicyInception, NumberofOpenComplaints, TotalClaimAmount, VehicleClass, VehicleSize]],
                                       columns=['CustomerLifetimeValue', 'Coverage', 'Education', 'EmploymentStatus', 'Gender', 'Income', 'MaritalStatus',
                                                'MonthsSinceLastClaim', 'MonthsSincePolicyInception', 'NumberofOpenComplaints', 'TotalClaimAmount', 'VehicleClass', 'VehicleSize'],
                                       dtype=float,
                                       index=['input'])

        # Get the model's prediction
        prediction = model.predict(input_variables)[0]

        # Render the form again, but add in the prediction and remind user
        # of the values they input before
        return flask.render_template('main.html',
                                     original_input={'CustomerLifetimeValue': CustomerLifetimeValue,
                                                     'Coverage': Coverage,
                                                     'Education': Education,
                                                     'EmploymentStatus': EmploymentStatus,
                                                     'Gender': Gender,
                                                     'Income': Income,
                                                     'MaritalStatus': MaritalStatus,
                                                     'MonthsSinceLastClaim': MonthsSinceLastClaim,
                                                     'MonthsSincePolicyInception': MonthsSincePolicyInception,
                                                     'NumberofOpenComplaints': NumberofOpenComplaints,
                                                     'TotalClaimAmount': TotalClaimAmount,
                                                     'VehicleClass': VehicleClass,
                                                     'VehicleSize': VehicleSize,
                                                     },
                                     result=round(prediction),
                                     )


if __name__ == '__main__':
    app.run(debug=True)
