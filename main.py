#! /usr/bin/python3

from automata import Automaton
from automata import Grammar
from automata import RegularExpression
from reader import *


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