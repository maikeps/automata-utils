productions = {
	"0": ["ERR"],
	"1": ["<S'>", ";", "ID", "grampro"],
	"2": [".", "ned", "<PROGRAM>", "ginbe"],
	"3": [".", "ned", "<PROGRAM>", "ginbe", "<VAR>", "rav"],
	"4": ["<VAR>", ";", "VAR_TYPE", ":", "<LIST_VAR>"],
	"5": ["&"],
	"6": ["<LIST_VAR'>", "ID"],
	"7": ["<LIST_VAR>", ","],
	"8": ["&"],
	"9": ["<PROGRAM'>", "ID"],
	"10": ["<PROGRAM>", "<LOOP>"],
	"11": ["<PROGRAM>", "<COND>"],
	"12": ["<PROGRAM>", ";", "<EXP>", "tewri"],
	"13": ["&"],
	"14": ["<PROGRAM''>", ":="],
	"15": ["<PROGRAM>", ";", "<EXP>", ":=", "OP_ARR"],
	"16": ["<PROGRAM>", ";", "<EXP>"],
	"17": ["<PROGRAM>", ";", "CONST", "adre"],
	"18": ["<PROGRAM>", ";", "<EXP>", "UNARY_OP"],
	"19": [";", "ned", "<PROGRAM>", "od", "CONST", "ot", "<EXP>", ":=", "ID", "rof"],
	"20": ["<ELSE>", "<PROGRAM>", "enth", "<EXP>", "fi"],
	"21": [";", "ned", "<PROGRAM>", "seel"],
	"22": [";", "ned"],
	"23": ["<EXP'>", "ID"],
	"24": ["<EXP'>", "CONST"],
	"25": ["<EXP>", "OP"],
	"26": ["&"],
	"27": ["&"] #extra pros FOL
}

table = {
	"<S>": {
		"grampro": "1", "ID": "", ";": "", "ginbe": "", "ned": "", ".": "", "rav": "", ":": "", "VAR_TYPE": "", ",": "", "tewri": "", ":=": "", 
		"OP_ARR": "", "adre": "", "rof": "", "ot": "", "CONST": "", "od": "", "fi": "", "enth": "", "seel": "", "UNARY_OP": "", "OP": "", "$": ""
	},
	"<S'>": {
		"grampro": "", "ID": "", ";": "", "ginbe": "2", "ned": "", ".": "", "rav": "3", ":": "", "VAR_TYPE": "", ",": "", "tewri": "", ":=": "", 
		"OP_ARR": "", "adre": "", "rof": "", "ot": "", "CONST": "", "od": "", "fi": "", "enth": "", "seel": "", "UNARY_OP": "", "OP": "", "$": ""
	},
	"<VAR>": {
		"grampro": "", "ID": "4", ";": "", "ginbe": "5", "ned": "", ".": "", "rav": "", ":": "", "VAR_TYPE": "", ",": "", "tewri": "", ":=": "", 
		"OP_ARR": "", "adre": "", "rof": "", "ot": "", "CONST": "", "od": "", "fi": "", "enth": "", "seel": "", "UNARY_OP": "", "OP": "", "$": ""
	},
	"<LIST_VAR>": {
		"grampro": "", "ID": "6", ";": "", "ginbe": "", "ned": "", ".": "", "rav": "", ":": "", "VAR_TYPE": "", ",": "", "tewri": "", ":=": "", 
		"OP_ARR": "", "adre": "", "rof": "", "ot": "", "CONST": "", "od": "", "fi": "", "enth": "", "seel": "", "UNARY_OP": "", "OP": "", "$": ""
	},
	"<LIST_VAR'>": {
		"grampro": "", "ID": "", ";": "", "ginbe": "", "ned": "", ".": "", "rav": "", ":": "8", "VAR_TYPE": "", ",": "7", "tewri": "", ":=": "", 
		"OP_ARR": "", "adre": "", "rof": "", "ot": "", "CONST": "", "od": "", "fi": "", "enth": "", "seel": "", "UNARY_OP": "", "OP": "", "$": ""
	},
	"<PROGRAM>": {
		"grampro": "", "ID": "9", ";": "", "ginbe": "", "ned": "13", ".": "", "rav": "", ":": "", "VAR_TYPE": "", ",": "", "tewri": "12", ":=": "", 
		"OP_ARR": "", "adre": "", "rof": "10", "ot": "", "CONST": "", "od": "", "fi": "11", "enth": "", "seel": "13", "UNARY_OP": "", "OP": "", "$": ""
	},
	"<PROGRAM'>": {
		"grampro": "", "ID": "", ";": "", "ginbe": "", "ned": "", ".": "", "rav": "", ":": "", "VAR_TYPE": "", ",": "", "tewri": "", ":=": "14", 
		"OP_ARR": "15", "adre": "", "rof": "", "ot": "", "CONST": "", "od": "", "fi": "", "enth": "", "seel": "", "UNARY_OP": "", "OP": "", "$": ""
	},
	"<PROGRAM''>": {
		"grampro": "", "ID": "16", ";": "", "ginbe": "", "ned": "", ".": "", "rav": "", ":": "", "VAR_TYPE": "", ",": "", "tewri": "", ":=": "", 
		"OP_ARR": "", "adre": "17", "rof": "", "ot": "", "CONST": "16", "od": "", "fi": "", "enth": "", "seel": "", "UNARY_OP": "18", "OP": "", "$": ""
	},
	"<LOOP>": {
		"grampro": "", "ID": "", ";": "", "ginbe": "", "ned": "", ".": "", "rav": "", ":": "", "VAR_TYPE": "", ",": "", "tewri": "", ":=": "", 
		"OP_ARR": "", "adre": "", "rof": "19", "ot": "", "CONST": "", "od": "", "fi": "", "enth": "", "seel": "", "UNARY_OP": "", "OP": "", "$": ""
	},
	"<COND>": {
		"grampro": "", "ID": "", ";": "", "ginbe": "", "ned": "", ".": "", "rav": "", ":": "", "VAR_TYPE": "", ",": "", "tewri": "", ":=": "", 
		"OP_ARR": "", "adre": "", "rof": "", "ot": "", "CONST": "", "od": "", "fi": "20", "enth": "", "seel": "", "UNARY_OP": "", "OP": "", "$": ""
	},
	"<ELSE>": {
		"grampro": "", "ID": "", ";": "", "ginbe": "", "ned": "22", ".": "", "rav": "", ":": "", "VAR_TYPE": "", ",": "", "tewri": "", ":=": "", 
		"OP_ARR": "", "adre": "", "rof": "", "ot": "", "CONST": "", "od": "", "fi": "", "enth": "", "seel": "21", "UNARY_OP": "", "OP": "", "$": ""
	},
	"<EXP>": {
		"grampro": "", "ID": "23", ";": "", "ginbe": "", "ned": "", ".": "", "rav": "", ":": "", "VAR_TYPE": "", ",": "", "tewri": "", ":=": "", 
		"OP_ARR": "", "adre": "", "rof": "", "ot": "", "CONST": "24", "od": "", "fi": "", "enth": "", "seel": "", "UNARY_OP": "", "OP": "", "$": ""
	},
	"<EXP'>": {
		"grampro": "", "ID": "", ";": "26", "ginbe": "", "ned": "", ".": "", "rav": "", ":": "", "VAR_TYPE": "", ",": "", "tewri": "", ":=": "", 
		"OP_ARR": "", "adre": "", "rof": "", "ot": "26", "CONST": "", "od": "", "fi": "", "enth": "26", "seel": "", "UNARY_OP": "", "OP": "25", "$": ""
	}
}

