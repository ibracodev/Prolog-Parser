"""
(1) <program>        -> <clause-list> <query> | <query>
(2) <clause-list>    -> <clause> | <clause> <clause-list>
(3) <clause>         -> <predicate> . | <predicate> :- <predicate-list> .
(4) <query>          -> ?- <predicate-list> .
(5) <predicate-list> -> <predicate> | <predicate> , <predicate-list>
(6) <predicate>      -> <atom> | <atom> ( <term-list> )
(7) <term-list>      -> <term> | <term> , <term-list>
(8) <term>           -> <atom> | <variable> | <structure> | <numeral>
(9) <structure>      -> <atom> ( <term-list> )
(10)(not tested) <atom>           -> <small-atom> | ' <string> '
(11)√ <small-atom>     -> <lowercase-char> | <lowercase-char> <character-list>
(12)√ <variable>       -> <uppercase-char> | <uppercase-char> <character-list>
(13) <character-list> -> <alphanumeric> | <alphanumeric> <character-list>
(14) <alphanumeric>   -> <lowercase-char> | <uppercase-char> | <digit>
(15)√ <lowercase-char> -> a | b | c | ... | x | y | z
(16)√ <uppercase-char> -> A | B | C | ... | X | Y | Z | _
(17)√ <numeral>        -> <digit> | <digit> <numeral>
(18)√ <digit>          -> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
(19) <string>         -> <character> | <character> <string>
(20) <character>      -> <alphanumeric> | <special>
(21)√ <special>        -> + | - | * | / | \ | ^ | ~ | : | . | ? | | # | $ | & 
"""

"""
BAD PROGRAMMING STYLE C-STYLE
USE GLOBALS FIRST

LATER ADJUST TO USE FUNCTIONS
"""


from pathlib import Path
errorFile = open("ErrorFile.txt", 'w')

class CharClasses(): #this class defines constants to each character
    LOWER  = 0
    UPPER  = 1
    DIGIT   = 2
    SPECIAL = 3
    EOF = 38
    UNKNOWN = 99
    

class Tokens(): #this class defines constants of the tokens when identified
    INT_LIT     = 10 
    IDENT       = 11 
    ASSIGN_OP   = 20
    ADD_OP      = 21
    SUB_OP      = 22
    MULT_OP     = 23
    DIV_OP      = 24
    LEFT_PAREN  = 25
    RIGHT_PAREN = 26
    BACKSLASH   = 27
    HAT         = 28
    TILDA       = 29
    COLON       = 30
    DOT         = 31
    QUESTION    = 32
    SPACE       = 33
    HASH        = 34
    DOLLAR      = 35
    AMP         = 36
    COMMA       = 37
    SMALLATOM   = 38
    VARIABLE    = 39
    STRING      = 40
    EOF         = 41
    SINGLEQUOTE = 42
    COLONDASH   = 43
    QUERYSTART  = 44
    ATOM        = 45
    UNKNOWN     = 46



charClass = 99 # integer denoting the code of the current char
lexeme = "" #string denoting the lexeme
nextChar = '' #character denoting the next character
nextToken = 0 #integer denoting the next token
line = 1
file = None #holds the current file
special = ['+', '-', '*', '/', '\\', '^', '~', ':', '.', '?',' ', '#', '$', '&']
isError = False #denotes if program is faulty or not

#Lexical Analaysis

def addChar() -> None: #this function adds a character to the lexeme
    globals()['lexeme'] += nextChar

def getChar() -> None: #this function reads a single character and identifies its character class
    global nextChar 
    global file
    global charClass
    nextChar = file.read(1) #reads one character
    print(nextChar)
    if nextChar:
        #print('value of NEXTCHAR', nextChar)
        if str.isalpha(nextChar) or nextChar == '_': #if it is an alphabet or contains an underscore then it is rule 15 or 16
            if str.islower(nextChar): #if lower then its rule 15
                charClass = CharClasses.LOWER
            else: #if its underscore or upper then its rule 16
                charClass = CharClasses.UPPER
        elif str.isdigit(nextChar): # if its a digit then go for rule 18
            charClass = CharClasses.DIGIT
        
        else: #else go for rule 21 because its special
            if nextChar == '\n':
                globals()['line']+=1
            if nextChar in special:
                charClass = CharClasses.SPECIAL
            else:
                charClass = CharClasses.UNKNOWN
                
    else: 
        charClass = CharClasses.EOF
      

        

def getNonBlank() -> None: #skips all white space for example: int x     =     6; #this will skip the spaces in between the tokens
    global nextChar
    while(str.isspace(nextChar)): # as long as there is a whitespace, get the next character.
        getChar()

