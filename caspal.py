from automata import RegularExpression as RE
from automata import Automaton

import reader

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
	adre = RE('adre').generate_automaton()
	tewri = RE('tewri').generate_automaton()

	# pr = grampro | rav | ginbe | ned | rof | od | fi | enth | seel | adre | tewri
	# pr = (grampro | rav | ginbe ).determinize() | ned | rof).determinize() | od | fi).determinize() | enth | seel).determinize() | adre | tewri).determinize()
	pr = (grampro | rav | ginbe).determinize()
	pr = (pr | ned | rof).determinize()
	pr = (pr | od | fi).determinize()
	pr = (pr | enth | seel).determinize()
	pr = (pr | adre | tewri).determinize()
	# pr = (grampro | rav).determinize()
	# print(pr.accept_states)
	pr = pr.minimize()

	# print(pr.accept_states)
	# print(pr)
	# reader.save_file('caspal/pr', pr)

	# print(pr)
	# DeclVar
	tegerin = RE('tegerin').generate_automaton()
	leanboo = RE('leanboo').generate_automaton()
	ingstr = RE('ingstr').generate_automaton()
	tegerin_arr = RE('tegerin[]').generate_automaton()
	leanboo_arr = RE('leanboo[]').generate_automaton()
	ingstr_arr = RE('ingstr[]').generate_automaton()

	# declvar = tegerin | leanboo | ingstr | tegerin_arr | leanboo_arr | ingstr_arr


	# CONST
	etru = RE('etru').generate_automaton()
	sefal = RE('sefal').generate_automaton()
	_ = RE('0').generate_automaton()
	a = RE('1').generate_automaton()
	aa = RE('2').generate_automaton()
	aaa = RE('3').generate_automaton()
	aaaa = RE('4').generate_automaton()
	aaaaa = RE('5').generate_automaton()
	aaaaaa = RE('6').generate_automaton()
	aaaaaaa = RE('7').generate_automaton()
	aaaaaaaa = RE('8').generate_automaton()
	aaaaaaaaa = RE('9').generate_automaton()
	string = RE('\'(q|w|e|r|t|y|u|i|o|p|a|s|d|f|g|h|j|k|l|z|x|c|v|b|n|m|Q|W|E|R|T|Y|U|I|O|P|A|S|D|F|G|H|J|K|L|Z|X|C|V|B|N|M|1|2|3|4|5|6|7|8|9|0| )*\'').generate_automaton()


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
	eq = RE('==').generate_automaton()
	ass = RE('=').generate_automaton()
	# # tesquo = RE('\'').generate_automaton()

	# ID
	# di = RE('(q|w|e|r|t|y|u|i|o|p|a|s|d|f|g|h|j|k|l|z|x|c|v|b|n|m|Q|W|E|R|T|Y|U|I|O|P|A|S|D|F|G|H|J|K|L|Z|X|C|V|B|N|M|_)(q|w|e|r|t|y|u|i|o|p|a|s|d|f|g|h|j|k|l|z|x|c|v|b|n|m|Q|W|E|R|T|Y|U|I|O|P|A|S|D|F|G|H|J|K|L|Z|X|C|V|B|N|M|_|1|2|3|4|5|6|7|8|9|0)*').generate_automaton()
	di = RE('(a|b)*').generate_automaton()
	print(di)

	# SEP
	space = RE(' ').generate_automaton()
	semicolon = RE(';').generate_automaton()
	dot = RE('.').generate_automaton()
	comma = RE(',').generate_automaton()
	colon = RE(':').generate_automaton()


	# const = etru | sefal | _ | a | aa | aaa | aaaa | aaaaa | aaaaaa | aaaaaaa | aaaaaaaa | aaaaaaaaa | string
	# op = add | sub | div | mul | ro | nad | ton | grt | lst | neq | eq | ass# | tesquo
	# ids = di
	# sep = space | semicolon | dot | comma | colon

	# print('fi')
	# print(fi)
	# print()
	# print('enth')
	# print(enth)
	# print()
	# print('di')
	# print(di)
	# print()
	# print()

	# pr = fi | enth
	ids = di
	sep = space | semicolon | dot
	op = ass | add | grt
	const = a
	declvar = tegerin


	# pr = pr.minimize()
	# print('asas', pr)
	# declvar = declvar.minimize().beautify()
	const = const.minimize()
	op = op.minimize()
	ids = ids.minimize()
	sep = sep.minimize()
	declvar = declvar.minimize()

	# print(sep)
	# print(((const | ids | op).determinize() | pr | sep).determinize())

	lex = (((const | ids | op).determinize() | pr | sep).determinize() | declvar).determinize()
	lex = rename(lex)


	# lex = pr.union(op, True).union(ids, True).union(sep, True).union(const, True)# | declvar 
	# lex = pr | declvar | const | op | ids | sep

	reader.save_file('caspal/lex', lex)
	
def analyze(src):
	program = ' '.join(reader.read_file(src))
	lex = reader.open_file('caspal/lex')[1]

	print(program)
	print(lex.analyze(program))

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
	automaton.verify_word('=')
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

	
	# CONST
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


	return automaton

gen_lex()
analyze('caspal/test.csp')
# di = RE('(a|b)*').generate_automaton()
