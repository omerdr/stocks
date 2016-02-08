import csv
import decimal
import pickle

from pandas import DataFrame

from financial_utils import PRICE_CHANGE_FIELDS, PRICE_CHANGE_DATE_FORMAT
from datetime import datetime
import scipy.io as sio

INPUT_FILE_NAME = 'data/merged_analysts_quotes_2014_predictions.csv'  # Input is merged stocks and analyst predictions
OUT_DATA_MATRIX_PYTHON_FILE = 'data/data_matrix.pkl'
OUT_DATA_MATRIX_MATLAB_FILE = 'data/data_matrix.mat'

RESPONSE_LABEL = "_response_"


def construct_data_matrix(input_file_name, output_filename_python, output_filename_matlab, has_header=True):
    data = dict()  # used to store the data matrix Z
    data_dates = dict()  # used to store the dates used in the data matrix
    # response_vector = dict()  # response vector y

    ticker = None
    with open(input_file_name, 'r') as infile:
        if has_header:
            infile.readline()

        for l in csv.reader(infile):

            cur_date = datetime.strptime(l[PRICE_CHANGE_FIELDS.Date.zvalue], PRICE_CHANGE_DATE_FORMAT)

            # Filter everything that's not from 2014 H2
            if cur_date.year != 2014 or cur_date.month < 6:
                continue

            # Filter lines without an analyst target price
            try:
                Pi = float(l[PRICE_CHANGE_FIELDS.New_Target.zvalue])  # Analyst prediction = Pi / Peoq
            except ValueError:
                continue

            Peoq = float(l[PRICE_CHANGE_FIELDS.Current_Price.zvalue])
            Pf = float(l[PRICE_CHANGE_FIELDS.Price_in_a_year.zvalue])  # true values y = Pf / Peoq
            analyst = l[PRICE_CHANGE_FIELDS.Firm.zvalue]

            if ticker != l[PRICE_CHANGE_FIELDS.Ticker.zvalue]:
                ticker = l[PRICE_CHANGE_FIELDS.Ticker.zvalue]
                data[ticker] = dict()
                data_dates[ticker] = dict()
                data[ticker][RESPONSE_LABEL] = Pf /Peoq

            # Don't assume data is ordered latest first
            if analyst not in data[ticker] or data_dates[ticker][analyst] < cur_date:
                data[ticker][analyst] = Pi / Peoq
                data_dates[ticker][analyst] = cur_date

            # if ticker not in response_vector:
            #     response_vector[ticker] = Pf / Peoq

    pickle.dump(data, open(output_filename_python, 'wb'))
    # Z = pickle.load(open('data/data_matrix.pkl'))

    df = DataFrame(data).T.fillna(0)
    column_labels = df.columns.tolist()  # Firms
    row_labels = df.T.columns.tolist()  # Tickers
    # df['Citigroup Inc.']
    # df.T['AAPL']

    savedict = {"data": df.as_matrix(), "column_labels": column_labels, "row_labels": row_labels}
    sio.savemat(output_filename_matlab, savedict)


def main():
    construct_data_matrix(INPUT_FILE_NAME, OUT_DATA_MATRIX_PYTHON_FILE, OUT_DATA_MATRIX_MATLAB_FILE)


if __name__ == "__main__":
    main()