tokens = ["<grampro, PR>", 
"< , SEP>", 
"<myFirstGrampro, ID>", 
"<;, SEP>", 
"< , SEP>", 
"<rav, PR>", 
"< , SEP>", 
"<age, ID>", 
"<,, SEP>", 
"< , SEP>", 
"<height, ID>", 
"<,, SEP>", 
"< , SEP>", 
"<i, ID>", 
"<:, SEP>", 
"< , SEP>", 
"<tegerin, VAR_TYPE>", 
"<;, SEP>", 
"< , SEP>", 
"<info, ID>", 
"<:, SEP>", 
"< , SEP>", 
"<tegerin[], VAR_TYPE>", 
"<;, SEP>", 
"< , SEP>", 
"<name, ID>", 
"<:, SEP>", 
"< , SEP>", 
"<ingstr, VAR_TYPE>", 
"<;, SEP>", 
"< , SEP>", 
"<is_tall, ID>", 
"<,, SEP>", 
"< , SEP>", 
"<is_old, ID>", 
"<:, SEP>", 
"< , SEP>", 
"<leanboo, VAR_TYPE>", 
"<;, SEP>", 
"< , SEP>", 
"< , SEP>", 
"<ginbe, PR>", 
"< , SEP>", 
"<name, ID>", 
"< , SEP>", 
"<:=, OP>", 
"< , SEP>", 
"<adre, PR>", 
"< , SEP>", 
"<'What is your name', CONST>", 
"<;, SEP>", 
"< , SEP>", 
"<age, ID>", 
"< , SEP>", 
"<:=, OP>", 
"< , SEP>", 
"<adre, PR>", 
"< , SEP>", 
"<'How old are you', CONST>", 
"<;, SEP>", 
"< , SEP>", 
"<height, ID>", 
"< , SEP>", 
"<:=, OP>", 
"< , SEP>", 
"<adre, PR>", 
"< , SEP>", 
"<'What is your height', CONST>", 
"<;, SEP>", 
"< , SEP>", 
"< , SEP>", 
"<info, ID>", 
"< , SEP>", 
"<[0], OP_ARR>", 
"< , SEP>", 
"<:=, OP>", 
"< , SEP>", 
"<age, ID>", 
"<;, SEP>", 
"< , SEP>", 
"<info, ID>", 
"< , SEP>", 
"<[1], OP_ARR>", 
"< , SEP>", 
"<:=, OP>", 
"< , SEP>", 
"<height, ID>", 
"<;, SEP>", 
"< , SEP>", 
"< , SEP>", 
"<fi, PR>", 
"< , SEP>", 
"<height, ID>", 
"< , SEP>", 
"<>, OP>", 
"< , SEP>", 
"<175, CONST>", 
"< , SEP>", 
"<enth, PR>", 
"< , SEP>", 
"<is_tall, ID>", 
"< , SEP>", 
"<:=, OP>", 
"< , SEP>", 
"<Etru, CONST>", 
"<;, SEP>", 
"< , SEP>", 
"<seel, PR>", 
"< , SEP>", 
"<is_tall, ID>", 
"< , SEP>", 
"<:=, OP>", 
"< , SEP>", 
"<Sefal, CONST>", 
"<;, SEP>", 
"< , SEP>", 
"<ned, PR>", 
"<;, SEP>", 
"< , SEP>", 
"< , SEP>", 
"<is_old, ID>", 
"< , SEP>", 
"<:=, OP>", 
"< , SEP>", 
"<is_old, ID>", 
"< , SEP>", 
"<>, OP>", 
"< , SEP>", 
"<40, CONST>", 
"<;, SEP>", 
"< , SEP>", 
"< , SEP>", 
"<fi, PR>", 
"< , SEP>", 
"<is_tall, ID>", 
"< , SEP>", 
"<enth, PR>", 
"< , SEP>", 
"<fi, PR>", 
"< , SEP>", 
"<is_old, ID>", 
"< , SEP>", 
"<enth, PR>", 
"< , SEP>", 
"<tewri, PR>", 
"< , SEP>", 
"<name, ID>", 
"< , SEP>", 
"<;, SEP>", 
"< , SEP>", 
"<seel, PR>", 
"< , SEP>", 
"<tewri, PR>", 
"< , SEP>", 
"<name, ID>", 
"< , SEP>", 
"<;, SEP>", 
"< , SEP>", 
"<ned, PR>", 
"<;, SEP>", 
"< , SEP>", 
"<seel, PR>", 
"< , SEP>", 
"<fi, PR>", 
"< , SEP>", 
"<is_old, ID>", 
"< , SEP>", 
"<enth, PR>", 
"< , SEP>", 
"<tewri, PR>", 
"< , SEP>", 
"<name, ID>", 
"< , SEP>", 
"<;, SEP>", 
"< , SEP>", 
"<seel, PR>", 
"< , SEP>", 
"<tewri, PR>", 
"< , SEP>", 
"<name, ID>", 
"< , SEP>", 
"<;, SEP>", 
"< , SEP>", 
"<ned, PR>", 
"<;, SEP>", 
"< , SEP>", 
"<ned, PR>", 
"<;, SEP>", 
"< , SEP>", 
"< , SEP>", 
"<rof, PR>", 
"< , SEP>", 
"<i, ID>", 
"< , SEP>", 
"<:=, OP>", 
"< , SEP>", 
"<0, CONST>", 
"< , SEP>", 
"<ot, PR>", 
"< , SEP>", 
"<10, CONST>", 
"< , SEP>", 
"<od, PR>", 
"< , SEP>", 
"<fi, PR>", 
"< , SEP>", 
"<5, CONST>", 
"< , SEP>", 
"<si, OP>", 
"< , SEP>", 
"<5, CONST>", 
"< , SEP>", 
"<enth, PR>", 
"< , SEP>", 
"<tewri, PR>", 
"< , SEP>", 
"<'For loop test', CONST>", 
"<;, SEP>", 
"< , SEP>", 
"<ned, PR>", 
"<;, SEP>", 
"< , SEP>", 
"<ned, PR>", 
"<;, SEP>", 
"< , SEP>", 
"< , SEP>", 
"<ned, PR>", 
"<., SEP>"]

def check(tokens):
	stack = ['$', '<S>']
	i = 0
	current_word = get_token_info(tokens[i])
	
	while stack != ['$']:
		print(stack, tokens[i])
		if stack[-1] == current_word:
			i += 1
			if i < len(tokens):
				while get_token_info(tokens[i]) == ' ':
					i += 1
				current_word = get_token_info(tokens[i])
			del stack[-1]
		else:
			top = stack[-1]
			print(current_word)
			subs = productions[table[top][current_word]]
		
			if subs == "":
				return False
			del stack[-1]
			
			for item in subs:
				if item != '&':
					stack.append(item)
	
	return True

def get_token_info(token):
	token = token[1:]
	token = token[:-1]
	info = token.split(', ')
	if info[1] == 'PR' or info[1] == 'SEP' or info[0] == ':=':
		return info[0]
	else:
		return info[1]

print(check(tokens))
