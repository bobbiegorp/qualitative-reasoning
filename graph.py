"""
from graphviz import Digraph

dot = Digraph(comment='The Round Table')
dot.node('A', 'King Arthur')
dot.node('B', 'Sir Bedevere the Wise')
dot.node('L', 'Sir Lancelot')
dot.edges(['AB', 'AL'])

dot.edge('B', 'L', constraint='false')
print(dot.source)

dot.render('./round-table.gv', view=True)
"""
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
    print(len(all_states))
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

        # Zero cannot have negative derivative assumption
        if (inflow_value == 0 and inflow_deriv == -1) or (volume_value == 0 and volume_deriv == -1) or (outflow_value == 0 and outflow_deriv == -1):
            continue
        #Value correspondence
        elif volume_value != outflow_value:
            continue

        # Derivative check, start with inflow and outvalue value that determine volume derivative, which inturn determines outflow derivative
        expected_volume_deriv_value = max(-1,inflow_value - outflow_value) #Making sure not -2
        if (inflow_value != 1 and outflow_value != 1 and (expected_volume_deriv_value != volume_deriv)) or (volume_deriv != outflow_deriv):
            continue

        states.append(state)

    print(len(states))
    for state in states:
        print(state)

    return states

def find_transitions(states):
    states_mapping = {}     #From index in states to state_ID
    states = {}             #From state_ID to state info
    transitions = set()     #From state ID to state ID
    #state_have_transitions = set()

    state_ID = 1

    for current_index,current_state in enumerate(states):
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
            inflow, volume, outflow = state
            inflow_value, inflow_deriv = inflow
            volume_value, volume_deriv = volume
            outflow_value, outflow_deriv = outflow

            #Derivatives should have continuity, thus not 2 steps apart
            inflow_deriv_diff = current_inflow_deriv - inflow_deriv
            volume_deriv_diff = current_volume_deriv - volume_deriv
            outflow_deriv_diff = current_outflow_deriv - outflow_deriv
            if abs(inflow_deriv_diff) == 2 or abs(volume_deriv_diff) == 2 or abs(outflow_deriv_diff) == 2:
                continue

            #See which state precedes the other
            current_inflow_precedes = ((current_inflow_deriv + current_inflow_value) == inflow_value)
            current_volume_precedes = ((current_volume_deriv + current_volume_value) == volume_value)
            current_outflow_precedes = ((current_outflow_deriv + current_outflow_value) == outflow_value)
            if current_inflow_precedes and current_volume_precedes and current_outflow_precedes:

                #Does not have and state ID yet
                if states_mapping.get(current_index,0) == 0
                    states_mapping[current_index] = state_ID
                    states[state_ID] = current_state
                    state_ID += 1
                    states_mapping[index] = state_ID
                    states[state_ID] = state
                    state_ID += 1
                    transitions.add(state_ID-2,state_ID-1)
            elif not(current_inflow_precedes and current_volume_precedes and current_outflow_precedes):
                #

            #current_index != index   state does not transition to itself

if __name__ == "__main__":
    all_states = generate_states()
    states = reduce_states(all_states)
    #states = find_transitions(states)
