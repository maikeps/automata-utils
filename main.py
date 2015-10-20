#! /usr/bin/python3

import json

from automata import Automaton
from automata import Grammar
from automata import RegularExpression


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
	if target == 'deterministic':
		conversion = current.determinize()
	elif target == 'automaton':
		conversion = current.generate_automaton()
	elif target == 'grammar':
		conversion = current.generate_grammar()
	elif target == 're':
		conversion = current.generate_regular_expression()
	return conversion

def process_save(which, target_src):
	if which == 'current':
		save_file(target_src, current)
	elif which == 'conversion':
		save_file(target_src, conversion)

def proccess_print(which):
	if which == 'current':
		print(current, '\n')
	elif which == 'conversion':
		print(conversion, '\n')
	else:
		print('Command not found.')


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
					if file_type != 'automaton':
						print('Error: Can only convert automata to their deterministic form.')
					else:
						print('Error: Cannot convert '+file_type+' into '+args[1])
			
			elif args[0] == 'minimize':
				# try:
				conversion = current.minimize()
				# except NameError:
				# 	print('Error: File not yet loaded.')
				# except AttributeError:
				# 	if file_type != 'automaton':
				# 		print('Error: Only automata have the minimize function.')
				
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

			elif args[0] == 'refresh':
				try:
					current = conversion
					conversion = None

					print("You are now working with "+current.__class__.__name__)
				except NameError:
					print('Error: File not yet converted.')

			elif args[0] == 'exit':
				print("Bye.")
				break

			else:
				print('Command not found.')

		except IndexError:
			print('Not enough arguments.')