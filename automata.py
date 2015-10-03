import copy
import re

class Automaton:
	"""
	An automaton is defined formally by a 5-tuple
	(states, alphabet, transition function, initial state, accept states)
	"""

	def __init__(self, states, alphabet, transition, initial_state, accept_states):
		self.states = states
		self.alphabet = alphabet
		self.transition = transition
		self.initial_state = initial_state
		self.accept_states = accept_states

		self.current_states = [initial_state]

	def __str__(self):
		string = ""
		# Initial State:
		string += "Initial State: "
		string += "\t"+self.initial_state+"\n"

		# Accept States
		string += "Accept States: "
		string += "\t{"
		for i in range(len(self.accept_states)-1):
			string += self.accept_states[i]+", "
		try:
			string += self.accept_states[-1]+"}\n"
		except IndexError:
			string += "}\n"

		# Alphabet
		string += "Alphabet: "
		string += "\t{"
		for i in range(len(self.alphabet)-1):
			string += self.alphabet[i]+", "
		try:
			string += self.alphabet[-1]+"}\n"
		except IndexError:
			string += "}\n"

		# States
		string += "States: "
		string += "\t{"
		for i in range(len(self.states)-1):
			string += self.states[i]+", "
		string += self.states[-1]+"}\n"

		# Transition table
		string += "Transition table:\n"
		for key in self.transition:
			for transition in self.transition[key]:
				if key is not 'M' and key is not 'F':
					string += "\t("+key+", "+transition+") -> "
					for i in range(len(self.transition[key][transition])-1):
						item = self.transition[key][transition][i]
						string += item+" | "
					string += self.transition[key][transition][-1]+"\n"


		return string

	def __or__(self, other):
		return self.union(other)

	def __add__(self, other):
		return self.concat(other)

	def change_state(self, current_states, _input):
		"""
		Given the current states and an input,
		update the current states of the automaton
		"""

		achieved_states = []
		deleted_states = []

		# current_states = self.epsilon(current_states)

		for current_state in current_states:
			try:
				future_states = self.transition[current_state][_input]
			except KeyError:
				future_states = [current_state]
			for state in future_states:
				achieved_states.append(state)

		for state in current_states:
			if state not in achieved_states:
				deleted_states.append(state)

		for state in deleted_states:
			del current_states[current_states.index(state)]

		for state in achieved_states:
			if state not in current_states:
				current_states.append(state)

		self.current_states = current_states

		return current_states

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
		"""
		Determinizes the automaton
		"""

		new_transition = {}
		
		# Calculates the epsilon closure for the initial state
		initial_closure = self.epsilon(self.initial_state)

		# Adds the calculated closure to the new transition table
		# Note: add_state is responsible for adding the remaining states
		self.add_state(initial_closure, self.transition, new_transition)

		# Sets the remaining variables to form an Automaton
		new_states = [key for key in new_transition]
		
		# Build the accept states array
		new_accept_states = []
		for state in new_transition:
			for final_state in self.accept_states:
				if final_state in state and state not in new_accept_states:
					new_accept_states.append(state)

		# Create and return the automaton
		return Automaton(new_states, self.alphabet,	new_transition,	''.join(sorted(initial_closure)), new_accept_states)

	def epsilon(self, state):
		"""
		Given a state, find its epsilon closure
		"""

		closure = [state]

		states_aux = [state];

		while True:
			count = 0
			next_states = []

			# For each state in the auxiliary states array
			for state_aux in states_aux:
				# Gets the epsilon transition as a list of states
				next_states = self.change_state([state_aux], '&')

				# For each state in this list, check if it's already visited
				# If not, add a counter and add the state to the closure list
				for next_state in next_states:
					if next_state not in closure and next_state is not 'M':
						count += 1
						closure.append(next_state)
			
			# Sets the auxiliary states list with the contents
			# Of the epsilon transition
			states_aux = next_states

			# If the countes is 0, then no new state has been reached
			# By epsilon transitions, and the closure is found
			if count == 0:
				return closure

	def add_state(self, new_state_arr, transition, new_transition):
		"""
		Adds recursively a new state to the new transition
		Based on the existing transition
		"""

		# Creates a name for the new state
		new_state_arr = sorted(new_state_arr)
		new_state_name = ''.join(new_state_arr)

		# Add the new transition with empty info
		new_transition[new_state_name] = {}

		# For each element in the alphabet
		for input_aux in self.alphabet:
			aux = []
			# Get each possible transition from the new state
			# and get the transition from the current input
			for state_aux in new_state_arr:
				try:
					for item in transition[state_aux][input_aux]:

						if item not in aux and transition[state_aux][input_aux] != ['M']:
							aux = list(set(aux) | set(self.epsilon(item)))
				except:
					pass
			
			# Add the dead state	
			if aux == []:
				aux = ['M']


			# Fills the transition table with the newly found state
			sort = sorted(aux)
			name = ''.join(sort)
			new_transition[new_state_name][input_aux] = [name]

			# If it's a non existin state in the transition, adds it
			if name not in new_transition:
				self.add_state(sort, transition, new_transition)

	def union(self, other):
		"""
		Generates the union between this and the other automaton.
		"""
		self_deterministic = self.determinize()
		self_transition = copy.deepcopy(self_deterministic.transition)
		other_deterministic = other.determinize()
		other_transition = copy.deepcopy(other_deterministic.transition)

		new_transition = {}
		new_initial_state = 'qi'
		new_accept_states = ['qf']
		new_alphabet = list(set(self_deterministic.alphabet) | set(other_deterministic.alphabet))

		name_map = {}

		# Rename states in other automaton to prevent name conflicts
		for state in other_transition:
			new_name = state
			count = 1
			while new_name == state:
				new_name = state+str(count)
				count += 1
			name_map[state] = new_name

		new_transition['qi'] = {}
		new_transition['qi'] = {'&': [self_deterministic.initial_state, name_map[other_deterministic.initial_state]]}

		# Add self transitions to the new transition table
		for state in self_transition:
			if state is not 'M':
				new_transition[state] = {}
				for char in self_transition[state]:
					new_transition[state][char] = self_transition[state][char]

		# Add other transitions to the new transition table
		for state in other_transition:
			if state is not 'M':
				new_transition[name_map[state]] = {}
				for char in other_transition[state]:
					new_transition[name_map[state]][char] = [name_map[other_transition[state][char][0]]]

		# Add dead and final states
		new_transition['M'] = {}
		new_transition['qf'] = {}
		for char in new_alphabet:
			new_transition['M'][char] = ['M']
			new_transition['qf'][char] = ['M']

		# Add missing transitions
		for state in new_transition:
			for char in new_alphabet:
				if char not in new_transition[state]:
					new_transition[state][char] = ['M']

		# Add accept state transition
		for state in self_transition:
			if state in self_deterministic.accept_states:
				new_transition[state]['&'] = ['qf']
		for state in other_transition:
			if state in other_deterministic.accept_states:
				new_transition[name_map[state]]['&'] = ['qf']


		new_states = [state for state in new_transition]

		union_automaton = Automaton(new_states, new_alphabet, new_transition, new_initial_state, new_accept_states)
		return union_automaton.determinize().beautify()

	def concat(self, other):
		"""
		Generates the concatenation between this and the other automaton.
		"""
		self_deterministic = self.determinize()
		other_deterministic = other.determinize()

		self_transition = copy.deepcopy(self_deterministic.transition)
		other_transition = copy.deepcopy(other_deterministic.transition)

		new_alphabet = list(set(self_deterministic.alphabet) | set(other_deterministic.alphabet))
		new_initial_state = self_deterministic.initial_state

		new_transition = {}
		name_map = {}

		# Create transition table for the first automaton
		for key in self_transition:
			if key is not 'M':
				new_transition[key] = {}
				for char in new_alphabet:
					if char in self_transition[key]:
						new_transition[key][char] = self_transition[key][char]
					else:
						new_transition[key][char] = ['M']

		# Create transition table for the second automaton
		for key in other_transition:
			if key is not 'M':
				state = key
				i = 1
				while state in new_transition:
					state = key+str(i)
					i += 1

				name_map[key] = state

				new_transition[state] = {}
				for char in new_alphabet:
					if char in other_transition[key]:
						new_transition[state][char] = other_transition[key][char]
					else:
						new_transition[state][char] = ['M']


		# Update names in case of duplicates
		for key in other_transition:
			for char in other_transition[key]:
				for i in range(len(other_transition[key][char])):
					item = other_transition[key][char][i]
					if item is not 'M':
						new_transition[name_map[key]][char][i] = name_map[item]
	

		# Create epsilon transition on concatenate
		for key in self_deterministic.accept_states:
			new_transition[key]['&'] = [name_map[other_deterministic.initial_state]]


		# Create dead state
		new_transition['M'] = {}
		for char in new_alphabet:
			new_transition['M'][char] = ['M']


		new_states = [state for state in new_transition]
		new_accept_states = [name_map[item] for item in other_deterministic.accept_states]

		concat_automaton = Automaton(new_states, new_alphabet, new_transition, new_initial_state, new_accept_states)
		return concat_automaton.determinize().beautify()

	def beautify(self):
		"""
		Beautifies the automaton, renaming every state with more readable names
		"""
		new_transition = {}
		new_initial_state = 'q0'

		name_map = {}
		name_map[self.initial_state] = 'q0'
		name_map['M'] = 'M'

		for state in self.transition:
			if state != self.initial_state and state is not 'M':
				name_map[state] = 'q'+str(len(name_map)-1)

		for state in self.transition:
			new_transition[name_map[state]] = {}
			for char in self.transition[state]:
				states = []
				for item in self.transition[state][char]:
					states.append(name_map[item])

				new_transition[name_map[state]][char] = states

		new_states = [state for state in new_transition]
		new_accept_states = [name_map[state] for state in self.accept_states]

		return Automaton(new_states, self.alphabet, new_transition, new_initial_state, new_accept_states)

	def generate_grammar(self):
		"""
		Generates the grammar based on the automaton
		"""
		automaton = self.determinize()

		production = {}
		start_symbol = ''

		# Creates the start symbol 
		if automaton.initial_state in automaton.accept_states:
			start_symbol = '<S>'
			production[start_symbol] = ['<'+automaton.initial_state+'>', '&']
		else:
			start_symbol = '<'+automaton.initial_state+'>'
			
		# Find the non terminal symbols
		nonterminal = []
		for item in automaton.states:
			if item is not 'M' and item is not 'F' and '<'+item+'>' not in nonterminal:
				nonterminal.append('<'+item+'>')

		# Find the terminal symbols
		terminal = automaton.alphabet

		# Find the production rules
		for key in automaton.transition:
			if key is not 'M' and key is not 'F':
				prod = ""
				for character in automaton.transition[key]:
					if automaton.transition[key][character][0] is not 'M':
						prod = character+"<"+automaton.transition[key][character][0]+">"
						try:
							production['<'+key+'>'].append(prod)
						except KeyError:
							production['<'+key+'>'] = [prod]
		
		# Find production rules resulting only in terminal symbols
		for key in automaton.transition:
			for character in automaton.transition[key]:
				for accept_state in automaton.accept_states:
					if automaton.transition[key][character][0] == accept_state:
						production['<'+key+'>'].append(character)


		return Grammar(nonterminal, terminal, production, start_symbol)

	def generate_regular_expression(self):
		"""
		Generates a regular expression based on the automaton
		"""

		# Generate general automaton
		re = ''

		deterministic = self.determinize();

		states = deterministic.states + ['qi', 'qf']
		initial_state = 'qi'
		accept_state = ['qf']

		transition = copy.deepcopy(deterministic.transition)
		transition[initial_state] = {}
		
		for char in deterministic.alphabet:
			transition[initial_state][char] = ['M']

		transition[initial_state]['&'] = [deterministic.initial_state]
		for state in deterministic.accept_states:
			transition[state]['&'] = accept_state

		transition['qf'] = {}
		for char in deterministic.alphabet:
			transition['qf'][char] = ['M']

		general_automaton = Automaton(states, deterministic.alphabet, transition, initial_state, accept_state)
		
		transition = general_automaton.transition
		state_list = sorted(general_automaton.states)


		while len(transition) > 2:
			# Select state to be removed
			index = 0
			states = sorted(list(transition.keys()))
			to_remove = states[index]
			while to_remove == 'qi' or to_remove == 'qf':
				index += 1
				to_remove = states[index]

			# Get all states that have a transition to to_remove
			previous_states = {}
			for state in state_list:
				for char in list(sorted(transition[state].keys())):
					if transition[state][char][0] == to_remove and state != to_remove:
						previous_states[state] = char

			# Get all states that to_remove have a transition to
			next_states = {}
			for char in list(sorted(transition[to_remove].keys())):
				for state in transition[to_remove][char]:
					if state != to_remove:
						next_states[state] = char

			# For each state in the previous states list
			# Link them with each state in the next states list
			for previous in list(sorted(previous_states.keys())):
				concat = ''
				for _next in list(sorted(next_states.keys())):
					next_char = next_states[_next]
					previous_char = previous_states[previous]

					if len(next_char) > 1:
						next_char = '('+next_char+')'
					if len(previous_char) > 1:
						previous_char = '('+previous_char+')'

					concat = previous_char + '$' + next_char
					
					# Check for closure
					# If there is a loop from to_remove to to_remove,
					# we replace '$' with the content of the closure
					for char in list(sorted(transition[to_remove].keys())):
						if transition[to_remove][char][0] == to_remove:
							if len(char) == 1:
								concat = concat.replace('$', ''+char+'*')
							else:
								concat = concat.replace('$', '('+char+')*')

					concat = concat.replace('$', '')

					if concat == '&&':
						concat = '&'
					elif len(concat) > 1 and '&' in concat and '|&' not in concat:
						concat = concat.replace('&', '')

					transition[previous][concat] = [_next]

			# Handles cases where there's two paths to the same state
			for state in sorted(list(previous_states.keys())):
				visited_list = {}
				for char in sorted(list(transition[state].keys())):
					target_state = transition[state][char][0]
					if target_state not in list(visited_list.keys()):
						visited_list[target_state] = char
					else:
						char2 = visited_list[target_state]
						union = char + '|' + char2

						transition[state][union] = [target_state]
						del transition[state][char]

			# Remove every transition to to_remove
			for state in state_list:
				for char in sorted(list(transition[state].keys())):
					if transition[state][char][0] == to_remove:
						del transition[state][char]

			# Finally remove the state
			del transition[to_remove]

			# Update the state list
			state_list = sorted(list(transition.keys()))

		# Get the resulting regular expression
		key = list(transition['qi'].keys())
		return RegularExpression(key[0])

