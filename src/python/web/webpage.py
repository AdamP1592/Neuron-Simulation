from flask import Flask
import sim

no_cur = sim.input_currents.input_current()
square_cur = sim.input_currents.square_current()
sin_cur = sim.input_currents.sin_current()


app = Flask(__name__)

@app.route("/")
def home():

    return "test"
@app.route("/id/<id>", methods=['GET', 'POST'])
def get_next_sim_batch(id, variable):
    return str(id), variable

def set_current(neuron_sim, v):


if __name__ == "__main__":
    inputs = [no_cur, sin_cur, square_cur]
    dt = 0.01
    neuron_sim = sim.simulation(dt)

#neuron_sim_webpage.py