def lex() -> int: 
    getNonBlank()
    global lexeme
    global charClass
    global nextToken
    global charClass
    lexeme = ""
    match charClass:
        case CharClasses.DIGIT: # <numeral> mimics rule 17
            addChar()
            getChar()
            while(charClass == CharClasses.DIGIT):
                addChar()
                getChar()
            nextToken = Tokens.INT_LIT

        case CharClasses.LOWER: # <SMALLATOM> mimics rule 11
            addChar()
            getChar()
            while(charClass == CharClasses.LOWER or charClass == CharClasses.UPPER or charClass == CharClasses.DIGIT):
                addChar()
                getChar()

            nextToken = Tokens.SMALLATOM
            

        #defining a small atom could be an issue here because the token value is of a small atom which causes problems for the alphanumeric function - ibra 6/5/22
        
        case CharClasses.UPPER: # <VARIABLE> mimics rule 12
            
            addChar()
            getChar()
            while(charClass == CharClasses.LOWER or charClass == CharClasses.UPPER or charClass == CharClasses.DIGIT):
                addChar()
                getChar()

            nextToken = Tokens.VARIABLE


        case CharClasses.SPECIAL:
            print(nextChar)
            lookup(globals()['nextChar'])
            getChar()
            if nextToken == Tokens.COLON:
                
                lookup(globals()['nextChar'])
                if nextToken == Tokens.SUB_OP:
                    getChar()
                    nextToken = Tokens.COLONDASH
            elif nextToken == Tokens.QUESTION:
                
                lookup(globals()['nextChar'])
                if nextToken == Tokens.SUB_OP:
                    getChar()
                    nextToken = Tokens.QUERYSTART
            

                    


        case CharClasses.UNKNOWN: #for paranthesis and other special tokens like +,-,:,*,/ (i forgot to add brackets, are they needed too?)
            lookup(globals()['nextChar'])
            getChar()
            if nextToken == Tokens.SINGLEQUOTE:
                addChar()
                getChar()
                while(charClass == CharClasses.LOWER or charClass == CharClasses.UPPER or charClass == CharClasses.DIGIT or (charClass == CharClasses.SPECIAL and nextChar != '\'')):
                    addChar()
                    getChar()
                if nextChar == "\'":
                    addChar()
                    getChar()
                    nextToken = Tokens.ATOM
        
            
        case CharClasses.EOF: #for eof (from the textbook)
            nextToken = Tokens.EOF
            lexeme = "EOF"

    if nextToken == Tokens.SMALLATOM:
        nextToken = Tokens.ATOM;
    print(f"Next token is: {nextToken}, Next lexeme is {lexeme}\n");
    return nextToken


def lookup(ch) -> int: #lookup function for special characters
    global nextToken
    match ch:
        case '(':
            addChar()
            nextToken = Tokens.LEFT_PAREN
        case ')':
            addChar()
            nextToken = Tokens.RIGHT_PAREN
        case '+':
            addChar()
            nextToken = Tokens.ADD_OP
        case '-':
            addChar()
            nextToken = Tokens.SUB_OP
        case '*':
            addChar()
            nextToken = Tokens.MULT_OP
        case '/':
            addChar()
            nextToken = Tokens.DIV_OP
        case '\\':
            addChar()
            nextToken = Tokens.BACKSLASH
        case '^':
            addChar()
            nextToken = Tokens.HAT
        case '~':
            addChar()
            nextToken = Tokens.TILDA
        case ':':
            addChar()
            nextToken = Tokens.COLON
        case '.':
            addChar()
            nextToken = Tokens.DOT
        case '?':
            addChar()
            nextToken = Tokens.QUESTION
        case ' ':
            addChar()
            nextToken = Tokens.SPACE
        case '#':
            addChar()
            nextToken = Tokens.HASH
        case '$':
            addChar()
            nextToken = Tokens.DOLLAR
        case '&':
            addChar()
            nextToken = Tokens.AMP
        case ',':
            addChar()
            nextToken = Tokens.COMMA
        case "\'":
            addChar()
            nextToken = Tokens.SINGLEQUOTE
        case _:
            addChar()
            nextToken = Tokens.UNKNOWN

    return nextToken


#-----------------------------------------Syntax Analysis--------------------------------------


#defining parsing functions here (note: there is a hierarchy and by the end program() is the only function we should be calling) - ibra 6/5/22
'(1) <program>        -> <clause-list> <query> | <query>' # <clause-list>? <query>
def program():
    print("enter program")
    if nextToken == Tokens.QUERYSTART:
        query()
    else:
        clauselist()
        query()

    print("exit program")




