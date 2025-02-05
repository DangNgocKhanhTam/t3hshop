from flask import Flask, render_template
from datetime import datetime
app = Flask(__name__)

def get_current_time(): 
    return datetime.now().strftime("%A, %d %B %Y (Đọc thời gian của hệ thống)")


@app.route("/")
def index(): 
    current_time= get_current_time()
    return render_template('index.html', current_time=current_time)

if __name__ == '__main__': 
    app.run(debug=True)