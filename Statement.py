__author__ = 'Ties'
import Statement as S
import copy

class Statement:
    def __init__(self,statement):
        self.statement =  statement
        self.children = []
        self.compile()


    def compile(self):
        #Remove whitespaces at front
        while self.statement[0] == ' ':
            self.statement = self.statement[1:]

        while self.statement[0] == '{':
            self.statement = self.statement[self.findclosure(self.statement,'{','}')+1:]

        #Read first char
        self.a = str(self.statement[0])
        self.b = ""

        #Read additional digits if constant
        if self.a[0] in "0123456789":
            self.statement = self.statement + " "
            while self.statement[len(self.a)] in "0123456789":
                self.a = self.a + self.statement[len(self.a)]
            self.statement = self.statement[:-1]

        if self.a[0] == '\'':
            self.a = self.a + self.statement[len(self.a)]

        if self.a[0] == '"':
            close = self.findclosure(self.statement[len(self.a)-1:],'','"')
            while len(self.a) != close:
                self.a = self.a + self.statement[len(self.a)]
            self.a = self.a + self.statement[len(self.a)]

        if self.a[0] == '[':
            close = self.findclosure(self.statement[len(self.a)-1:],'[',']')
            while len(self.a) != close:
                self.a = self.a + self.statement[len(self.a)]
            self.a = self.a + self.statement[len(self.a)]
            self.encapsulate = S.Statement(self.a[1:-1])

        # print "Statement: " + self.a + " " + " Code: " + self.statement
         #Composition
        if len(self.statement) > len(self.a):
            # print "COMP"
            self.children.append(S.Statement(self.a))
            self.children.append(S.Statement(self.statement[len(self.a):]))

    def findclosure(self,string,begin,end):
        cap = 1
        for i in range(1,len(string)):
            if string[i]==end:
                cap = cap-1
            if string[i]==begin:
                cap = cap+1
            if cap == 0:
                return i
    #     SYNTAX ERROR
        print "syntax error"

    def execute(self,stack,variables, input, output):
        self.prestack = list(stack)
        self.prevariables = str(variables)
        self.preinput = list(input)
        self.preoutput = list(output)
        # print str(stack) + " on " + self.printtree()
        if len(self.children)==2:
            for child in self.children:
                child.execute(stack,variables, input, output)
        else:
            ### ARITHMETIC OPERATIONS:
            # +: Add
            # Input: n, m
            # Output: m+n
            if self.a == '+':
                a = stack.pop(len(stack)-1)
                stack.append(stack.pop(len(stack)-1) + a)

            # -: Substract
            # Input: n, m
            # Output: m-n
            elif self.a == '-':
                a = stack.pop(len(stack)-1)
                stack.append(stack.pop(len(stack)-1) - a)

            # *: Multiply
            # Input: n, m
            # Output: m*n
            elif self.a == '*':
                a = stack.pop(len(stack)-1)
                stack.append(stack.pop(len(stack)-1) * a)

            # /: Divide
            # Input: n, m
            # Output: m/n
            elif self.a == '/':
                a = stack.pop(len(stack)-1)
                stack.append(stack.pop(len(stack)-1) / a)

            # _: Negative
            # Input: n
            # Output: -n
            elif self.a == '_':
                stack.append(-stack.pop(len(stack)-1))

            # .: Print integer
            # Input: n
            # Output:
            elif self.a == '.':
                output.append(stack.pop(len(stack)-1))

            # ,: Print char
            # Input: n
            # Output:
            elif self.a == ',':
                output.append(chr(stack.pop(len(stack)-1)))

            # : Print string
            # Input:
            # Output:
            elif self.a[0] == '"':
                output.extend(list(self.a[1:-1]))

            # {letter}: Put/Execute lambda variable
            # Input:
            # Output:
            elif self.a[0] in "abcdefghijklmnopqrstuvwxyz":
                stack.append(self.a[0])

            elif self.a[0]==':':
                a = stack.pop(len(stack)-1)
                if a in "abcdefghijklmnopqrstuvwxyz":
                    b = stack.pop(len(stack)-1)
                    variables[a] = b
                    self.waarde = b
                    self.variabele = a
                else:
                    raise Exception("Try to assign to illegal variable!")

            elif self.a[0]==';':
                stack.append(variables[stack.pop(len(stack)-1)])

            # !: Execute lambda variable
            # Input: []
            # Output:
            elif self.a == '!':
                self.children.append(stack.pop(len(stack)-1))
                self.children[0].execute(stack,variables,input,output)

            # ?: Execute lambda variable conditionally (IF)
            # Input: [] n
            # Output:
            elif self.a == '?':
                a = stack.pop(len(stack)-1)
                if stack.pop(len(stack)-1)!=0:
                    a.execute(stack,variables,input,output)

            # #: Execute lambda variable conditionally repeatedly (WHILE)
            # Input: [] [] n
            # Output:
            elif self.a == "#":
                a = stack.pop(len(stack)-1)
                b = stack.pop(len(stack)-1)
                child = copy.copy(b)
                self.children.append(child)
                child.execute(stack,variables,input,output)
                self.repetitions = 1
                self.stacks = []
                self.variables = []
                while(stack.pop(len(stack)-1)!=0):
                    self.repetitions = self.repetitions + 1
                    child = copy.copy(a)
                    self.children.append(child)
                    child.execute(stack,variables,input,output)
                    child = copy.copy(b)
                    self.children.append(child)
                    child.execute(stack,variables,input,output)

            ### CONDITIONAL OPERATIONS:
            # =: Equals
            # Input: n, m
            # Output: n==m
            elif self.a == '=':
                if stack.pop(len(stack)-1)==stack.pop(len(stack)-1):
                    stack.append(-1)
                else:
                    stack.append(0)

            # =: Or
            # Input: n, m
            # Output: n==m
            elif self.a == '|':
                if stack.pop(len(stack)-1)!=0 or stack.pop(len(stack)-1)!=0:
                    stack.append(-1)
                else:
                    stack.append(0)

            # =: Not
            # Input: n
            # Output: !n
            elif self.a == '~':
                a = stack.pop(len(stack)-1)
                print a
                stack.append(a*-1-1)

            # >: Greater Than
            # Input: n, m
            # Output: n>m
            elif self.a == '>':
                if stack.pop(len(stack)-1)<stack.pop(len(stack)-1):
                    stack.append(-1)
                else:
                    stack.append(0)

            ###BASIC STACK OPERATIONS
            # $: Duplicate top
            # Input: n
            # Output: n, n
            elif self.a == '$':
                stack.append(stack[len(stack)-1])

            # $: Pick
            # Input: n
            # Output: m
            elif len(self.a) == 1 and ord(self.a[0]) == 195:
                stack.append(stack[len(stack)-1-stack.pop(len(stack)-1)])

            # \: Swap
            # Input: n, m
            # Output: n, m
            elif self.a == '\\':
                a = stack.pop(len(stack)-1)
                b = stack.pop(len(stack)-1)
                stack.append(a)
                stack.append(b)

            # @: Rotate
            # Input: n, m, o
            # Output: m, o, n
            elif self.a == '@':
                a = stack.pop(len(stack)-1)
                b = stack.pop(len(stack)-1)
                c = stack.pop(len(stack)-1)
                stack.append(b)
                stack.append(a)
                stack.append(c)

            # %: Remove
            # Input: n
            # Output:
            elif self.a == '%':
                stack.pop(len(stack)-1)

            elif self.a == 'Q':
                stack.append(stack[len(stack)-2-stack.pop(len(stack)-1)])

            elif self.a == "^":
                stack.append(ord(input.pop()))

            ### INTEGER:
            # {integer}: Integer
            # Input:
            # Output: {integer}
            elif self.a.isdigit():
                stack.append(int(self.a))

            elif self.a[0] == '\'':
                stack.append(ord(self.a[1]))

            ### STATEMENT:
            else:
                if hasattr(self,'encapsulate'):
                    stack.append(self.encapsulate)
                else:
                    raise Exception("Undefined statement '" + self.a + "', ASCII code '" + str(ord(self.a[0])) + "'!")
        self.poststack = list(stack)
        self.postvariables = str(variables)
        self.postinput = list(input)
        self.postoutput = list(output)

    def printtree(self):
        if len(self.children)==2:
            return self.children[0].printtree() + self.children[1].printtree()
        else:
            return "[" + self.a + "]"

    def printbuss(self):
            if len(self.children)>0:
                string = ""
                # While
                if hasattr(self,'repetitions'):
                    return self.makeWhileb(0)
                else:
                    # Format children strings
                    for child in self.children:
                        string = string + child.printbuss()

                    # !: Execute
                    if self.a[0] == '!' and len(self.children)==1:
                        return string + "\\RightLabel{$[apply^{ns}]$}\n\\UnaryInfC{$\\langle  "+ self.format(self.a) + ", g," + self.format(self.printer(self.prestack)) + "," + self.format(self.printer(self.preinput)) + "," + self.format(self.printer(self.preoutput)) \
                       + "\\rangle \\rightarrow(g," + self.format(self.printer(self.poststack)) + "," + self.format(self.printer(self.postinput)) + "," + self.format(self.printer(self.postoutput))+")$}\n"
                    else:
                        # Composition
                        return string + "\\RightLabel{$[comp^{ns}]$}\n\\BinaryInfC{$\\langle " \
                       + self.format(self.a) + self.format(self.statement[len(self.a):]) + ", g," + self.format(self.printer(self.prestack)) + "," + self.format(self.printer(self.preinput)) + "," + self.format(self.printer(self.preoutput)) \
                       + "\\rangle \\rightarrow(g," + self.format(self.printer(self.poststack)) + "," + self.format(self.printer(self.postinput)) + "," + self.format(self.printer(self.postoutput))\
                       + ")$}\n"
            else:
                ###### AXIOMS
                ### 1. STACK OPERATIONS
                # Duplicate
                if self.a[0] == "$":
                    return "\\AxiomC{}\n\\RightLabel{$[dup^{ns}]$}\n\\UnaryInfC{$\\langle  "+ self.format(self.a) + ", g," + self.format(self.printer(self.prestack)) + "," + self.format(self.printer(self.preinput)) + "," + self.format(self.printer(self.preoutput)) \
                       + "\\rangle \\rightarrow(g," + self.format(self.printer(self.poststack)) + "," + self.format(self.printer(self.postinput)) + "," + self.format(self.printer(self.postoutput))+")$}\n"
                # Swap
                if self.a[0] == "\\":
                    return "\\AxiomC{}\n\\RightLabel{$[swap^{ns}]$}\n\\UnaryInfC{$\\langle  "+ self.format(self.a) + ", g," + self.format(self.printer(self.prestack)) + "," + self.format(self.printer(self.preinput)) + "," + self.format(self.printer(self.preoutput)) \
                       + "\\rangle \\rightarrow(g," + self.format(self.printer(self.poststack)) + "," + self.format(self.printer(self.postinput)) + "," + self.format(self.printer(self.postoutput))+")$}\n"
                # Delete
                if self.a[0] == "%":
                    return "\\AxiomC{}\n\\RightLabel{$[del^{ns}]$}\n\\UnaryInfC{$\\langle  "+ self.format(self.a) + ", g," + self.format(self.printer(self.prestack)) + "," + self.format(self.printer(self.preinput)) + "," + self.format(self.printer(self.preoutput)) \
                       + "\\rangle \\rightarrow(g," + self.format(self.printer(self.poststack)) + "," + self.format(self.printer(self.postinput)) + "," + self.format(self.printer(self.postoutput))+")$}\n"
                # Rotate
                if self.a[0] == "@":
                    return "\\AxiomC{}\n\\RightLabel{$[rot^{ns}]$}\n\\UnaryInfC{$\\langle  "+ self.format(self.a) + ", g," + self.format(self.printer(self.prestack)) + "," + self.format(self.printer(self.preinput)) + "," + self.format(self.printer(self.preoutput)) \
                       + "\\rangle \\rightarrow(g," + self.format(self.printer(self.poststack)) + "," + self.format(self.printer(self.postinput)) + "," + self.format(self.printer(self.postoutput))+")$}\n"
                # Pick

                ### 2. VARIABLES
                # Assign
                if self.a[0] == ":":
                    return "\\AxiomC{}\n\\RightLabel{$[assign^{ns}]$}\n\\UnaryInfC{$\\langle  "+ self.format(self.a) + ", g," + self.format(self.printer(self.prestack)) + "," + self.format(self.printer(self.preinput)) + "," + self.format(self.printer(self.preoutput)) \
                       + "\\rangle \\rightarrow(g\pass{" + self.format(str(self.waarde)) + "}{" + self.format(self.variabele) + "}"+ "," + self.format(self.printer(self.poststack)) + "," + self.format(self.printer(self.postinput)) + "," + self.format(self.printer(self.postoutput))+")$}\n"
                # Retrieve
                if self.a[0] == ";":
                    return "\\AxiomC{}\n\\RightLabel{$[retrieve^{ns}]$}\n\\UnaryInfC{$\\langle  "+ self.format(self.a) + ", g," + self.format(self.printer(self.prestack)) + "," + self.format(self.printer(self.preinput)) + "," + self.format(self.printer(self.preoutput)) \
                       + "\\rangle \\rightarrow(g," + self.format(self.printer(self.poststack)) + "," + self.format(self.printer(self.postinput)) + "," + self.format(self.printer(self.postoutput))+")$}\n"

                ### 3. LOGIC

                ### 4. OPERATORS
                # Add
                if self.a[0] == "+":
                    return "\\AxiomC{}\n\\RightLabel{$[add^{ns}]$}\n\\UnaryInfC{$\\langle  "+ self.format(self.a) + ", g," + self.format(self.printer(self.prestack)) + "," + self.format(self.printer(self.preinput)) + "," + self.format(self.printer(self.preoutput)) \
                       + "\\rangle \\rightarrow(g," + self.format(self.printer(self.poststack)) + "," + self.format(self.printer(self.postinput)) + "," + self.format(self.printer(self.postoutput))+")$}\n"
                # Subtract
                elif self.a[0] == "-":
                    return "\\AxiomC{}\n\\RightLabel{$[sub^{ns}]$}\n\\UnaryInfC{$\\langle  "+ self.format(self.a) + ", g," + self.format(self.printer(self.prestack)) + "," + self.format(self.printer(self.preinput)) + "," + self.format(self.printer(self.preoutput)) \
                       + "\\rangle \\rightarrow(g," + self.format(self.printer(self.poststack)) + "," + self.format(self.printer(self.postinput)) + "," + self.format(self.printer(self.postoutput))+")$}\n"
                # Multiply
                elif self.a[0] == "*":
                    return "\\AxiomC{}\n\\RightLabel{$[mult^{ns}]$}\n\\UnaryInfC{$\\langle  "+ self.format(self.a) + ", g," + self.format(self.printer(self.prestack)) + "," + self.format(self.printer(self.preinput)) + "," + self.format(self.printer(self.preoutput)) \
                       + "\\rangle \\rightarrow(g," + self.format(self.printer(self.poststack)) + "," + self.format(self.printer(self.postinput)) + "," + self.format(self.printer(self.postoutput))+")$}\n"
                # Divide
                elif self.a[0] == "/":
                    return "\\AxiomC{}\n\\RightLabel{$[div^{ns}]$}\n\\UnaryInfC{$\\langle  "+ self.format(self.a) + ", g," + self.format(self.printer(self.prestack)) + "," + self.format(self.printer(self.preinput)) + "," + self.format(self.printer(self.preoutput)) \
                       + "\\rangle \\rightarrow(g," + self.format(self.printer(self.poststack)) + "," + self.format(self.printer(self.postinput)) + "," + self.format(self.printer(self.postoutput))+")$}\n"

                # Negative
                elif self.a[0] == "_":
                    return "\\AxiomC{}\n\\RightLabel{$[neg^{ns}]$}\n\\UnaryInfC{$\\langle  "+ self.format(self.a) + ", g," + self.format(self.printer(self.prestack)) + "," + self.format(self.printer(self.preinput)) + "," + self.format(self.printer(self.preoutput)) \
                       + "\\rangle \\rightarrow(g," + self.format(self.printer(self.poststack)) + "," + self.format(self.printer(self.postinput)) + "," + self.format(self.printer(self.postoutput))+")$}\n"
                # Equals
                elif self.a[0] == "=":
                    return "\\AxiomC{}\n\\RightLabel{$[eq^{ns}]$}\n\\UnaryInfC{$\\langle  "+ self.format(self.a) + ", g," + self.format(self.printer(self.prestack)) + "," + self.format(self.printer(self.preinput)) + "," + self.format(self.printer(self.preoutput)) \
                       + "\\rangle \\rightarrow(g," + self.format(self.printer(self.poststack)) + "," + self.format(self.printer(self.postinput)) + "," + self.format(self.printer(self.postoutput))+")$}\n"
                # Inverse
                elif self.a[0] == "~":
                    return "\\AxiomC{}\n\\RightLabel{$[inv^{ns}]$}\n\\UnaryInfC{$\\langle  "+ self.format(self.a) + ", g," + self.format(self.printer(self.prestack)) + "," + self.format(self.printer(self.preinput)) + "," + self.format(self.printer(self.preoutput)) \
                       + "\\rangle \\rightarrow(g," + self.format(self.printer(self.poststack)) + "," + self.format(self.printer(self.postinput)) + "," + self.format(self.printer(self.postoutput))+")$}\n"
                # Greater than
                elif self.a[0] == ">":
                    return "\\AxiomC{}\n\\RightLabel{$[greater^{ns}]$}\n\\UnaryInfC{$\\langle  "+ self.format(self.a) + ", g," + self.format(self.printer(self.prestack)) + "," + self.format(self.printer(self.preinput)) + "," + self.format(self.printer(self.preoutput)) \
                       + "\\rangle \\rightarrow(g," + self.format(self.printer(self.poststack)) + "," + self.format(self.printer(self.postinput)) + "," + self.format(self.printer(self.postoutput))+")$}\n"
                # And
                elif self.a[0] == "&":
                    return "\\AxiomC{}\n\\RightLabel{$[and^{ns}]$}\n\\UnaryInfC{$\\langle  "+ self.format(self.a) + ", g," + self.format(self.printer(self.prestack)) + "," + self.format(self.printer(self.preinput)) + "," + self.format(self.printer(self.preoutput)) \
                       + "\\rangle \\rightarrow(g," + self.format(self.printer(self.poststack)) + "," + self.format(self.printer(self.postinput)) + "," + self.format(self.printer(self.postoutput))+")$}\n"
                # Or
                elif self.a[0] == "|":
                    return "\\AxiomC{}\n\\RightLabel{$[or^{ns}]$}\n\\UnaryInfC{$\\langle  "+ self.format(self.a) + ", g," + self.format(self.printer(self.prestack)) + "," + self.format(self.printer(self.preinput)) + "," + self.format(self.printer(self.preoutput)) \
                       + "\\rangle \\rightarrow(g," + self.format(self.printer(self.poststack)) + "," + self.format(self.printer(self.postinput)) + "," + self.format(self.printer(self.postoutput))+")$}\n"

                ### 6. Input/output
                # Getchar
                if self.a[0] == "^":
                    return "\\AxiomC{}\n\\RightLabel{$[getchar^{ns}]$}\n\\UnaryInfC{$\\langle  "+ self.format(self.a) + ", g," + self.format(self.printer(self.prestack)) + "," + self.format(self.printer(self.preinput)) + "," + self.format(self.printer(self.preoutput)) \
                       + "\\rangle \\rightarrow(g," + self.format(self.printer(self.poststack)) + "," + self.format(self.printer(self.postinput)) + "," + self.format(self.printer(self.postoutput))+")$}\n"
                # Comment
                if self.a[0] == "{":
                    return "\\AxiomC{}\n\\RightLabel{$[comment^{ns}]$}\n\\UnaryInfC{$\\langle  "+ self.format(self.a) + ", g," + self.format(self.printer(self.prestack)) + "," + self.format(self.printer(self.preinput)) + "," + self.format(self.printer(self.preoutput)) \
                       + "\\rangle \\rightarrow(g," + self.format(self.printer(self.poststack)) + "," + self.format(self.printer(self.postinput)) + "," + self.format(self.printer(self.postoutput))+")$}\n"
                # Printchar
                if self.a[0] == ",":
                    return "\\AxiomC{}\n\\RightLabel{$[printchar^{ns}]$}\n\\UnaryInfC{$\\langle  "+ self.format(self.a) + ", g," + self.format(self.printer(self.prestack)) + "," + self.format(self.printer(self.preinput)) + "," + self.format(self.printer(self.preoutput)) \
                       + "\\rangle \\rightarrow(g," + self.format(self.printer(self.poststack)) + "," + self.format(self.printer(self.postinput)) + "," + self.format(self.printer(self.postoutput))+")$}\n"
                # Printnum
                if self.a[0] == ".":
                    return "\\AxiomC{}\n\\RightLabel{$[printnum^{ns}]$}\n\\UnaryInfC{$\\langle  "+ self.format(self.a) + ", g," + self.format(self.printer(self.prestack)) + "," + self.format(self.printer(self.preinput)) + "," + self.format(self.printer(self.preoutput)) \
                       + "\\rangle \\rightarrow(g," + self.format(self.printer(self.poststack)) + "," + self.format(self.printer(self.postinput)) + "," + self.format(self.printer(self.postoutput))+")$}\n"
                # Getchar
                if self.a[0] == "\"":
                    return "\\AxiomC{}\n\\RightLabel{$[string^{ns}]$}\n\\UnaryInfC{$\\langle  "+ self.format(self.a) + ", g," + self.format(self.printer(self.prestack)) + "," + self.format(self.printer(self.preinput)) + "," + self.format(self.printer(self.preoutput)) \
                       + "\\rangle \\rightarrow(g," + self.format(self.printer(self.poststack)) + "," + self.format(self.printer(self.postinput)) + "," + self.format(self.printer(self.postoutput))+")$}\n"

                # Push
                else:
                    return "\\AxiomC{}\n\\RightLabel{$[push^{ns}]$}\n\\UnaryInfC{$\\langle  "+ self.format(self.a) + ", g," + self.format(self.printer(self.prestack)) + "," + self.format(self.printer(self.preinput)) + "," + self.format(self.printer(self.preoutput)) \
                       + "\\rangle \\rightarrow(g," + self.format(self.printer(self.poststack)) + "," + self.format(self.printer(self.postinput)) + "," + self.format(self.printer(self.postoutput))+")$}\n"
                # return "\\AxiomC{$\\langle  "+ self.format(self.a) + "," + self.format(self.prevariables) + "," + self.format(self.printer(self.prestack)) + "," + self.format(self.printer(self.preinput)) + "," + self.format(self.printer(self.preoutput)) \
                #        + "\\rangle \\rightarrow(" + self.format(self.postvariables) + "," + self.format(self.printer(self.poststack)) + "," + self.format(self.printer(self.postinput)) + "," + self.format(self.printer(self.postoutput))+")$}\n"

    def makeWhileb(self,i):
        if i+2<=len(self.children):
            return self.children[i].printbuss() + self.children[i+1].printbuss() +  self.makeWhileb(i+2) \
            + "\\RightLabel{$[while^{ns}_{tt}]$}\n" \
            + "\TrinaryInfC{$\\langle " \
            + self.format(self.a) + self.format(self.statement[len(self.a):]) + "," + self.format(self.prevariables) + "," + self.format(self.printer(self.prestack)) + "," + self.format(self.printer(self.preinput)) + "," + self.format(self.printer(self.preoutput)) \
            + "\\rangle \\rightarrow(" + self.format(self.postvariables) + "," + self.format(self.printer(self.poststack)) + "," + self.format(self.printer(self.postinput)) + "," + self.format(self.printer(self.postoutput))\
            + ")$}\n"
        else:
            return self.children[i].printbuss() + "\\RightLabel{$[while^{ns}_{ff}]$}\n\\UnaryInfC{$\\langle "+ self.format(self.a) + "," + self.format(self.prevariables) + "," + self.format(self.printer(self.prestack)) + "," + self.format(self.printer(self.preinput)) + "," + self.format(self.printer(self.preoutput)) \
                       + "\\rangle \\rightarrow(" + self.format(self.postvariables) + "," + self.format(self.printer(self.poststack)) + "," + self.format(self.printer(self.postinput)) + "," + self.format(self.printer(self.postoutput))+">$}\n"

    def whileBody(self):
        return self.format(self.a) + self.format(self.statement[len(self.a):])

    def __repr__(self):
        return  self.statement

    def format(self,string):
        string = string.replace(str('\\'),"\\backslash")
        string = string.replace(str('^'),"$\\textasciicircum$")
        for char in "$_&%#":
            string = string.replace(str(char),"\\"+str(char))
        return string.replace(str(' '),"\\:")

    def printer(self,lister,i=-1):
        if(i==-1):
            i = len(lister)-1
            if len(lister) == 0:
                return "(,)"
        if i == 0:
            return "(" + str(lister[i]) + ",(,))"
        return "(" + str(lister[i]) + "," + self.printer(lister,i-1) + ")"