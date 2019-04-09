
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
        #if volume_value == 2 and outflow_value == 2:
        #    print(state)
        #    print(expected_volume_deriv_value)
        #    print(volume_deriv)
        #if ((inflow_value != 1 or outflow_value != 1) and (expected_volume_deriv_value != volume_deriv)) or (volume_deriv != outflow_deriv):
        if (volume_deriv != outflow_deriv):
            continue

        states.append(state)

    print(len(states))
    for state in states:
        print(state)

    return states
'''
def find_transitions(states):
    states_mapping = {}     #From index in states to state_ID
    states_info = {}             #From state_ID to state info
    transitions = {}     #From state ID to list of state ID
    states_with_origins = set()
    states_with_origins.add(1)

    states.sort(key=lambda tup: tup[1])
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
            if current_index == index:   #state does not transition to itself
                continue

            inflow, volume, outflow = state
            inflow_value, inflow_deriv = inflow
            volume_value, volume_deriv = volume
            outflow_value, outflow_deriv = outflow

            if current_inflow_deriv == 0 and inflow_deriv == 1:
                continue

            #Derivatives should have continuity, thus not 2 steps apart
            inflow_deriv_diff = current_inflow_deriv - inflow_deriv
            volume_deriv_diff = current_volume_deriv - volume_deriv
            outflow_deriv_diff = current_outflow_deriv - outflow_deriv

            if abs(inflow_deriv_diff) == 2 or abs(volume_deriv_diff) == 2 or abs(outflow_deriv_diff) == 2:
                continue

            #See if state precedes the other, checking on quantity value as well as derivative change
            current_inflow_precedes = (min((current_inflow_value + current_inflow_deriv),1) == inflow_value)
            current_volume_precedes = (min(( current_volume_value + current_volume_deriv ),2) == volume_value)
            current_outflow_precedes = (min(( current_outflow_value + current_outflow_deriv),2) == outflow_value)
            #correct_inflow_deriv = current_inflow
            if inflow_value != 1 or outflow_value != 1:
                volume_deriv_shift = max(-1,inflow_value - outflow_value)
                expected_volume_deriv = current_volume_deriv + volume_deriv_shift
                if expected_volume_deriv != volume_deriv or volume_deriv != outflow_deriv:
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

                    #if current_state_ID in states_with_origins:
                    #    states_with_origins.add(other_state_ID)
                #continue

            current_inflow_follows = (min((inflow_deriv + inflow_value), 1) == current_inflow_value)
            current_volume_follows = (min((volume_deriv + volume_value), 2) == current_volume_value)
            current_outflow_follows = (min((outflow_deriv + outflow_value), 2) == current_outflow_value)

            if current_inflow_follows and current_volume_follows and current_outflow_follows:

                # Does not have an state ID yet
                if other_state_ID == -1:
                    states_mapping[index] = state_ID
                    states_info[state_ID] = state
                    other_state_ID = state_ID
                    state_ID += 1

                if current_state_ID == -1:
                    states_mapping[current_index] = state_ID
                    states_info[state_ID] = current_state
                    current_state_ID = state_ID
                    state_ID += 1
                list = transitions.get(other_state_ID, [])
                if current_state_ID not in list:
                    list.append(current_state_ID)
                    transitions[other_state_ID] = list

    print("-" * 100)
    transitions_counter = 0
    for i in transitions.items():
        print(i)
        transitions_counter += len(i[1])
    print(states_info)
    print(len(states_info))
    print(transitions_counter)
    print(len(states_with_origins))
    print(states_with_origins)

    return states_mapping,states_info,transitions#,states_with_origins
'''

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

        if current_inflow_deriv == 0 and inflow_deriv == 1:
            continue

        #Derivatives should have continuity, thus not 2 steps apart
        inflow_deriv_diff = current_inflow_deriv - inflow_deriv
        volume_deriv_diff = current_volume_deriv - volume_deriv
        outflow_deriv_diff = current_outflow_deriv - outflow_deriv

        if abs(inflow_deriv_diff) == 2 or abs(volume_deriv_diff) == 2 or abs(outflow_deriv_diff) == 2:
            continue

        #See if state precedes the other, checking on quantity value as well as derivative change
        current_inflow_precedes = (min((current_inflow_value + current_inflow_deriv),1) == inflow_value)
        current_volume_precedes = (min(( current_volume_value + current_volume_deriv ),2) == volume_value)
        current_outflow_precedes = (min(( current_outflow_value + current_outflow_deriv),2) == outflow_value)
        #correct_inflow_deriv = current_inflow
        if inflow_value != 1 or outflow_value != 1:
            volume_deriv_shift = max(-1,inflow_value - outflow_value)
            expected_volume_deriv = current_volume_deriv + volume_deriv_shift
            if expected_volume_deriv != volume_deriv or volume_deriv != outflow_deriv:
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
                print("test")
                states_mapping, states_info, transitions = find_transitions(states, index, state_ID, states_mapping, states_info, transitions)
                    #if current_state_ID in states_with_origins:
                    #    states_with_origins.add(other_state_ID)
                #continue
            '''
            current_inflow_follows = (min((inflow_deriv + inflow_value), 1) == current_inflow_value)
            current_volume_follows = (min((volume_deriv + volume_value), 2) == current_volume_value)
            current_outflow_follows = (min((outflow_deriv + outflow_value), 2) == current_outflow_value)

            if current_inflow_follows and current_volume_follows and current_outflow_follows:

                # Does not have an state ID yet
                if other_state_ID == -1:
                    states_mapping[index] = state_ID
                    states_info[state_ID] = state
                    other_state_ID = state_ID
                    state_ID += 1

                if current_state_ID == -1:
                    states_mapping[current_index] = state_ID
                    states_info[state_ID] = current_state
                    current_state_ID = state_ID
                    state_ID += 1
                list = transitions.get(other_state_ID, [])
                if current_state_ID not in list:
                    list.append(current_state_ID)
                    transitions[other_state_ID] = list
                '''
    print("-" * 100)
    transitions_counter = 0
    for i in transitions.items():
        print(i)
        transitions_counter += len(i[1])
    print(states_info)
    print(len(states_info))
    print(transitions_counter)
    #print(len(states_with_origins))
    #print(states_with_origins)

    return states_mapping,states_info,transitions#,states_with_origins
def create_graph(states,transitions):
    dot = Digraph(comment='The container system')

    for state_ID,info in states.items():
        string_ID = str(state_ID)
        text = "State: " + string_ID + "\nInflow " + str(info[0]) + "\nVolume " + str(info[1]) + "\n Outflow " + str(info[2])
        dot.node(string_ID, text)

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



if __name__ == "__main__":
    all_states = generate_states()
    states = reduce_states(all_states)
    states_mapping, states, transitions = find_transitions(states)
    create_graph(states,transitions)
