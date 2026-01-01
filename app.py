from flask import Flask, render_template_string
import sqlite3

app = Flask(__name__)

def get_db_data(query):
    conn = sqlite3.connect("parkir.db")
    c = conn.cursor()
    c.execute(query)
    results = c.fetchall()
    conn.close()
    return results

# Halaman penghuni (root)
@app.route("/")
def index():
    slots = get_db_data("SELECT Slot_Parkir_ID, Slot_Parkir_Label, Slot_Parkir_Status FROM Slot_Parkir")
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Status Slot Parkir</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background: linear-gradient(to bottom right, #ffe0f0, #fff0f5);
                margin: 0;
                padding: 0;
                text-align: center;
            }
            .header {
                background-color: #c2185b;
                color: white;
                padding: 30px 0;
                font-size: 32px;
                font-weight: bold;
                position: relative;
            }
            .header::after {
                content: "🏢"; 
                font-size: 48px;
                position: absolute;
                right: 20px;
                top: 10px;
            }
            table {
                width: 60%;
                margin: 30px auto;
                border-collapse: collapse;
                box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
            }
            th, td { border: 1px solid #ddd; padding: 12px; text-align: center; }
            th { background-color: #e91e63; color: white; }
            tr:nth-child(even) { background-color: #f8bbd0; }
            .status-terisi { background-color: #f44336; color: white; font-weight: bold; }
            .status-kosong { background-color: #4caf50; color: white; font-weight: bold; }
            .welcome { font-size: 24px; margin: 20px 0; color: #880e4f; }
            .decoration { font-size: 36px; margin-bottom: 20px; }
        </style>
    </head>
    <body>
        <div class="header">Status Slot Parkir</div>
        <div class="welcome">Selamat Datang di Apartemen!</div>
        <div class="decoration">✨🏠✨</div>
        <table>
            <tr><th>ID Slot</th><th>Label</th><th>Status</th></tr>
            {% for slot in slots %}
            <tr>
                <td>{{ slot[0] }}</td>
                <td>{{ slot[1] }}</td>
                <td class="{{ 'status-terisi' if slot[2] else 'status-kosong' }}">
                    {{ 'Terisi' if slot[2] else 'Kosong' }}
                </td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    return render_template_string(html, slots=slots)

# Halaman admin (terpisah, hanya diakses dengan /admin)
@app.route("/admin")
def admin():
    transaksi = get_db_data("SELECT * FROM Transaksi_Parkir")
    total_transaksi = len(transaksi)
    total_pendapatan = sum([t[5] for t in transaksi]) if transaksi else 0
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin Parkir</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #e0f7fa; text-align: center; margin: 0; padding: 0; }
            h1, h2 { color: #00796b; padding: 10px 0; }
            table { width: 70%; margin: 20px auto; border-collapse: collapse; box-shadow: 0px 4px 8px rgba(0,0,0,0.2); }
            th, td { border: 1px solid #ddd; padding: 10px; text-align: center; }
            th { background-color: #0288d1; color: white; }
            tr:nth-child(even) { background-color: #b3e5fc; }
        </style>
    </head>
    <body>
        <h1>Data Transaksi Parkir</h1>
        <table>
            <tr>
                <th>ID Transaksi</th><th>ID Kendaraan</th><th>ID Pengelola</th>
                <th>Waktu Masuk</th><th>Waktu Keluar</th><th>Biaya</th>
            </tr>
            {% for t in transaksi %}
            <tr>
                <td>{{ t[0] }}</td><td>{{ t[1] }}</td><td>{{ t[2] }}</td>
                <td>{{ t[3] }}</td><td>{{ t[4] }}</td><td>{{ t[5] }}</td>
            </tr>
            {% endfor %}
        </table>
        <h2>Laporan & Analisis</h2>
        <p>Total transaksi: {{ total_transaksi }}</p>
        <p>Total pendapatan: Rp {{ total_pendapatan }}</p>
    </body>
    </html>
    """
    return render_template_string(html, transaksi=transaksi, total_transaksi=total_transaksi, total_pendapatan=total_pendapatan)

if __name__ == "__main__":
    app.run(debug=True)
