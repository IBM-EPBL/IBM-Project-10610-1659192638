import uuid
from flask import Flask

instance_id = uuid.uuid4().hex
app = Flask(_name_)


@app.route("/")
def get_instance_id():
    return f"<b style='font-size:30px;color:red;'>Instance ID: {instance_id}</b>"



if _name_ == "_main_":
    app.run(port=5000, host="0.0.0.0")
