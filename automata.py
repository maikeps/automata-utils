import copy
import re

class Automaton:

	# An automaton is defined formally by a 5-tuple
	# (states, alphabet, transition function, initial state, accept states)
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
		#	if self.states[i] is not 'F' and self.states[i] is not 'M':
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
		new_transition = {}
		
		initial_closure = self.epsilon(self.initial_state)

		self.add_state(initial_closure, self.transition, new_transition)

		new_states = [key for key in new_transition]
		new_accept_states = []
		for state in new_transition:
			for final_state in self.accept_states:
				if final_state in state and state not in new_accept_states:
					new_accept_states.append(state)


		return Automaton(new_states, self.alphabet,	new_transition,	''.join(sorted(initial_closure)), new_accept_states)

	def epsilon(self, state):
		closure = [state]

		states_aux = [state];
		while True:
			count = 0
			next_states = []
			for state_aux in states_aux:
				next_states = self.change_state([state_aux], '&')
				for next_state in next_states:
					if next_state not in closure and next_state is not 'M':
						count += 1
						closure.append(next_state)
			
			states_aux = next_states

			if count == 0:
				return closure

	def add_state(self, new_state_arr, transition, new_transition):
		# Add the new transition, with empty info
		new_state_arr = sorted(new_state_arr)
		new_state_name = ''.join(new_state_arr)

		new_transition[new_state_name] = {}

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
				
			if aux == []:
				aux = ['M']

			sort = sorted(aux)
			name = ''.join(sort)
			new_transition[new_state_name][input_aux] = [name]

			if name not in new_transition:
				self.add_state(sort, transition, new_transition)

	def union(self, other):
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
		# return union_automaton

	def concat(self, other):
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
		# return concat_automaton

	def beautify(self):
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
		automaton = self.determinize()

		production = {}
		start_symbol = ''

		if automaton.initial_state in automaton.accept_states:
			start_symbol = '<S>'
			production[start_symbol] = ['<'+automaton.initial_state+'>', '&']
		else:
			start_symbol = '<'+automaton.initial_state+'>'
			
		nonterminal = []
		for item in automaton.states:
			if item is not 'M' and item is not 'F' and '<'+item+'>' not in nonterminal:
				nonterminal.append('<'+item+'>')

		terminal = automaton.alphabet

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
		
		for key in automaton.transition:
			for character in automaton.transition[key]:
				for accept_state in automaton.accept_states:
					if automaton.transition[key][character][0] == accept_state:
						production['<'+key+'>'].append(character)


		return Grammar(nonterminal, terminal, production, start_symbol)

	def generate_regular_expression(self):
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
	
		try:
			del transition['M']
			del transition['F']
		except KeyError:
			pass

		while len(transition) > 2:
			# print(transition)
			index = 0
			to_remove = list(transition.keys())[index]
			while to_remove == 'qi' or to_remove == 'qf':
				index += 1
				to_remove = list(transition.keys())[index]

			previous_states = []
			next_states = []

			for state in transition:
				for char in transition[state]:
					if transition[state][char][0] == to_remove and state != to_remove:
						previous_states.append((state, char))

			for char in transition[to_remove]:
				if transition[to_remove][char][0] != to_remove and transition[to_remove][char][0] != 'M' and transition[to_remove][char][0] != 'F':
					next_states.append((transition[to_remove][char][0], char))



			for previous_state in previous_states:
				concat = ''
				for next_state in next_states:
					concat = previous_state[1] + '$' + next_state[1]
					concat = concat.replace('&', '')

					for char in transition[to_remove]:
						if to_remove == transition[to_remove][char][0]:
							concat = concat.replace('$', '('+char+')*')
							break

					if '$' in concat:
						concat = concat.replace('$', '')

					transition[previous_state[0]][concat] = [next_state[0]]

				if concat != previous_state[1]:
					del transition[previous_state[0]][previous_state[1]]

			union = ''

			for previous_state in previous_states:
				state = previous_state[0]
				for char in list(transition[state].keys()):
					aux = transition[state][char]
					for char2 in list(transition[state].keys()):
						if aux == transition[state][char2] and char != char2:
							union = char + '|' + char2
							transition[state][union] = transition[state][char]
							del transition[state][char]
							del transition[state][char2]
							break
					if union != '':
						break
			del transition[to_remove]
			

		for char in list(transition['qi'].keys()):
			if transition['qi'][char][0] == 'M':
				del transition['qi'][char]



		key = list(transition['qi'].keys())
		print("saedwd", transition)
		return RegularExpression(key[0])

