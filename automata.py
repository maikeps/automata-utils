#! /usr/bin/python3

class Automaton:

	# An automaton is defined formally by a 5-tuple
	# (states, alphabet, transition function, initial state, accept states)
	def __init__(self, states, alphabet, transition, initial_state, accept_states):
		self.states = states
		self.alphabet = alphabet
		self.transition = transition
		self.initial_state = initial_state
		self.accept_states = accept_states

		self.current_states = [initial_state, ]

	def change_state(self, _input):
		achieved_states = []
		deleted_states = []

		for current_state in self.current_states:
			future_states = self.transition[current_state][_input]
			for state in future_states:
				achieved_states.append(state)

		for state in self.current_states:
			if state not in achieved_states:
				deleted_states.append(state)

		for state in deleted_states:
			del self.current_states[self.current_states.index(state)]

		for state in achieved_states:
			if state not in self.current_states:
				self.current_states.append(state)

		print(self.current_states)

	def check_done(self):
		for state in self.current_states:
			if state in self.accept_states: return True
		return False

	def verify_word(self, word):
		for char in word:
			if char not in self.alphabet:
				return False
			self.change_state(char)
		return self.check_done();

	def determinize(self):
		transition = self.transition
		transition_aux = {}

		for state in transition:
			for _input in transition[state]:
				# Create new state
				new_state = transition[state][_input]

				new_state_str = ""
				
				for aux in new_state:
					new_state_str += aux

				if new_state_str not in transition:
					self.addState(new_state, new_state_str, transition, transition_aux)

		for key in transition_aux:
			transition[key] = transition_aux[key]

		return transition

	def addState(self, new_state_arr, new_state_name, transition, transition_aux):
		# Add the new transition, with empty info
		transition_aux[new_state_name] = {}

		for input_aux in self.alphabet:
			aux = []
			# Get each possible transition from the new state
			# and get the transition from the current input
			for state_aux in new_state_arr: 
				for item in transition[state_aux][input_aux]:
					if item not in aux and transition[state_aux][input_aux] != ['M']:
						aux.append(item)
			transition_aux[new_state_name][input_aux] = aux

		for item in transition_aux[new_state_name]:
			aux_str = ""
			for state in transition_aux[new_state_name][item]:
				aux_str += state
				
			if aux_str not in transition_aux:
				self.addState(transition_aux[new_state_name][item], aux_str, transition, transition_aux)



states = ['q0', 'q1', 'q2', 'M']
alphabet = ['0', '1']
transition = {
	'q0': {'0': ['q0', 'q1'], '1': ['q0']},
	'q1': {'0': ['q2'], '1': ['M']},
	'q2': {'0': ['q2'], '1': ['q2']},
	'M': {'0': ['M'], '1': ['M']}
}
initial_state = 'q0'
accept_states = ['q2']

automaton = Automaton(states, alphabet, transition, initial_state, accept_states);
# print(automaton.verify_word('001010101010111000100000001'))
print(automaton.determinize())