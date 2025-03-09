current_input_type = [0] #has to be mutable 
current_types = {}
currents = []
current_names = []

sliders = [] #storage for sliders so they dont become garbage


def on_close(event):
        exit()

#setup array of currents 
def get_action_potential_threshold(sim):
    from input_currents import constant_current
    from input_currents import input_current
    # The dictionary is defined but not used in this version,
    # because we use arithmetic (exponentiation) for sign flipping.
    add_sub_switch = {1: -1, -1: 1}
    add_sub = -1

    action_thresh_step = 10.0  # initial current adjustment step
    
    curr = constant_current(3)
    no_curr = input_current()

    # Start with the resting potential as the initial threshold guess.
    thresh = sim.model.resting_potential

    sim.set_input_current(curr.get_current)

    # Run a preliminary simulation to determine max voltage (used for spike criterion)
    for _ in range(int(15/sim.dt)):
        sim.iterate()

    max_v = max(sim.v)
    possible_range = max_v - sim.model.resting_potential
    deviation = 0.1
    modifier = possible_range * deviation
    modified_max = max_v - modifier  # voltage threshold to consider a spike

    sim.clear()
    print(sim.input_current_func(0))
    previous_spike_thresh = sim.model.resting_potential
    iteration_count = 2  # used to alternate adjustment direction

    # Continue adjusting the threshold until the step size is sufficiently small
    while action_thresh_step >= 0.001:
        # Iterate 5 seconds with current injection at the current threshold level.
        sim.set_input_current(curr.get_current)

        for _ in range(int(5/sim.dt)):
            sim.iterate()
            # If the voltage exceeds the threshold, remove current by switching input.
            if sim.model.v >= thresh:
                sim.set_input_current(no_curr.get_current)

        # Use the last 5 seconds of simulation values to determine max voltage.
        vs = sim.v[-int(5/sim.dt):]
        v_max = max(vs)

        # If a spike occurred (voltage reached modified_max), store the threshold.
        if v_max >= modified_max and iteration_count % 2 == 0:
            previous_spike_thresh = thresh
            # Flip the adjustment direction by incrementing iteration_count.
            iteration_count += 1
             # Halve the adjustment step for finer resolution.
            action_thresh_step /= 2.0

            
        elif iteration_count % 2 == 1:
            # No spike: also increment iteration_count to flip the adjustment direction.
            iteration_count += 1
            

        # Update the threshold using the alternating sign:
        
        thresh += action_thresh_step * (add_sub ** iteration_count)
        sim.clear()
    return thresh
    

def setup_currents():
    #plan to swap out hard coded input currents with inspect.isclass
    import input_currents
    freq, current = 0, 0
    currents.append(input_currents.input_current())
    currents.append(input_currents.sin_current([freq, current]))
    currents.append(input_currents.square_current([freq, current]))
    
    for i in range(len(currents)):
        current_name = str(currents[i])

        #setting up dict to keep track of all the current types, and the indexes they are at
        current_names.append(current_name)
def set_params(val, label, pos):
    if "current" in label : 
        currents[pos].set_amplitude(val)
    else:
        currents[pos].set_frequency(val)
    neuron_sim.set_input_current(currents[pos].get_current)
