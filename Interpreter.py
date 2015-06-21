__author__ = 'Ties'

import Statement as S
import sys
# sys.setrecursionlimit(5000)

if False:
    with open (raw_input(), "r") as file:
        data=file.read().replace('\n','').replace('\t','').replace(chr(184),'').replace(chr(248),chr(195))
    print "DATA =" + data
else:
    data = raw_input().replace('\n','').replace('\t','').replace(chr(184),'').replace(chr(248),chr(195))

input = []
with open ("input.txt", "r") as file:
    input=file.read().replace('\n','')
print "Input: " + input
input = "In"
input = list(input)
state = S.Statement(data)
print "State: " + str(state.statement)

# state = S.Statement("20[1-$][$.]#")
# state = S.Statement("10$[1-$$.7>[a;!]?]a:a;!")
# state = S.Statement("[3 5+]a:5a;-")
# state = S.Statement("[3-]a:3 5+[[$-1][$.]#]z:%{ dit is een comment }99 9[1-$][\$@$@$@$@\/*=[1-$$[%\ 1-$@]?0=[\$.\]?]?]#")
# state = S.Statement("1$[$][$@+$.]#")
stack = []
output = []
variables = {}
# state.execute(stack, variables)
# try:
state.execute(stack, variables, input, output)
# except Exception as exc:
#     print "EXCEPTION: " + str(exc)
#     exit()
print "\nExecute succesfull:"
print " Stack: " + str(stack)
print " Variables: " + str(variables)
print " Syntax: " + state.printtree()
print " Output: " + str(output)

with open ("header.tex", "r") as file:
    header=file.read()

busstree = header +  state.printbuss() + "\DP\n\\end{document}"
# print " LaTeX: \n" + busstree
# print " Counter: " + str(counter)
with open ("busstree.tex", "w") as file:
    file.write(busstree)