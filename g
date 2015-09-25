{
"terminal": ["1", "2"],
"start_symbol": "<S>", 
"nonterminal": ["<q0>", "<q1>", "<S>"], 
"production": {
	"<q1>": ["2<q1>", "1<q0>", "1"], 
	"<q0>": ["2<q0>", "1<q1>", "2"], 
	"<S>": ["<q0>", "&"]
}, 
"type": "grammar"
}