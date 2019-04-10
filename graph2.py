
from graphviz import Digraph

import itertools

def generate_states():

    # Inflow has [0,+] value
    # Volume has [0,+,max] value
    # Outflow has [0,+,max] value
    # Derivatives has [-,0,+]
    inflow_values = [0,1]
    volume_outflow_values = [0,1,2]
    derivatives = [-1,0,1]
    inflow_tuples = list(itertools.product(inflow_values,derivatives))
    volume_outflow_tuples = list(itertools.product(volume_outflow_values, derivatives))
    all_states = list(itertools.product(inflow_tuples, volume_outflow_tuples,volume_outflow_tuples))

    print(inflow_tuples)
    print(volume_outflow_tuples)
    print(all_states)
    print("#Number of all states: ",len(all_states))
    #for i in all_states:
    #    print(i)

    return all_states

def reduce_states(all_states):

    #Assumptions
    #Constraints check such as value correspondence
    #Derivative check
    states = []

    for state in all_states:
        inflow, volume, outflow = state
        inflow_value,inflow_deriv = inflow
        volume_value, volume_deriv = volume
        outflow_value, outflow_deriv = outflow

        # Zero cannot have negative derivative constraint/assumption
        if (inflow_value == 0 and inflow_deriv == -1) or (volume_value == 0 and volume_deriv == -1) or (outflow_value == 0 and outflow_deriv == -1):
            continue
        #Value correspondence for zero and max between volume and outflow, thus in a way also for the plus, all value correspondence
        elif volume_value != outflow_value:
            continue

        # Derivative check, start with inflow and outvalue value that determine volume derivative, which inturn determines outflow derivative
        expected_volume_deriv_value = max(-1,inflow_value - outflow_value) #Making sure not -2
        #if volume_value == 2 and outflow_value == 2:
        #    print(state)
        #    print(expected_volume_deriv_value)
        #    print(volume_deriv)
        #if ((inflow_value != 1 or outflow_value != 1) and (expected_volume_deriv_value != volume_deriv)) or (volume_deriv != outflow_deriv):

        #Since outflow derivative is proportional to volume deriv and there is value correspondence, the derivative of the two follows the same directions
        if (volume_deriv != outflow_deriv):
            continue

        states.append(state)

    print("#Number of possible states: ",len(states))
    for state in states:
        print(state)

    return states

def find_transitions(states,current_index=0,state_ID=1,states_mapping={},states_info={},transitions={}):
    #states_mapping = {}     #From index in states to state_ID
    #states_info = {}             #From state_ID to state info
    #transitions = {}     #From state ID to list of state ID
    #states_with_origins = set()
    #states_with_origins.add(1)

    #states.sort(key=lambda tup: tup[1])
    #state_ID = 1

    current_state = states[current_index]

    current_inflow, current_volume, current_outflow = current_state
    current_inflow_value,current_inflow_deriv = current_inflow
    current_volume_value, current_volume_deriv = current_volume
    current_outflow_value, current_outflow_deriv = current_outflow
        #initial state
        #if current_index == 0:
            #states_mapping[current_index] = state_ID
            #states[state_ID] = current_state
            #state_ID += 1

    for index,state in enumerate(states):
        if current_index == index:   #state does not transition to itself
            continue

        inflow, volume, outflow = state
        inflow_value, inflow_deriv = inflow
        volume_value, volume_deriv = volume
        outflow_value, outflow_deriv = outflow

        #if current_index != 0 and current_inflow_deriv == 0 and inflow_deriv == 1:
        #    continue

        #print("-"*100)
        #print(state)

        #Derivatives should have continuity, thus not 2 steps apart
        inflow_deriv_diff = current_inflow_deriv - inflow_deriv
        volume_deriv_diff = current_volume_deriv - volume_deriv
        outflow_deriv_diff = current_outflow_deriv - outflow_deriv

        if abs(inflow_deriv_diff) == 2 or abs(volume_deriv_diff) == 2 or abs(outflow_deriv_diff) == 2:
            continue

        #See if state precedes the other, checking on quantity value shift first then the derivative change as well
        current_inflow_precedes = (min((current_inflow_value + current_inflow_deriv),1) == inflow_value)
        current_volume_precedes = (min(( current_volume_value + current_volume_deriv ),2) == volume_value)
        current_outflow_precedes = (min(( current_outflow_value + current_outflow_deriv),2) == outflow_value)
        #correct_inflow_deriv = current_inflow

        #When inflow is 1 and outflow is 1, it is ambigous, thus allow for all cases, which are where deriv is negative, zero or positive due to
        # Inflow quantity being negative, equal or greater than outflow.
        if inflow_value != 1 or outflow_value != 1:
            volume_deriv_shift = max(-1,inflow_value - outflow_value)
            expected_volume_deriv = current_volume_deriv + volume_deriv_shift
            if expected_volume_deriv != volume_deriv:
                continue
            #correct_outflow_deriv =

        current_state_ID = states_mapping.get(current_index, -1)
        other_state_ID = states_mapping.get(index, -1)
        if current_inflow_precedes and current_volume_precedes and current_outflow_precedes:

        # Does not have an state ID yet
            if current_state_ID == -1:
                states_mapping[current_index] = state_ID
                states_info[state_ID] = current_state
                current_state_ID = state_ID
                state_ID += 1

            if other_state_ID== -1:
                states_mapping[index] = state_ID
                states_info[state_ID] = state
                #other_state_ID = state_ID + 1
                other_state_ID = state_ID
                state_ID += 1

            list = transitions.get(current_state_ID,[])
            if other_state_ID not in list:
                list.append(other_state_ID)
                transitions[current_state_ID] = list
                states_mapping, states_info, transitions = find_transitions(states, index, state_ID, states_mapping, states_info, transitions)

    return states_mapping,states_info,transitions#,states_with_origins
