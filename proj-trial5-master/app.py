import flask
import pickle
import pandas as pd

# Use pickle to load in the pre-trained model
with open(f'model/model6.pkl', 'rb') as f:
    model = pickle.load(f)

# Initialise the Flask app
app = flask.Flask(__name__, template_folder='templates')

# Set up the main route


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
    app.run()
