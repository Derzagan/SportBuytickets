from flask import Flask, request, jsonify
import pyodbc
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Подключение к SQL Server
conn_str = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=W2CSM-K09CUUVH5;"  # ← замени на свой, если отличается
    "Database=SportBuyDB;"
    "Trusted_Connection=yes;"
)

def get_conn():
    return pyodbc.connect(conn_str)

@app.route('/buy', methods=['POST'])
def buy():
    data = request.json
    event = data.get('event')
    seats = data.get('seats')
    name = data.get('name')
    email = data.get('email')
    dob = data.get('dob')

    conn = get_conn()
    cursor = conn.cursor()

    for seat in seats:
        row, col = seat.split('-')
        # Проверяем, занято ли уже место
        cursor.execute("""
            SELECT COUNT(*) FROM Tickets WHERE EventName=? AND SeatRow=? AND SeatCol=?
        """, (event, row, col))
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO Tickets (EventName, SeatRow, SeatCol, FullName, Email, DateBirth)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (event, row, col, name, email, dob))

    conn.commit()
    conn.close()
    return jsonify({'message': 'Билеты успешно приобретены!'})

@app.route('/taken_seats', methods=['GET'])
def taken_seats():
    event = request.args.get('event', 'default')

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT SeatRow, SeatCol FROM Tickets WHERE EventName = ?", event)
    rows = cursor.fetchall()
    taken = [f"{r[0]}-{r[1]}" for r in rows]
    conn.close()
    return jsonify({'taken': taken})

if __name__ == '__main__':
    app.run(debug=True)