def set_current_type(current_type_str, slider_axes):
    #when set current is called 1: input_current in neuron_sim is set 2: text boxes for the required params are created
    
    #set the current input index
    pos = current_names.index(current_type_str)
    current_input_type[0] = pos

    #set new input function in sim
    current = currents[pos]
    neuron_sim.set_input_current(currents[pos].get_current)
    textbox_labels = currents[pos].needed_params
    #creates new sliders for the input parameters

    for i in slider_axes:
        i.clear()
        i.set_axis_off()
  

    sliders.clear()

    #I have no idea why but any time I tried to use a normal loop the
    #values passed by the function would be overwritten
    def recursive_slider_builder(textbox_labels, i):
        def set_input_params(val):
            #no idea why the index needs to be shifted back when calling
            #i with the event when it builds everything with i
            j = i - 1
            set_params(float(val), textbox_labels[j], pos)
        if i >= len(textbox_labels):
            return
        
        current_param_limits = current.param_value_ranges[i]

        slider = Slider(slider_axes[i], textbox_labels[i], current_param_limits[0], current_param_limits[1], 0)
        slider.on_changed(set_input_params)
        
        #any inputs will be trashed if not stored
        sliders.append(slider)
        i += 1
        recursive_slider_builder(textbox_labels, i)
        
    recursive_slider_builder(textbox_labels, 0)
        
        
    print(sliders)
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from matplotlib.widgets import RadioButtons, Slider

    from simulation import simulation

    #sim setup
    dt = 0.01
    neuron_sim = simulation(dt)

    apt = get_action_potential_threshold(neuron_sim)
    neuron_sim.model.action_potential_threshold = apt
    setup_currents()
    
    #plot setup
    plt.ion()
    plt.show()




    ######### need adjusttable subplot mosaic for input values
    fig, ax_dict = plt.subplot_mosaic("""
                                AAADD
                                AAADD
                                BBBDD
                                BBBDD
                                CCCFF
                                CCCGG
                                """)
    

 

    
    #axs setup, want to make dynamically generated in future

    
    ax0 = ax_dict["A"] #membrane potential graph
    ax1 = ax_dict["B"] #gating potential graph
    ax2 = ax_dict["C"] #current graph
    ax3 = ax_dict["D"] #input_currents

    slider_axes = [ax_dict["F"], ax_dict["G"]]

    for i in slider_axes:
        i.set_axis_off()

    #screenshot and excape cases
    def on_press(event):
        import sys
        #clear event
        sys.stdout.flush()

        #why are you like this
        if(event.key == " "):
            from pathlib import Path
            #savefig chooses to save two parent folders up, so set path directly
            p = Path("simulation.py")
            #current input type =  
            fig.savefig("{}/demo/{}.png".format(str(p.parent.absolute()), current_names[current_input_type[0]]))
            print("saved")
        if event.key=="escape":
            exit()

    #some styling
    fig.tight_layout()
    fig.set_size_inches(18,6)

    #escape cases
    fig.canvas.mpl_connect('key_press_event', on_press)
    fig.canvas.mpl_connect('close_event', on_close)

    #setup for radio buttons
    current_radio_buttons = RadioButtons(ax3, current_names)
    current_radio_buttons.on_clicked(lambda current_name: set_current_type(current_name, slider_axes))

    #could not update y_data and still reload the graph, so this is what you get
    #no idea why
    i = 0
    while(i < 10000):
        #clears data points
        ax0.cla()
        ax1.cla()
        ax1.cla()
        ax2.cla()
        #resets lables after being cleared
        ax0.set_ylabel("Potential(mv)")
        ax1.set_ylabel("Activation")
        ax2.set_ylabel("Current (µA/cm²)")
        
        #redraw after every 10 steps
        for j in range(50):
            neuron_sim.iterate()

        #limit how many datapoints can be seen at once time
        num_datapoints = len(neuron_sim.times)
        past_range = 6000

        if num_datapoints < past_range:
            past_range = num_datapoints
       
        
        #plots data
        x = neuron_sim.times[num_datapoints - past_range:]

        ax0.plot(x, neuron_sim.v[num_datapoints - past_range:])

        ax1.plot(x, neuron_sim.m[num_datapoints - past_range:])
        ax1.plot(x, neuron_sim.n[num_datapoints - past_range:])
        ax1.plot(x, neuron_sim.h[num_datapoints - past_range:])

        ax2.plot(x, neuron_sim.input_currents[num_datapoints - past_range:])
        plt.draw()

        plt.pause(0.005)
    

        i+=1
    plt.close()