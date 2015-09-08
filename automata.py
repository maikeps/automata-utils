#! /usr/bin/python3

import json

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
			if self.states[i] is not 'F' and self.states[i] is not 'M':
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

	def change_state(self, current_states, _input):
		achieved_states = []
		deleted_states = []

		# current_states = self.epsilon(current_states)

		for current_state in current_states:
			future_states = self.transition[current_state][_input]
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
		transition = self.transition
		transition_aux = {}

		for state in transition:
			if '&' in self.alphabet:
				epsilon = self.epsilon(state)
			else:
				epsilon = [state]

			if epsilon != [state]:
				new_state = epsilon

				new_state_str = ""

				for aux in new_state:
					new_state_str += aux

				if new_state_str not in transition:
					self.add_state(new_state, new_state_str, transition, transition_aux)
			else:
				for _input in transition[state]:
					if _input is not '&':
						new_state = transition[state][_input]
										
						new_state_str = ""
					
						for aux in new_state:
							new_state_str += aux

						if new_state_str not in transition:
							self.add_state(new_state, new_state_str, transition, transition_aux)

		for key in transition_aux:
			transition[key] = transition_aux[key]


		new_states = [key for key in transition]
		new_accept_states = []
		for state in transition:
			for final_state in self.accept_states:
				if final_state in state:
					new_accept_states.append(state)

		for state in transition:
			for next_state in transition[state]:
				if len(transition[state][next_state]) > 1:
					state_str = ""
				
					for aux in transition[state][next_state]:
						state_str += aux
					transition[state][next_state] = [state_str]
			if '&' in self.alphabet:
				del transition[state]['&']

		alphabet = self.alphabet

		if '&' in self.alphabet:
			del alphabet[alphabet.index('&')]

		return Automaton(new_states, self.alphabet,	transition,	self.initial_state, new_accept_states)

	def epsilon(self, state):
		closure = [state]

		states_aux = [state];
		while True:
			count = 0
			next_states = []
			for state_aux in states_aux:
				next_states = self.change_state([state_aux], '&')
				for next_state in next_states:
					if next_state not in closure and next_state is not 'M' and next_state is not 'F':
						count += 1
						closure.append(next_state)
			states_aux = next_states

			if count == 0:
				return closure

	def add_state(self, new_state_arr, new_state_name, transition, transition_aux):
		# Add the new transition, with empty info
		transition_aux[new_state_name] = {}

		for input_aux in self.alphabet:
			aux = []
			# Get each possible transition from the new state
			# and get the transition from the current input
			for state_aux in new_state_arr: 
				for item in transition[state_aux][input_aux]:
					if item not in aux and transition[state_aux][input_aux] != ['M']:
						if '&' not in self.alphabet:
							aux.append(item)
						else:
							aux = aux + self.epsilon(item)

			if aux == []:
				aux = ['M']
			transition_aux[new_state_name][input_aux] = aux

		for item in transition_aux[new_state_name]:
			aux_str = ""
			for state in transition_aux[new_state_name][item]:
				aux_str += state
				
			if aux_str not in transition and aux_str not in transition_aux:
				self.add_state(transition_aux[new_state_name][item], aux_str, transition, transition_aux)

	def generate_grammar(self):
		automaton = self.determinize()

		start_symbol = automaton.initial_state
		nonterminal = [item for item in automaton.states if item is not 'M' and item is not 'F']
		terminal = [item for item in automaton.alphabet]

		production = {}
		for key in automaton.transition:
			if key is not 'M' and key is not 'F':
				prod = ""
				for character in automaton.transition[key]:
					prod = character+"<"+automaton.transition[key][character][0]+">"
					try:
						production[key].append(prod)
					except KeyError:
						production[key] = [prod]
		
		for key in automaton.transition:
			for character in automaton.transition[key]:
				for accept_state in automaton.accept_states:
					if automaton.transition[key][character][0] is accept_state:
						production[key].append(character)

		return Grammar(nonterminal, terminal, production, start_symbol)

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
		states = [item for item in self.nonterminal]
		states.append('F')
		states.append('M')
		alphabet = [item for item in self.terminal]
		initial_state = self.start_symbol

		accept_states = ['F']
		transition = {}

		for key in self.production:
			transition[key] = {}
			for item in self.production[key]:
				if item.islower():
					try:
						transition[key][item].append('F')
					except KeyError:
						transition[key][item] = ['F']
				else:
					char = item
					next_state = ''
					for letter in item:
						if letter.isupper():
							char = char.replace(letter, '')
							next_state = letter
						# else:
					try:
						transition[key][char].append(next_state)
					except KeyError:
						transition[key][char] = [next_state]


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
		if self.expression is '&':
			return Automaton(states=['q0'], alphabet=[], transition=[], initial_state='q0', accept_states=['q0'])
		if self.expression is '':
			return Automaton(states=['q0'], alphabet=[], transition=[], initial_state='q0', accept_states=[])
		if len(self.expression) == 1:
			states = ['q0', 'q1']
			alphabet = [self.expression]
			transition = {
				'q0': {},
				'q1': {}
			}
			transition['q0'][self.expression] = ['q1']
			transition['q1'][self.expression] = ['M']
			initial_state = 'q0'
			accept_states = ['q1']

			return Automaton(states, alphabet, transition, initial_state, accept_states)