class Grammar:
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

	# Grammar type 3
	def generate_automaton(self):
		states = [re.compile(r'<(.*?)>').findall(item)[0] for item in self.nonterminal]
		states.append('F')
		states.append('M')
		alphabet = [item for item in self.terminal]
		initial_state = re.compile(r'<(.*?)>').findall(self.start_symbol)[0]

		accept_states = ['F']
		transition = {}

		for key in self.production:
			clean_key = re.compile(r'<(.*?)>').findall(key)[0]
			transition[clean_key] = {}
			for item in self.production[key]:
				if item in self.terminal or item == '&':
					try:
						transition[clean_key][item].append('F')
					except KeyError:
						transition[clean_key][item] = ['F']
				else:
					next_state = re.compile(r'<(.*?)>').findall(item)[0]
					char = re.compile(r'(.*?)<'+next_state+'>').findall(item)[0]

					if char == '':
						char = '&'

					try:
						transition[clean_key][char].append(next_state)
					except KeyError:
						transition[clean_key][char] = [next_state]

		transition['F'] = {}
		transition['M'] = {}
		for char in alphabet:	
			transition['F'][char] = ['M']
			transition['M'][char] = ['M']

		automaton = Automaton(states, alphabet, transition, initial_state, accept_states)
		return automaton.determinize()

class RegularExpression:

	def __init__(self, expression):
		self.expression = expression

	def __str__(self):
		return self.expression

	def generate_automaton(self):
		automaton = Automaton(['qi'], [], {}, 'qi', ['qi'])
		automaton_aux = Automaton(['qi'], [], {}, 'qi', ['qi'])
	
		operation_stack = []
		union_pending = False
		open_stack = []
		i = 0
		while True:
			try:
				char = self.expression[i]


				if char is '(':
					open_stack.append(i)
				elif char is ')':
					if len(open_stack) > 1:
						del open_stack[-1]
					else:
						# Resolve scope from open_stack[-1] to i
						sub_re_str = self.expression[open_stack[-1]+1:i]
						sub_automaton = RegularExpression(sub_re_str).generate_automaton()
						after = i+1
						
						try:
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


						if union_pending:
							automaton_aux = automaton_aux + sub_automaton
						else:
							automaton = automaton + sub_automaton

						del open_stack[-1]


				elif char is '?' or char is '*' or char is '+':
					pass

				elif char is '|':
					if union_pending:
						automaton = automaton | automaton_aux
						automaton_aux = Automaton(['qi'], [], {}, 'qi', ['qi'])
					elif len(open_stack) == 0:
						union_pending = True

				
				#!{?,*,+,(,),|}
				elif len(open_stack) == 0:
					next_char = ''
					try:
						next_char = self.expression[i+1]
					except IndexError:
						pass
					if union_pending:
						automaton_aux = automaton_aux + self.generate_simple_automaton(char, next_char)
					else:
						automaton = automaton + self.generate_simple_automaton(char, next_char)

			except IndexError:
				if union_pending:
					automaton = automaton | automaton_aux

				return automaton.determinize().beautify()


			i += 1

	def generate_simple_automaton(self, char, next_char=''):
		
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
			print('antes', accept_states)
			transition['q0']['&'] = ['q1']
			print('dps', accept_states)

		return Automaton(states, alphabet, transition, initial_state, accept_states)