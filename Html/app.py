from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)

# Подключение к SQL Server (замени Driver при необходимости)
conn_str = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=W2CSM-K09CUUVH5;"
    "Database=SportBuyDB;"
    "Trusted_Connection=yes;"
)

def get_conn():
    return pyodbc.connect(conn_str)

@app.route("/buy", methods=["POST"])
def buy():
    data = request.json
    seats = data["seats"]
    name = data["name"]
    email = data["email"]
    birth = data["dob"]
    event = data.get("event", "default")

    conn = get_conn()
    cursor = conn.cursor()

    for seat in seats:
        row, col = map(int, seat.split("-"))
        cursor.execute("""
            INSERT INTO Tickets (EventName, SeatRow, SeatCol, FullName, Email, DateBirth, IsTaken)
            VALUES (?, ?, ?, ?, ?, ?, 1)
        """, (event, row, col, name, email, birth))

    conn.commit()
    conn.close()
    return jsonify({"message": "Билеты успешно куплены!"})

@app.route("/taken_seats", methods=["GET"])
def taken():
    event = request.args.get("event", "default")
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT SeatRow, SeatCol FROM Tickets WHERE EventName = ? AND IsTaken = 1", event)
    taken = [f"{row}-{col}" for row, col in cursor.fetchall()]
    conn.close()
    return jsonify({"taken": taken})

if __name__ == "__main__":
    app.run(debug=True)
