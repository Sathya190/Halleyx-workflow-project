from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

workflows = []
steps = []
rules = []

@app.route("/")
def home():
    return "Halleyx Workflow Project Running"

# -------- WORKFLOWS --------
@app.route("/workflows", methods=["GET"])
def get_workflows():
    return jsonify(workflows)

@app.route("/workflows", methods=["POST"])
def create_workflow():
    data = request.get_json()
    workflow = {"name": data.get("name")}
    workflows.append(workflow)
    return jsonify({"message": "Workflow created"})

# -------- STEPS --------
@app.route("/steps", methods=["GET"])
def get_steps():
    return jsonify(steps)

@app.route("/steps", methods=["POST"])
def create_step():
    data = request.get_json()
    step = {
        "workflow": data.get("workflow"),
        "name": data.get("name")
    }
    steps.append(step)
    return jsonify({"message": "Step created"})

# -------- RULES --------
@app.route("/rules", methods=["GET"])
def get_rules():
    return jsonify(rules)

@app.route("/rules", methods=["POST"])
def create_rule():
    data = request.get_json()
    rule = {
        "step": data.get("step"),
        "condition": data.get("condition"),
        "next_step": data.get("next_step")
    }
    rules.append(rule)
    return jsonify({"message": "Rule created"})

# -------- EXECUTION --------
@app.route("/execute", methods=["POST"])
def execute():
    data = request.get_json()
    workflow_name = data.get("workflow")
    amount = data.get("amount")

    logs = []
    current_step = None

    # first step find
    for s in steps:
        if s["workflow"] == workflow_name:
            current_step = s["name"]
            break

    while current_step:
        logs.append(f"Current Step: {current_step}")

        next_step = None

        for r in rules:
            if r["step"] == current_step:
                if ">" in r["condition"]:
                    value = int(r["condition"].split(">")[1])
                    if amount > value:
                        next_step = r["next_step"]
                        break
                elif "<=" in r["condition"]:
                    value = int(r["condition"].split("<=")[1])
                    if amount <= value:
                        next_step = r["next_step"]
                        break

        if not next_step:
            break

        current_step = next_step

    return jsonify(logs)


if __name__ == "__main__":
    app.run(debug=True)