'(2) <clause-list>    -> <clause> | <clause> <clause-list>' # [clause] #we called lex once
'(3) <clause>         -> <predicate> . | <predicate> :- <predicate-list> .'
'(5) <predicate-list> -> <predicate> | <predicate> , <predicate-list>'
'(6) <predicate>      -> <atom> | <atom> ( <term-list> )'
def clauselist():
    print("enter clause list") 
    clause()
    while nextToken == Tokens.ATOM: 
        #lex()
        clause() #one clause for now
    print("exit clause list")
   




'(3) <clause>         -> <predicate> . | <predicate> :- <predicate-list> .'
def clause():
    print("enter clause")
    predicate()
    if nextToken == Tokens.DOT:
        lex()
    elif nextToken == Tokens.COLONDASH:
        lex()
        predicatelist()
        if nextToken == Tokens.DOT:
            lex()
        else:
            print(f'error in line {line}, expected a .')
            errorFile.write(f'error in line {line}, expected a .\n')
            globals()['isError'] = True
            if nextToken == Tokens.ATOM:
                clause()
            elif nextToken == Tokens.QUERYSTART:
                return
    else:
        print(f'error in line {line}, expected a . or :-')
        errorFile.write(f'error in line {line}, expected a . or :-\n')
        globals()['isError'] = True
        if nextToken == Tokens.ATOM:
            clause()
        elif nextToken == Tokens.QUERYSTART:
            return
    print("exit clause")




'(4) <query>          -> ?- <predicate-list>'
def query():

    print("enter query")
    global nextToken
    print(nextToken)
    if nextToken == Tokens.QUERYSTART:
        lex()
        predicatelist()
    else:
        print(f'error in line {line}, expected a ?-')
        errorFile.write(f'error in line {line}, expected a ?-\n')
        globals()['isError'] = True
    print("exit query")





'(5) <predicate-list> -> <predicate> | <predicate> , <predicate-list>' # predicate {,predicate}
def predicatelist():
    global nextToken
    print("enter predicate list")
    predicate()
    while nextToken == Tokens.COMMA:
        lex()
        predicate()


    print("exit predicate list")




'(6) <predicate>      -> <atom> | <atom> ( <term-list> )' # atom [(<term-list>)]
def predicate():
    print("enter predicate")
    if nextToken == Tokens.ATOM:
        lex()
        if nextToken == Tokens.LEFT_PAREN:
            lex()
            termlist()
            if nextToken == Tokens.RIGHT_PAREN:
                lex()
            else:
                print(f"error in line {line}, missing right parenthesis")
                errorFile.write(f"error in line {line}, missing right parenthesis\n")
                globals()['isError'] = True
                while nextToken != Tokens.EOF and nextToken != Tokens.DOT and nextToken != Tokens.COMMA:
                    lex()
                
            
            
    else:
        print(f"error in line {line}, no atom")
        errorFile.write(f"error in line {line}, no atom\n")
        globals()['isError'] = True
        while nextToken != Tokens.EOF and nextToken != Tokens.DOT and nextToken != Tokens.COMMA:
            lex()

    print("exit predicate")
    




'(7) <term-list>      -> <term> | <term> , <term-list>' # term{,term} one term followed by a comma and another term
def termlist():
    print("enter termlist")
    term()
    while nextToken == Tokens.COMMA:
        lex()
        term()
    print("exit termlist")
    
    

'(8) <term>           -> <atom> | <variable> | <structure> | <numeral>'
def term():
    print("enter term")
    if nextToken == Tokens.ATOM:
        lex()
        if nextToken == Tokens.LEFT_PAREN:
            lex()
            termlist()
            if nextToken == Tokens.RIGHT_PAREN:
                pass
            else:
                print(f"error in line {line}, missing right parenthesis")
                globals()['isError'] = True
                errorFile.write(f"error in line {line}, missing right parenthesis\n")
                pass
            lex()
    elif nextToken == Tokens.VARIABLE:
        lex()
    elif nextToken == Tokens.INT_LIT:
        lex()
    else:
        print(nextToken)
        print(f"not valid term, line {line}")
        errorFile.write(f"not valid term, line {line}\n")
        globals()['isError'] = True
        while nextToken != Tokens.EOF and nextToken != Tokens.RIGHT_PAREN and nextToken != Tokens.COMMA:
            lex()            
    print("exit term")


def main():
    global file, line
    fileNum = 1
    while(Path(str(fileNum) + ".txt").is_file()):
        globals()['isError'] = False
        line = 1
        file = open(str(fileNum) + ".txt")
        errorFile.write('OPENING FILE ' + str(fileNum)+"\n")
        getChar()
        lex()
        program()
        if not globals()['isError']:
            errorFile.write('program is correct\n')
        fileNum += 1

    errorFile.close()
    return 0


main()