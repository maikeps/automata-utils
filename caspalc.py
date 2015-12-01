#! /usr/bin/python3

from automata import RegularExpression as RE
from automata import Automaton

import reader
import sys

def gen_lex():
	# PR
	grampro = RE('grampro').generate_automaton()
	rav = RE('rav').generate_automaton()
	ginbe = RE('ginbe').generate_automaton()
	ned = RE('ned').generate_automaton()
	rof = RE('rof').generate_automaton()
	od = RE('od').generate_automaton()
	fi = RE('fi').generate_automaton()
	enth = RE('enth').generate_automaton()
	seel = RE('seel').generate_automaton()
	ot = RE('ot').generate_automaton()
	adre = RE('adre').generate_automaton()
	tewri = RE('tewri').generate_automaton()


	pr = (grampro | rav | ginbe).determinize()
	pr = (pr | ned | rof).determinize()
	pr = (pr | od | fi).determinize()
	pr = (pr | enth | seel).determinize()
	pr = (pr | adre | tewri).determinize()
	pr = (pr | ot).determinize()
	pr = pr.minimize()

	print('Created PR')


	# DeclVar
	tegerin = RE('tegerin([])*').generate_automaton()
	leanboo = RE('leanboo([])*').generate_automaton()
	ingstr = RE('ingstr([])*').generate_automaton()

	declvar = (tegerin | leanboo).determinize()
	declvar = (declvar | ingstr).determinize()
	declvar = declvar.minimize()

	print('Created DECLVAR')


	# CONST
	etru = RE('Etru').generate_automaton()
	sefal = RE('Sefal').generate_automaton()
	numbas = RE('(-?(1|2|3|4|5|6|7|8|9)(1|2|3|4|5|6|7|8|9|0)*)|0').generate_automaton()

	const = (etru | sefal).determinize()
	const = (const | numbas).determinize()
	const = const.minimize()
	print('Created CONST')

	# String
	string = RE('"(q|w|e|r|t|y|u|i|o|p|a|s|d|f|g|h|j|k|l|z|x|c|v|b|n|m|Q|W|E|R|T|Y|U|I|O|P|A|S|D|F|G|H|J|K|L|Z|X|C|V|B|N|M|1|2|3|4|5|6|7|8|9|0| )*"').generate_automaton()

	string = string.minimize()
	print('Created STRING')

	# OP
	add = Automaton(['p', 'q', 'M'], ['+'], {'p': {'+': ['q']},'q': {'+': ['M']},'M': {'+': ['M']}}, 'p', ['q'])
	sub = RE('-').generate_automaton()
	div = RE('/').generate_automaton()
	mul = Automaton(['p', 'q', 'M'], ['*'], {'p': {'*': ['q']},'q': {'*': ['M']},'M': {'*': ['M']}}, 'p', ['q'])
	ro = RE('ro').generate_automaton()
	nad = RE('nad').generate_automaton()
	ton = RE('ton').generate_automaton()
	grt = RE('>').generate_automaton()
	lst = RE('<').generate_automaton()
	neq = RE('!=').generate_automaton()
	eq = RE('si').generate_automaton()
	ass = RE('=').generate_automaton()

	num_re = '(((1|2|3|4|5|6|7|8|9)(1|2|3|4|5|6|7|8|9|0)*)|0)'
	id_re = '((q|w|e|r|t|y|u|i|o|p|a|s|d|f|g|h|j|k|l|z|x|c|v|b|n|m|Q|W|E|R|T|Y|U|I|O|P|A|S|D|F|G|H|J|K|L|Z|X|C|V|B|N|M|_)(q|w|e|r|t|y|u|i|o|p|a|s|d|f|g|h|j|k|l|z|x|c|v|b|n|m|Q|W|E|R|T|Y|U|I|O|P|A|S|D|F|G|H|J|K|L|Z|X|C|V|B|N|M|_|1|2|3|4|5|6|7|8|9|0)*)'
	str_re = '("(q|w|e|r|t|y|u|i|o|p|a|s|d|f|g|h|j|k|l|z|x|c|v|b|n|m|Q|W|E|R|T|Y|U|I|O|P|A|S|D|F|G|H|J|K|L|Z|X|C|V|B|N|M|1|2|3|4|5|6|7|8|9|0| )*")'
	op_arr_re = '['+num_re+']'# + '|' + id_re + '|' + str_re+']'
	op_arr = RE(op_arr_re).generate_automaton()

	op = (add | sub).determinize()
	op = (op | div).determinize()
	op = (op | mul).determinize()
	op = (op | ro).determinize()
	op = (op | nad).determinize()
	op = (op | ton).determinize()
	op = (op | grt).determinize()
	op = (op | lst).determinize()
	op = (op | neq).determinize()
	op = (op | eq).determinize()
	op = (op | ass).determinize()
	op = (op | op_arr).determinize()
	op = op.minimize()

	print('Created OP')


	# ID
	di = RE('(q|w|e|r|t|y|u|i|o|p|a|s|d|f|g|h|j|k|l|z|x|c|v|b|n|m|Q|W|E|R|T|Y|U|I|O|P|A|S|D|F|G|H|J|K|L|Z|X|C|V|B|N|M|_)(q|w|e|r|t|y|u|i|o|p|a|s|d|f|g|h|j|k|l|z|x|c|v|b|n|m|Q|W|E|R|T|Y|U|I|O|P|A|S|D|F|G|H|J|K|L|Z|X|C|V|B|N|M|_|1|2|3|4|5|6|7|8|9|0)*').generate_automaton()

	ids = di.minimize()

	print('Created ID')


	# SEP
	space = RE(' ').generate_automaton()
	semicolon = RE(';').generate_automaton()
	dot = RE('.').generate_automaton()
	comma = RE(',').generate_automaton()
	colon = RE(':').generate_automaton()

	sep = (space | semicolon).determinize()
	sep = (sep | dot).determinize()
	sep = (sep | comma).determinize()
	sep = (sep | colon).determinize()
	sep = sep.minimize()

	print('Created SEP')

	lex = (const | op).determinize()
	lex = (lex | pr).determinize()
	lex = (lex | sep).determinize()
	lex = (lex | declvar).determinize()
	lex = (lex | string).determinize()
	lex = (lex | ids).determinize()
	
	lex = rename(lex)

	reader.save_file('caspalc/lex', lex)