class Grammar:
	"""
	A Grammar is defined formally by a 4-tuple
	(nonterminal, terminal, production, start_symbol)
	"""
	def __init__(self, nonterminal, terminal, production, start_symbol):
		self.nonterminal = nonterminal
		self.terminal = terminal
		self.production = production
		self.inverse_prod = self.invert_production(production)
		self.start_symbol = start_symbol

	def __str__(self):
		string = ""

		# Start symbol
		string += "Start symbol: "
		string += "\t"+self.start_symbol+"\n"

		# Terminal symbols
		string += "Terminal symbols: "
		string += "\t{"
		for i in range(len(self.terminal)-1):
			string += self.terminal[i]+", "
		string += self.terminal[-1]+"}\n"

		# Non terminal symbols
		string += "Non terminal symbols: "
		string += "\t{"
		for i in range(len(self.nonterminal)-1):
			string += self.nonterminal[i]+", "
		string += self.nonterminal[-1]+"}\n"

		# Production rules
		string += "Production rules: \n"
		for key in self.production:
			string += "\t"+key+" -> "+self.production[key][0]
			for i in range(1, len(self.production[key])-1):
				string += " | "+self.production[key][i]
			string += " | "+self.production[key][-1]+"\n"

		return string

	def invert_production(self, production):
		inverse_prod = {}

		for key in production:
			prod = production[key]
			for result in prod:
				try:
					inverse_prod[result].append(key)
				except KeyError:
					inverse_prod[result] = [key]

		return inverse_prod

	def derive(self, state, word):
		new_states = [state]
		new_states_aux = []

		print(state)

		iteration_limit = 500

		for i in range(iteration_limit):
			for state_aux in new_states:
				# generate next derivation step
				for key in self.production:
					for item in self.production[key]:
						new_state = state_aux.replace(key, item)
						if new_state != state_aux:
							new_states_aux.append(new_state)
							state = new_state
							print(state)
						if new_state == word:
							return True

			new_states = new_states_aux
			new_states_aux = []


		return False

	def reduce(self, word):
		new_words = []
		
		for key in self.inverse_prod:
			if key in word:
				for item in self.inverse_prod[key]:
					reduced_word = word.replace(key, item)
					if reduced_word != word:
						new_words.append(reduced_word)
		
		depth += 1
		for item in new_words:
			if self.reduce(item, depth):
				return True

		return word == self.start_symbol
	
	def generate_automaton(self):
		"""
		Generate an Automaton based on the Grammar
		"""
		# Converts each non terminal symbol into a state
		# states = [re.compile(r'<(.*?)>').findall(item)[0] for item in self.nonterminal]
		states = []
		for item in self.nonterminal:
			try:
				states.append(re.compile(r'<(.*?)>').findall(item)[0])
			except IndexError:
				states.append(item)

		# Adds the final(F) and dead(M) states
		states.append('F')
		states.append('M')

		alphabet = [item for item in self.terminal]

		# Converts the start symbol into an initial state
		try:
			initial_state = re.compile(r'<(.*?)>').findall(self.start_symbol)[0]
		except IndexError:
			initial_state = self.start_symbol

		accept_states = ['F']
		transition = {}

		# For each rule in the production
		for key in self.production:
			# Given a rule A -> Bc
			# Where A and B are non terminal symbols and a is a terminal symbol,
			# Creates a transition from the state named 'A'
			# To the state named 'B', by the character 'c'
			#
			# If the rule is A -> c
			# Then create a transition from 'A' to 'F' by 'c'.
			try:
				clean_key = re.compile(r'<(.*?)>').findall(key)[0]
			except IndexError:
				clean_key = key
			transition[clean_key] = {}
			for item in self.production[key]:
				if item in self.terminal or item == '&':
					try:
						transition[clean_key][item].append('F')
					except KeyError:
						transition[clean_key][item] = ['F']
				else:
					try:
						next_state = re.compile(r'<(.*?)>').findall(item)[0]
					except IndexError:
						next_state = item
					try:
						char = re.compile(r'(.*?)<'+next_state+'>').findall(item)[0]
					except IndexError:
						char = item
			# print("SSSSSSSSSSSSSSSSSSSS 	ggenerate_automaton")

					if char == '':
						char = '&'

					try:
						transition[clean_key][char].append(next_state)
					except KeyError:
						transition[clean_key][char] = [next_state]

		# Creates the transitions for the dead(M) and final(F) states
		transition['F'] = {}
		transition['M'] = {}
		for char in alphabet:	
			transition['F'][char] = ['M']
			transition['M'][char] = ['M']

		# Build the Automaton and returns
		automaton = Automaton(states, alphabet, transition, initial_state, accept_states)
		return automaton.determinize()