def open_file(src):
	with open(src) as f:
		json_file = json.load(f)
		file_type = json_file["type"]

		if file_type == 'automaton':
			return file_type, open_automaton(json_file)
		if file_type == 'grammar':
			return file_type, open_grammar(json_file)
		if file_type == 're':
			return file_type, open_re(json_file)

def save_file(target_src, obj):
	with open(target_src, 'w') as outfile:
		if type(obj) is Automaton:
			save_automaton(outfile, obj)
		elif type(obj) is Grammar:
			save_grammar(outfile, obj)
		elif type(obj) is RegularExpression:
			save_re(outfile, obj)

def open_automaton(json_file):
	states = json_file["states"]
	alphabet = json_file["alphabet"]
	initial_state = json_file["initial_state"]
	accept_states = json_file["accept_states"]
	transition = json_file["transition"]

	return Automaton(states, alphabet, transition, initial_state, accept_states)

def save_automaton(outfile, obj):
	json_file = {
		"type": "automaton",
		"states": obj.states,
		"alphabet": obj.alphabet,
		"initial_state": obj.initial_state,
		"accept_states": obj.accept_states,
		"transition": obj.transition
	}
	json.dump(json_file, outfile)

def open_grammar(json_file):
	start_symbol = json_file["start_symbol"]
	terminal = json_file["terminal"]
	nonterminal = json_file["nonterminal"]
	production = json_file["production"]

	return Grammar(nonterminal, terminal, production, start_symbol)

def save_grammar(outfile, obj):
	json_file = {
		"type": "grammar",
		"start_symbol": obj.start_symbol,
		"terminal": obj.terminal,
		"nonterminal": obj.nonterminal,
		"production": obj.production
	}
	json.dump(json_file, outfile)

def open_re(json_file):
	return RegularExpression(json_file["expression"])

def save_re(outfile, obj):
	json_file = {
		"type": "re",
		"expression": obj.expression
	}
	json.dump(json_file, outfile)

def process_load(src):
	file_type, current = open_file(args[1])
	log = 'File "' + args[1] + '" loaded.\nYou are now working with'
	if type(current) is Automaton:
		log += ' an Automaton.'
	elif type(current) is Grammar:
		log += ' a Grammar.'
	elif type(current) is RegularExpression:
		log += ' a Regular Expression.'
	print(log)

	return file_type, current


def process_conversion(current, target):
	if target == 'automaton':
		conversion = current.generate_automaton()
	elif target == 'grammar':
		conversion = current.generate_grammar()
	elif target == 're':
		conversion = current.generage_re()

	return conversion

def process_save(which, target_src):
	if which == 'current':
		save_file(target_src, current)
	elif which == 'conversion':
		save_file(target_src, conversion)

def proccess_print(which):
	if which == 'current':
		print(current)
	elif which == 'conversion':
		print(conversion)

def show_help():
	print("Help")

if __name__ == '__main__':
	command = ""
	while True:
		command = input('>')
		args = command.split(' ')

		try:
			if args[0] == 'load':
				try:
					file_type, current = process_load(args[1])
				except FileNotFoundError:
					print('File "'+args[1]+'" not found.')


			elif args[0] == 'convert':
				try:
					conversion = process_conversion(current, args[1])
				except NameError:
					print('Error: File not yet loaded.')
				except AttributeError:
					print('Error: Cannot convert '+file_type+' into '+args[1])
		
			elif args[0] == 'save':
				try:
					process_save(args[1], args[2])
				except NameError:
					if args[1] == 'current':
						print('Error: File not yet loaded.')
					elif args[1] == 'conversion':
						print('Error: File not yet converted.')

			elif args[0] == 'print':
				try:
					proccess_print(args[1])
				except NameError:
					if args[1] == 'current':
						print('Error: File not yet loaded.')
					elif args[1] == 'conversion':
						print('Error: File not yet converted.')

			elif args[0] == 'exit':
				break

			elif args[0] == 'help':
				show_help()

			else:
				print('Command not found.')

		except IndexError:
			print('Not enough arguments.')