def analyze(src):
	program = ' '.join(reader.read_file(src))
	lex = reader.open_file('caspalc/lex')[1]
	tokens = lex.analyze(program)
	reader.write_file('caspalc/tokens', tokens)

def rename(automaton):
	# PR
	automaton.verify_word('grampro')
	accept_state = automaton.current_states[0]

	for state in automaton.transition:
		for char in automaton.transition[state]:
			if accept_state in automaton.transition[state][char]:
				automaton.transition[state][char] = ['PR']

	automaton.transition['PR'] = automaton.transition[accept_state]
	del automaton.transition[accept_state]

	automaton.accept_states.append('PR')
	automaton.accept_states.remove(accept_state)

	automaton.states.append('PR')
	automaton.states.remove(accept_state)


	# OP
	automaton.verify_word('+')
	accept_state = automaton.current_states[0]

	for state in automaton.transition:
		for char in automaton.transition[state]:
			if accept_state in automaton.transition[state][char]:
				automaton.transition[state][char] = ['OP']

	automaton.transition['OP'] = automaton.transition[accept_state]
	del automaton.transition[accept_state]

	automaton.accept_states.append('OP')
	automaton.accept_states.remove(accept_state)

	automaton.states.append('OP')
	automaton.states.remove(accept_state)

	# OP SUB
	automaton.verify_word('-')
	accept_state = automaton.current_states[0]

	for state in automaton.transition:
		for char in automaton.transition[state]:
			if accept_state in automaton.transition[state][char]:
				automaton.transition[state][char] = ['OP_SUB']

	automaton.transition['OP_SUB'] = automaton.transition[accept_state]
	del automaton.transition[accept_state]

	automaton.accept_states.append('OP_SUB')
	automaton.accept_states.remove(accept_state)

	automaton.states.append('OP_SUB')
	automaton.states.remove(accept_state)

	# OP - LOGIC
	automaton.verify_word('ton')
	accept_state = automaton.current_states[0]

	for state in automaton.transition:
		for char in automaton.transition[state]:
			if accept_state in automaton.transition[state][char]:
				automaton.transition[state][char] = ['OP_LOGIC']

	automaton.transition['OP_LOGIC'] = automaton.transition[accept_state]
	del automaton.transition[accept_state]

	automaton.accept_states.append('OP_LOGIC')
	automaton.accept_states.remove(accept_state)

	automaton.states.append('OP_LOGIC')
	automaton.states.remove(accept_state)

	# OP - LOGIC
	automaton.verify_word('ro')
	accept_state = automaton.current_states[0]

	for state in automaton.transition:
		for char in automaton.transition[state]:
			if accept_state in automaton.transition[state][char]:
				automaton.transition[state][char] = ['OP_LOGIC']

	automaton.transition['OP_LOGIC'] = automaton.transition[accept_state]
	del automaton.transition[accept_state]

	automaton.accept_states.append('OP_LOGIC')
	automaton.accept_states.remove(accept_state)

	automaton.states.append('OP_LOGIC')
	automaton.states.remove(accept_state)


	# DECLVAR
	automaton.verify_word('tegerin')
	accept_state = automaton.current_states[0]

	for state in automaton.transition:
		for char in automaton.transition[state]:
			if accept_state in automaton.transition[state][char]:
				automaton.transition[state][char] = ['DECLVAR']

	automaton.transition['DECLVAR'] = automaton.transition[accept_state]
	del automaton.transition[accept_state]

	automaton.accept_states.append('DECLVAR')
	automaton.accept_states.remove(accept_state)

	automaton.states.append('DECLVAR')
	automaton.states.remove(accept_state)

	# DECLVAR - Array
	automaton.verify_word('tegerin[]')
	accept_state = automaton.current_states[0]

	for state in automaton.transition:
		for char in automaton.transition[state]:
			if accept_state in automaton.transition[state][char]:
				automaton.transition[state][char] = ['DECLVAR_ARR']

	automaton.transition['DECLVAR_ARR'] = automaton.transition[accept_state]
	del automaton.transition[accept_state]

	automaton.accept_states.append('DECLVAR_ARR')
	automaton.accept_states.remove(accept_state)

	automaton.states.append('DECLVAR_ARR')
	automaton.states.remove(accept_state)


	# SEP
	automaton.verify_word(' ')
	accept_state = automaton.current_states[0]

	for state in automaton.transition:
		for char in automaton.transition[state]:
			if accept_state in automaton.transition[state][char]:
				automaton.transition[state][char] = ['SEP']

	automaton.transition['SEP'] = automaton.transition[accept_state]
	del automaton.transition[accept_state]

	automaton.accept_states.append('SEP')
	automaton.accept_states.remove(accept_state)

	automaton.states.append('SEP')
	automaton.states.remove(accept_state)


	# ID
	automaton.verify_word('b')
	accept_state = automaton.current_states[0]

	for state in automaton.transition:
		for char in automaton.transition[state]:
			if accept_state in automaton.transition[state][char]:
				automaton.transition[state][char] = ['ID']

	automaton.transition['ID'] = automaton.transition[accept_state]
	del automaton.transition[accept_state]

	automaton.accept_states.append('ID')
	automaton.accept_states.remove(accept_state)

	automaton.states.append('ID')
	automaton.states.remove(accept_state)


	# CONST - Numbers
	automaton.verify_word('1')
	accept_state = automaton.current_states[0]

	for state in automaton.transition:
		for char in automaton.transition[state]:
			if accept_state in automaton.transition[state][char]:
				automaton.transition[state][char] = ['CONST']

	automaton.transition['CONST'] = automaton.transition[accept_state]
	del automaton.transition[accept_state]

	automaton.accept_states.append('CONST')
	automaton.accept_states.remove(accept_state)

	automaton.states.append('CONST')
	automaton.states.remove(accept_state)


	# CONST - String
	automaton.verify_word('"foo"')
	accept_state = automaton.current_states[0]

	for state in automaton.transition:
		for char in automaton.transition[state]:
			if accept_state in automaton.transition[state][char]:
				automaton.transition[state][char] = ['STRING']

	automaton.transition['STRING'] = automaton.transition[accept_state]
	del automaton.transition[accept_state]

	automaton.accept_states.append('STRING')
	automaton.accept_states.remove(accept_state)

	automaton.states.append('STRING')
	automaton.states.remove(accept_state)


	# CONST - REZO
	automaton.verify_word('0')
	accept_state = automaton.current_states[0]

	for state in automaton.transition:
		for char in automaton.transition[state]:
			if accept_state in automaton.transition[state][char]:
				automaton.transition[state][char] = ['CONST_ZERO']

	automaton.transition['CONST_ZERO'] = automaton.transition[accept_state]
	del automaton.transition[accept_state]

	automaton.accept_states.append('CONST_ZERO')
	automaton.accept_states.remove(accept_state)

	automaton.states.append('CONST_ZERO')
	automaton.states.remove(accept_state)

	# COSNT - leanboo
	automaton.verify_word('Sefal')
	accept_state = automaton.current_states[0]

	for state in automaton.transition:
		for char in automaton.transition[state]:
			if accept_state in automaton.transition[state][char]:
				automaton.transition[state][char] = ['CONST_BOOL']

	automaton.transition['CONST_BOOL'] = automaton.transition[accept_state]
	del automaton.transition[accept_state]

	automaton.accept_states.append('CONST_BOOL')
	automaton.accept_states.remove(accept_state)

	automaton.states.append('CONST_BOOL')
	automaton.states.remove(accept_state)

	# ERROR
	for state in automaton.transition:
		for char in automaton.transition[state]:
			if 'M' in automaton.transition[state][char]:
				automaton.transition[state][char] = ['ERROR']

	automaton.transition['ERROR'] = automaton.transition['M']
	del automaton.transition['M']

	automaton.states.append('ERROR')
	automaton.states.remove('M')


	return automaton


if __name__ == '__main__':
	gen_lex()
	args = sys.argv
	program_src = args[1]
	print(analyze(program_src))
