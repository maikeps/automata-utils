import json
from automata import *

def read_file(src):
	with open(src) as f:
		return f.read().splitlines()

def write_file(src, content):
	with open(src, 'w') as f:
		for item in content:
			line = '<'+', '.join(item)+'>\n'
			# line = line
			f.write(line)

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
