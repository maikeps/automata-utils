import reader

tokens = reader.read_file("caspalc/tokens")
parser = reader.read_json("parse_table.json")
productions = parser["productions"]
table = parser["table"]



def check(tokens):
	stack = ['$', '<S>']
	i = 0
	current_word = get_token_info(tokens[i])
	
	while stack != ['$']:
		if(i >= len(tokens) and stack != ['$']):
			print("ERROR: Unexpected end of file.")
			return False

		print(stack, tokens[i])
		if stack[-1] == current_word:
			i += 1
			if i < len(tokens):
				current_word = get_token_info(tokens[i])
			del stack[-1]
		else:
			top = stack[-1]
			subs = productions[table[top][current_word]]
		
			if subs == ["ERR"]:
				print("ERROR: SYNTAX ERROR NEAR " + current_word)
				return False
			del stack[-1]
			
			for item in subs:
				if item != '&':
					stack.append(item)
	print("SYNTAX ANALYSIS COMPLETE")
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
