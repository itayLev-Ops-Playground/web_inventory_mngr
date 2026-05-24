from flask import Flask, render_template, request, redirect
from helpers import get_dummy_data, set_dummy_data, update_net_req
from helpers import get_data_base, set_data_base

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


# -------- ADD MODEL --------
@app.route("/add_model", methods=["POST"])
def add_model():
    name = request.form["model"]

    data = get_dummy_data()

    new_model = {
        "model": name,
        "id": 999999,
        "systems": {
            "engine": {"available": 0, "gross": 0, "net-req": 0},
            "air-frame": {"available": 0, "gross": 0, "net-req": 0},
        }
    }

    data.append(new_model)
    set_dummy_data(data)

    return redirect("/")


# -------- DELETE MODEL --------
@app.route("/delete/<model>")
def delete(model):
    data = get_dummy_data()

    data = [m for m in data if m["model"] != model]

    set_dummy_data(data)

    return redirect("/")


# -------- COMMIT CHANGES --------
@app.route("/commit")
def commit():
    data = get_dummy_data()
    set_data_base(data)

    return redirect("/")

    
# -------- START SERVER --------
if __name__ == "__main__":
    app.run(debug=True)