class RegularExpression:
	"""
	Regular expressions describe regular languages in formal language theory.
	"""
	def __init__(self, expression):
		self.expression = expression

	def __str__(self):
		return self.expression

	def generate_automaton(self):
		"""
		Generates an Automaton based on the regular expression
		"""

		# Initially, creates the final Automaton accepting only the empty word
		automaton = Automaton(['qi'], [], {}, 'qi', ['qi'])

		# Creates an auxiliary Automaton, to be used on union
		automaton_aux = Automaton(['qi'], [], {}, 'qi', ['qi'])
	
		# Auxiliary variables
		operation_stack = []
		union_pending = False
		open_stack = []
		i = 0

		# Iterates over the expression string
		while True:
			try:
				char = self.expression[i]

				# If char is '(' saves it's position on open_stack array
				if char is '(':
					open_stack.append(i)

				# If char is ')', we found a closing scope
				elif char is ')':
					# If we have already found a '(' before,
					# Ignore so we can generate the automaton recursively 
					# For the expression inside the '()' scope.
					if len(open_stack) > 1:
						del open_stack[-1]
					else:
						# Resolve the expression inside the '()' scope
						sub_re_str = self.expression[open_stack[-1]+1:i]
						sub_automaton = RegularExpression(sub_re_str).generate_automaton()
						after = i+1
						
						try:
							# If the whole scope is a closure, positive closure or &|() (ending with '?''),
							# Modify the resulting automaton
							if self.expression[after] is '*':
								for state in sub_automaton.transition:
									if state in sub_automaton.accept_states:
										sub_automaton.transition[state]['&'] = [sub_automaton.initial_state]
								for state in sub_automaton.accept_states:
									try:
										sub_automaton.transition[sub_automaton.initial_state]['&'].append(state)
									except KeyError:
										sub_automaton.transition[sub_automaton.initial_state]['&'] = [state]

								self.expression = self.expression[:after]+self.expression[after+1:]

							elif self.expression[after] is '+':
								for state in sub_automaton.transition:
									if state in sub_automaton.accept_states:
										try:
											sub_automaton.transition[state]['&'].append(sub_automaton.initial_state)
										except KeyError:
											sub_automaton.transition[state]['&'] = [sub_automaton.initial_state]


								self.expression = self.expression[:after]+self.expression[after+1:]
							
							elif self.expression[after] is '?':
								sub_automaton = sub_automaton | Automaton(['qi'], [], {}, 'qi', ['qi'])

								self.expression = self.expression[:after]+self.expression[after+1:]
						except IndexError:
							pass

						# If there's a union pending, only concatenates the generated automaton
						# To the auxiliary automaton.
						if union_pending:
							automaton_aux = automaton_aux + sub_automaton
						else:
							automaton = automaton + sub_automaton

						# Finally, remove the reference to the opening scope from the stack
						del open_stack[-1]


				elif char is '?' or char is '*' or char is '+':
					pass

				elif char is '|':
					# If there's a union pending and char is '|', 
					# Generate the union between the final automaton and the auxiliary automaton
					# Else, that's the first union symbol found, so sets union_pending as True.
					if union_pending:
						automaton = automaton | automaton_aux
						automaton_aux = Automaton(['qi'], [], {}, 'qi', ['qi'])
					elif len(open_stack) == 0:
						union_pending = True

				
				# U - {?,*,+,(,),|}
				# If char is not a special symbol and we are not currently searching for a close scope(')')
				# Then generates a simple automaton for that char, considering if it's *, + or ?.
				elif len(open_stack) == 0:
					next_char = ''
					try:
						next_char = self.expression[i+1]
					except IndexError:
						pass
					
					# If there's a union pending, only concatenates the generated automaton
					# To the auxiliary automaton.
					if union_pending:
						automaton_aux = automaton_aux + self.generate_simple_automaton(char, next_char)
					else:
						automaton = automaton + self.generate_simple_automaton(char, next_char)

			except IndexError:
				# If the while true caused an IndexError, then we have generated everything we need
				# Lastly, checks if there's still a union pending and generates the union 
				if union_pending:
					automaton = automaton | automaton_aux

				return automaton.determinize().beautify()

			# Increment the index counter
			i += 1

	def generate_simple_automaton(self, char, next_char=''):
		"""
		Generates a simple automaton that recognizes a single character
		Also, if it's a closure, positive closure or &|() (ending with '?''),
		Modify the automaton
		"""

		states = ['q0', 'q1']
		alphabet = [char]
		transition = {
			'q0': {},
			'q1': {}
		}
		transition['q0'][char] = ['q1']
		transition['q1'][char] = ['M']
		initial_state = 'q0'
		accept_states = ['q1']

		if next_char is '+':
			transition['q1']['&'] = ['q0']
		elif next_char is '*':
			transition['q1']['&'] = ['q0']
			transition['q0']['&'] = ['q1']
		elif next_char is '?':
			transition['q0']['&'] = ['q1']

		return Automaton(states, alphabet, transition, initial_state, accept_states)