def create_graph(states,transitions):
    dot = Digraph(comment='The container system')

    for state_ID,info in states.items():
        string_ID = str(state_ID)
        text = "State: " + string_ID + "\nInflow " + str(info[0]) + "\nVolume " + str(info[1]) + "\n Outflow " + str(info[2])
        dot.node(string_ID, text)#,shape="Box")

        transitions_list = transitions.get(state_ID,[])
        for trans_state_ID in transitions_list:
            dot.edge(string_ID, str(trans_state_ID))

    #dot.node('A', 'King Arthur')
    #dot.node('B', 'Sir Bedevere the Wise')
    #dot.node('L', 'Sir Lancelot')
    #dot.edges(['AB', 'AL'])

    #dot.edge('B', 'L', constraint='false')
    #print(dot.source)

    dot.render('./container_system_test.gv', view=True)

def give_trace(state_1,state_2=None):
    inflow,volume,outflow  = state_1
    inflow_value, inflow_deriv = inflow
    volume_value, volume_deriv = volume
    outflow_value, outflow_deriv = outflow

    if inflow_value == 0 and inflow_deriv == 0:
        inflow_text = "no inflow and it remains consistent like this"
        inflow_deduction = "the tap remains closed."
    elif inflow_value == 0 and inflow_deriv == 1:
        inflow_text = "no inflow, but the inflow is starting to increase"
        inflow_deduction = "the tap is turning on."
    elif inflow_value == 1 and inflow_deriv == 0:
        inflow_text = "a steady inflow."
        inflow_deduction = "the tap remains open as it is."
    elif inflow_value == 1 and inflow_deriv == 1:
        inflow_text = "is an inflow that is starting to increase"
        inflow_deduction = "the tap is opened further."
    elif inflow_value == 1 and inflow_deriv == -1:
        inflow_text = "is an inflow that is starting to decrease"
        inflow_deduction = "the tap is closing."

    if volume_value == 0:
        volume_value_text = "no"
    elif volume_value == 1:
        volume_value_text = "some"
    else:
        volume_value_text = "maximium amount of"

    if volume_deriv == 0:
        volume_deriv_text = "remains stable"
    elif volume_deriv == 1:
        volume_deriv_text = "is increasing"
    else:
        volume_deriv_text = "is decreasing"

    if outflow_value == 0 and outflow_deriv == 0:
        outflow_value_text = "no"
        outflow_deriv_text =  "There is " + outflow_value_text  + " outflow of the drain and remains stable. "
    elif outflow_value == 0 and outflow_deriv == 1:
        outflow_value_text = "no"
        outflow_deriv_text = "There is " + outflow_value_text  + " outflow of the drain, but there will be some outflow soon as some water will arrive at the container. "
    elif outflow_value == 1 and outflow_deriv == 0:
        outflow_value_text = "some"
        outflow_deriv_text = "There is " + outflow_value_text  + " outflow of the drain that remains stable. "
    elif outflow_value == 1 and outflow_deriv == 1:
        outflow_value_text = "some"
        outflow_deriv_text = "This is due to " + outflow_value_text + " outflow of the drain, which will increase to maximium amount of outflow as the container volume reaches it maximium as well. The inflow in this case is greater than the outflow"
    elif outflow_value == 1 and outflow_deriv == -1:
        outflow_value_text = "some"
        outflow_deriv_text = "There is " + outflow_value_text + " outflow, which is decreasing as the water in container is decreasing as well. The outflow is greater than the inflow in this case."
    elif outflow_value == 2 and outflow_deriv == 0:
        outflow_value_text = "the maximium amount of"
        outflow_deriv_text = "This is due to " + outflow_value_text + " outflow of the drain that remains stable for a moment as the maximium outflow is greater than the inflow and will prevent the contaner from overflowing "
    elif outflow_value == 2 and outflow_deriv == -1:
        outflow_value_text = "the maximium amount of"
        outflow_deriv_text = "This is due to " + outflow_value_text + " outflow of the drain, which is greater than the inflow and decreases the amount of volume in the container"

    print(state_1)

    #Intra state
    if state_2 == None:
        full_text = ("Currently at this state, there is " + inflow_text + " as " + inflow_deduction
                     + " Furthermore, there is " + volume_value_text + " water in the container to which the amount " + volume_deriv_text +
                     " as a result of the combination of inflow and the outflow. " + outflow_deriv_text)
    #Inter state, where state_1 is predecessor of state_2
    else:
        inflow2, volume2, outflow2 = state_2
        inflow_value2, inflow_deriv2 = inflow2
        volume_value2, volume_deriv2 = volume2
        outflow_value2, outflow_deriv2 = outflow2

        if inflow_value2 == 0 and inflow_deriv2 == 0:
            inflow2_text = " there is no inflow and the tap is and remains closed. "
        elif inflow_value2 == 0 and inflow_deriv2 == 1:
            inflow2_text = " there is no inflow, but the tap is turning on. "
        elif inflow_value2 == 1 and inflow_deriv2 == 0:
            inflow2_text = " there is a inflow that is steady as the tap remains open as it is. "
            if inflow_value == 1 and inflow_deriv == 1:
                inflow2_text = " there is still inflow, but the tap is not turned open any further and becomes a steady inflow. "
        elif inflow_value2 == 1 and inflow_deriv2 == 1:
            inflow2_text = ", there is an inflow that is starting to increase as the tap is opened further. "
        elif inflow_value2 == 1 and inflow_deriv2 == -1:
            inflow2_text = " the inflow is starting to decrease as the tap is closing. "

        inflow_vs_outflow = max(-1, inflow_value2 - outflow_value2)

        if inflow_vs_outflow == 0 and volume_deriv == 0:
            inflow_vs_outflow_text = "the inflow is equal to the outflow"
        elif inflow_vs_outflow == 0 and volume_deriv == 1:
            inflow_vs_outflow_text = "the inflow is greater than the outflow"
        elif inflow_vs_outflow == 0 and volume_deriv == -1:
            inflow_vs_outflow_text = "the outflow is greater than the inflow"
        elif inflow_vs_outflow == 1:
            inflow_vs_outflow_text = "the inflow is greater than the outflow"
        elif inflow_vs_outflow== -1:
            inflow_vs_outflow_text = "the outflow is greater than the inflow"

        volume_deriv_shift = volume_deriv2 - volume_deriv

        if volume_deriv_shift == 0:
            volume_deriv_shift_text = " remains the same"
        elif volume_deriv_shift == 1:
            volume_deriv_shift_text = "is increasing"
        elif volume_deriv_shift == -1:
            volume_deriv_shift_text = "is decreasing"

        if volume_value2 == 0:
            volume_value_text2 = "no"
        elif volume_value2 == 1:
            volume_value_text2 = "some"
        else:
            volume_value_text2 = "maximium amount of"

        if volume_deriv2 == 0:
            volume_deriv_text2 = "remains stable. "
        elif volume_deriv2 == 1:
            volume_deriv_text2 = "is increasing. "
        else:
            volume_deriv_text2 = "is decreasing. "

        if volume_deriv == 0:
            volume_deriv_deduction_text2 = "stable and now "
        elif volume_deriv == 1:
            volume_deriv_deduction_text2 = "was increasing and now "
        elif volume_deriv == -1:
            volume_deriv_deduction_text2 = "was decreasing and now "

        volume_deriv_deduction_text2 += inflow_vs_outflow_text + ", which results into a volume that " + volume_deriv_shift_text + " compared to the previous state. "

        if outflow_value2 == 0 and outflow_deriv2 == 0:
            outflow_value_text2 = "no"
            outflow_deriv_text2 = "there is " + outflow_value_text + " outflow of the drain and remains stable. "
        elif outflow_value2 == 0 and outflow_deriv2 == 1:
            outflow_value_text2 = "no"
            outflow_deriv_text2 = "there is " + outflow_value_text + " outflow of the drain, but there will be some outflow soon as some water will arrive at the container. "
        elif outflow_value2 == 1 and outflow_deriv2 == 0:
            outflow_value_text2 = "some"
            outflow_deriv_text2 = "there is " + outflow_value_text + " outflow of the drain that remains stable. "
        elif outflow_value2 == 1 and outflow_deriv2 == 1:
            outflow_value_text2 = "some"
            outflow_deriv_text2 = "there is " + outflow_value_text + " outflow of the drain, which will increase to maximium amount of outflow as the container volume reaches it maximium as well. The inflow in this case is greater than the outflow. "
        elif outflow_value2 == 1 and outflow_deriv2 == -1:
            outflow_value_text2 = "some"
            outflow_deriv_text2 = "there is " + outflow_value_text + " outflow, which is decreasing as the water in container is decreasing as well. The outflow is greater than the inflow in this case."
        elif outflow_value2 == 2 and outflow_deriv2 == 0:
            outflow_value_text2 = "the maximium amount of"
            outflow_deriv_text2 = "there is " + outflow_value_text + " outflow of the drain that remains stable for a moment as the maximium outflow is greater than the inflow and will prevent the contaner from overflowing. "
        elif outflow_value2 == 2 and outflow_deriv2 == -1:
            outflow_value_text2 = "the maximium amount of"
            outflow_deriv_text2 = "there is " + outflow_value_text + " outflow of the drain, which is greater than the inflow and decreases the amount of volume in the container. "

        print(state_2)

        full_text = ("At the predecessor state, there is " + inflow_text + " as " + inflow_deduction +
                     " Furthermore, there is " + volume_value_text + " water in the container to which the amount " + volume_deriv_text + "."
                      + outflow_deriv_text
                      + "With the transition to the next state," + inflow2_text
                     + "Also, due to the combination of inflow and the outflow of the previous state, there is "  + volume_value_text2
                     + " water in the container in the succesor state to which te amount " + volume_deriv_text2 +
                     "This is because in the previous state the volume was " + volume_deriv_deduction_text2
                     + "The outflow changes proportionally to the volume as well, " + outflow_deriv_text2 )
    print(full_text)

#def give_inter_state(pred_state,succesor_state):


if __name__ == "__main__":
    all_states = generate_states()
    states = reduce_states(all_states)
    states_mapping, states, transitions = find_transitions(states)
    create_graph(states,transitions)

    print("-" * 100)
    transitions_counter = 0
    for i in transitions.items():
        print(i)
        transitions_counter += len(i[1])
    print(states)
    print("Final amount of states: ",len(states))
    print("Amount of transitions: ",transitions_counter)
    #print(len(states_with_origins))
    #print(states_with_origins)
    for state_ID,state in states.items():
        give_trace(state)
    for state_ID,list in transitions.items():
        state_1 = states[state_ID]
        for state_ID2 in list:
            state_2 = states[state_ID2]
            give_trace(state_1,state_2)
    #give_intra_state(states[1])