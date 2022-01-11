from flask import *
from API_Connector import ApiConnector

app = Flask(__name__)


@app.route('/get_data')
def get_users():

    api_con = ApiConnector()
    balances = api_con.get_balances()

    # data = [{
    #     'name': 'Harsha',
    #     'email': 'email',
    # },
    #     {
    #         'name': 'Rajender',
    #         'email': 'mail',
    #     }
    # ]
    return jsonify(balances)


if __name__ == '__main__':
    app.run(debug=True)