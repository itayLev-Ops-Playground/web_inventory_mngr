from flask import Flask, render_template, request, redirect
from helpers import get_dummy_data, set_dummy_data, update_net_req

app = Flask(__name__)

# -------- HOME PAGE --------
@app.route("/")
def home():
    data = get_dummy_data()
    return render_template("index.html", data=data)

# -------- UPDATE SYSTEM --------
@app.route("/update", methods=["POST"])
def update():
    model = request.form["model"]
    system = request.form["system"]
    available = int(request.form["available"])
    gross = int(request.form["gross"])

    data = get_dummy_data()

    for m in data:
        if m["model"] == model:
            if system in m["systems"]:
                m["systems"][system]["available"] = available
                m["systems"][system]["gross"] = gross

    set_dummy_data(data)
    update_net_req()

    return redirect("/")
    
# -------- START SERVER --------
if __name__ == "__main__":
    app.run(debug=True)