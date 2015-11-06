from automata import RegularExpression as RE
from automata import Automaton

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

# DeclVar
tegerin = RE('tegerin').generate_automaton()
leanboo = RE('leanboo').generate_automaton()
ingstr = RE('ingstr').generate_automaton()
tegerin_arr = RE('tegerin[]').generate_automaton()
leanboo_arr = RE('leanboo[]').generate_automaton()
ingstr_arr = RE('ingstr[]').generate_automaton()


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
string = RE('\'(q|w|e|r|t|y|u|i|o|p|a|s|d|f|g|h|j|k|l|z|x|c|v|b|n|m|Q|W|E|R|T|Y|U|I|O|P|A|S|D|F|G|H|J|K|L|Z|X|C|V|B|N|M|1|2|3|4|5|6|7|8|9|0| )*\'')

# OP
add = Automaton(['p', 'q', 'M'], ['+'], {'p': {'+': ['q']},'q': {'+': ['p']},'M': {'+': ['M']}}, 'p', ['q'])
sub = RE('-').generate_automaton()
div = RE('/').generate_automaton()
mul = Automaton(['p', 'q', 'M'], ['*'], {'p': {'*': ['q']},'q': {'*': ['p']},'M': {'*': ['M']}}, 'p', ['q'])
ro = RE('ro').generate_automaton()
nad = RE('nad').generate_automaton()
ton = RE('ton').generate_automaton()
grt = RE('>').generate_automaton()
lst = RE('<').generate_automaton()
neq = RE('!=').generate_automaton()
eq = RE('==').generate_automaton()
ass = RE('=').generate_automaton()
# tesquo = RE('\'').generate_automaton()

# ID
di = RE('(q|w|e|r|t|y|u|i|o|p|a|s|d|f|g|h|j|k|l|z|x|c|v|b|n|m|Q|W|E|R|T|Y|U|I|O|P|A|S|D|F|G|H|J|K|L|Z|X|C|V|B|N|M|_)(q|w|e|r|t|y|u|i|o|p|a|s|d|f|g|h|j|k|l|z|x|c|v|b|n|m|Q|W|E|R|T|Y|U|I|O|P|A|S|D|F|G|H|J|K|L|Z|X|C|V|B|N|M|_|1|2|3|4|5|6|7|8|9|0)*').generate_automaton()

# SEP
space = RE(' ').generate_automaton()
semicolon = RE(';').generate_automaton()
dot = RE('.').generate_automaton()
colon = RE(',').generate_automaton()


pr = grampro | rav | ginbe | ned | rof | od | fi | enth | seel | adre | tewri
declvar = tegerin | leanboo | ingstr | tegerin_arr | leanboo_arr | ingstr_arr
const = etru | sefal | _ | a | aa | aaa | aaaa | aaaaa | aaaaaa | aaaaaaa | aaaaaaaa | aaaaaaaaa
op = add | sub | div | mul | ro | nad | ton | grt | lst | neq | eq | ass# | tesquo
ids = di
sep = space | semicolon | dot | colon

pr = pr.determinize().beautify().minimize()
declvar = declvar.determinize().beautify().minimize()
const = declvar.determinize().beautify().minimize()
op = op.determinize().beautify().minimize()
ids = ids.determinize().beautify().minimize()
sep = sep.determinize().beautify().minimize()

final = pr | declvar | const | op | ids | sep

print(final)
print(final.analyze('grampro name;'))