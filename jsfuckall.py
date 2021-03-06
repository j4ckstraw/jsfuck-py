#!/usr/bin/env python
#coding:utf-8


USE_CHAR_CODE = "USE_CHAR_CODE"
MIN,MAX = 32,126   # 可见字符范围

SIMPLE = {
'false':      '![]',
'true':       '!![]',
'undefined':  '[][[]]',
'NaN':        '+[![]]',
'Infinity':   '+(+!+[]+(!+[]+[])[!+[]+!+[]+!+[]]+[+!+[]]+[+[]]+[+[]]+[+[]])' # +"1e1000"
}

CONSTRUCTORS = {
'Array':    '[]',
'Number':   '(+[])',
'String':   '([]+[])',
'Boolean':  '(![])',
'Function': '[]["fill"]',
'RegExp':   'Function("return/"+false+"/")()'
}

MAPPING = {
'a':   '(false+"")[1]',
'b':   '([]["entries"]()+"")[2]',
'c':   '([]["fill"]+"")[3]',
'd':   '(undefined+"")[2]',
'e':   '(true+"")[3]',
'f':   '(false+"")[0]',
'g':   '(false+[0]+String)[20]',
'h':   '(+(101))["to"+String["name"]](21)[1]',
'i':   '([false]+undefined)[10]',
'j':   '([]["entries"]()+"")[3]',
'k':   '(+(20))["to"+String["name"]](21)',
'l':   '(false+"")[2]',
'm':   '(Number+"")[11]',
'n':   '(undefined+"")[1]',
'o':   '(true+[]["fill"])[10]',
'p':   '(+(211))["to"+String["name"]](31)[1]',
'q':   '(+(212))["to"+String["name"]](31)[1]',
'r':   '(true+"")[1]',
's':   '(false+"")[3]',
't':   '(true+"")[0]',
'u':   '(undefined+"")[0]',
'v':   '(+(31))["to"+String["name"]](32)',
'w':   '(+(32))["to"+String["name"]](33)',
'x':   '(+(101))["to"+String["name"]](34)[1]',
'y':   '(NaN+[Infinity])[10]',
'z':   '(+(35))["to"+String["name"]](36)',

'A':   '(+[]+Array)[10]',
'B':   '(+[]+Boolean)[10]',
'C':   'Function("return escape")()(("")["italics"]())[2]',
'D':   'Function("return escape")()([]["fill"])["slice"]("-1")',
'E':   '(RegExp+"")[12]',
'F':   '(+[]+Function)[10]',
'G':   '(false+Function("return Date")()())[30]',
'H':   USE_CHAR_CODE,
'I':   '(Infinity+"")[0]',
'J':   USE_CHAR_CODE,
'K':   USE_CHAR_CODE,
'L':   USE_CHAR_CODE,
'M':   '(true+Function("return Date")()())[30]',
'N':   '(NaN+"")[0]',
'O':   '(NaN+Function("return{}")())[11]',
'P':   USE_CHAR_CODE,
'Q':   USE_CHAR_CODE,
'R':   '(+[]+RegExp)[10]',
'S':   '(+[]+String)[10]',
'T':   '(NaN+Function("return Date")()())[30]',
'U':   '(NaN+Function("return{}")()["to"+String["name"]]["call"]())[11]',
'V':   USE_CHAR_CODE,
'W':   USE_CHAR_CODE,
'X':   USE_CHAR_CODE,
'Y':   USE_CHAR_CODE,
'Z':   USE_CHAR_CODE,

' ':   '(NaN+[]["fill"])[11]',
'!':   USE_CHAR_CODE,
'"':   '("")["fontcolor"]()[12]',
'#':   USE_CHAR_CODE,
'$':   USE_CHAR_CODE,
'%':   'Function("return escape")()([]["fill"])[21]',
'&':   '("")["link"](0+")[10]',
'\'':  USE_CHAR_CODE,
'(':   '(undefined+[]["fill"])[22]',
')':   '([0]+false+[]["fill"])[20]',
'*':   USE_CHAR_CODE,
'+':   '(+(+!+[]+(!+[]+[])[!+[]+!+[]+!+[]]+[+!+[]]+[+[]]+[+[]])+[])[2]',
',':   '([]["slice"]["call"](false+"")+"")[1]',
'-':   '(+(.+[0000000001])+"")[2]',
'.':   '(+(+!+[]+[+!+[]]+(!![]+[])[!+[]+!+[]+!+[]]+[!+[]+!+[]]+[+[]])+[])[+!+[]]',
'/':   '(false+[0])["italics"]()[10]',
':':   '(RegExp()+"")[3]',
';':   '("")["link"](")[14]',
'<':   '("")["italics"]()[0]',
'=':   '("")["fontcolor"]()[11]',
'>':   '("")["italics"]()[2]',
'?':   '(RegExp()+"")[2]',
'@':   USE_CHAR_CODE,
'[':   '([]["entries"]()+"")[0]',
'\\':  USE_CHAR_CODE,
']':   '([]["entries"]()+"")[22]',
'^':   USE_CHAR_CODE,
'_':   USE_CHAR_CODE,
'`':   USE_CHAR_CODE,
'{':   '(true+[]["fill"])[20]',
'|':   USE_CHAR_CODE,
'}':   '([]["fill"]+"")["slice"]("-1")',
'~':   USE_CHAR_CODE
}

GLOBAL = 'Function("return this")()'

import re

def fillMissingChars():
    '''
    将 USE_CHAR_CODE 替换掉
    '''
    for key in MAPPING:
        if MAPPING[key] == USE_CHAR_CODE:
            s = str(hex(ord(key)))[2:]
            string = '''("%"+({})+"{}")'''.format(\
                re.findall('\d+',s)[0]       if re.findall('\d',s)     else "",\
                re.findall('[a-zA-Z]+',s)[0] if re.findall('[a-zA-Z]',s) else "")
            MAPPING[key] = """Function("return unescape")()""" + string

def fillMissingDigits():
    '''
    填充MAPPING中 0-9 的数字
    '''
    for num in xrange(10):
        output = "+[]"
        if num > 0:
            output = "+!" + output
        for i in range(1,num):
            output = "+!+[]" + output
        if num > 1:
            output = output[1:]
        MAPPING[str(num)] = "[" + output + "]"


class replaceMap(object):
    '''
    替换 MAPPING中的
    '''
    def replace(self,pattern,replacement):
        self.value = re.sub(pattern,replacement,self.value)

    def digitReplacer(self,x):
        # if x.group() == "[0]":
        #     print "aaaaaaaaaaaaaaaaaaaaaaa"
        #     exit(10)
        x = re.findall(r'\d',x.group())[0]     
        ## 正则表达式 分组 
        ## python 匹配 \[(\d)\]   例如 [0]  并不是 选中分组\d 即0   而是 [0]
        return MAPPING[x]
    
    def numberReplacer(self,y):
        values = list(y.group())
        values.reverse()
        head = int(values.pop())
        values.reverse()
        output = "+[]"
    
        if head > 0:
            output = "+!" + output
        for i in range(1,head):
            output = "+!+[]" + output
        if head > 1:
            output = output[1:]            
        output = [output] + values
        output = "+".join(output)
        output = re.sub(r'\d',self.digitReplacer,output)
        return output

    def __init__(self):
        self.character = ""
        self.value = ""
        self.original = ""

        for i in range(MIN,MAX+1):
            # character = String.fromCharCode(i);
            self.character = chr(i)
            self.value = MAPPING[self.character]
            # print self.value
            if not self.value:
                continue
            self.original = self.value
    
            # for (key in CONSTRUCTORS){
            for key in CONSTRUCTORS:
                # replace("\\b" + key, CONSTRUCTORS[key] + '["constructor"]');
                self.value = re.sub(r'\b'+key,CONSTRUCTORS[key]+'["constructor"]',self.value)
            # print self.value
            # for (key in SIMPLE){
              # replace(key, SIMPLE[key]);
            # }
            for key in SIMPLE:
                self.value = re.sub(key,SIMPLE[key],self.value)
            # print self.value
    
            # replace('(\\d\\d+)', numberReplacer);
            self.replace('(\\d\\d+)',self.numberReplacer)
            # print '1'*8,self.value
            # value = re.sub(r'\d\d+',numberReplacer,value)
            # replace('\\((\\d)\\)', digitReplacer);
            self.replace('\\((\\d)\\)',self.digitReplacer)
            # print '2'*8,self.value

            # value = re.sub(r'\((\d)\)',digitReplacer,value)
            # replace('\\[(\\d)\\]', digitReplacer);
            self.replace('\\[(\\d)\\]',self.digitReplacer)   ## python 和 js中正则表达式 () 有区别
            # print '3'*8,self.value

            # value = re.sub(r'\[(\d)\]',digitReplacer,value)
            # replace("GLOBAL", GLOBAL);
            # replace('\\+""', "+[]");
            # replace('""', "[]+[]");
            # self.repalce("GLOBAL",GLOBAL)
            # self.replace('\\+""',"+[]")
            # self.replace('""',"[]+[]")
            self.value = re.sub("GLOBAL",GLOBAL,self.value)
            self.value = re.sub(r'\+""',"+[]",self.value)
            self.value = re.sub('\"\"',"[]+[]",self.value)
    
            MAPPING[self.character] = self.value;

class replaceStrings(object):
    '''
    替换 字符串
    '''
    def findMissing(self):
        self.missing = {}
        done = False
        for m in MAPPING:
            value = MAPPING[m]
            if re.search(self.regEx,value):
                ### Python offers two different primitive operations based on regular expressions:
                ### re.match() checks for a match only at the beginning of the string,
                ### while re.search() checks for a match anywhere in the string (this is what Perl does by default).
                self.missing[m] = value
                done = True
        # print "DONE"*8
        # print done
        return done
    
    def mappingReplacer(self,b):
        return "+".join(list(b.group().strip('""')))
        # return "+".join(list(b.group()))

        ## 去掉 “”

    def valueReplacer(self,c):
        c = c.group()
        return c if self.missing.has_key(c) else MAPPING[c]

        # print 'c:',c
        # print type(c)
        # raw_input()
        # return c if self.missing[c] else MAPPING[c]
        ## js  missing[c] 不存在 为undefined
        ## python missing[c] 不存在 会报错

    def __init__(self):
        self.regEx = ur'[^\[\]\(\)\!\+]{1}'
        self.missing = {}
        self.count = MAX - MIN

        for m in MAPPING:
            MAPPING[m] = re.sub(r'\"([^\"]+)\"',self.mappingReplacer,MAPPING[m])
        
        # print "TEST".center(79,'+')
        # print MAPPING['~']
        # print MAPPING['0']
        # print MAPPING['a']
        # print MAPPING[']']
        # print MAPPING['H']

        while self.findMissing():
            for m in self.missing:
                value = MAPPING[m]
                value = re.sub(self.regEx,self.valueReplacer,value)
                MAPPING[m]      = value
                self.missing[m] = value
                ## for self.missing  此处修改了missing的值  but ok
            self.count -= 1
            if self.count == 0:
                print "Could not compile the following chars:", self.missing
                break

class encode(object):
    def encodeReplacer(self,c):
        c = c.group()
        replacement = SIMPLE.has_key(c)
        if replacement:
            self.output.append("[" + SIMPLE[c] + "]+[]")
        else:
            replacement = MAPPING.has_key(c)
            if replacement:
                self.output.append(MAPPING[c])
            else:
                replacement ="([]+[])[" + encode("constructor") + "]" +\
                "[" + encode("fromCharCode") + "]" +\
                "(" + encode(str(ord(c[0]))) + ")"

                self.output.append(replacement)
                MAPPING[c] = replacement
    
    def __init__(self,input,wrapWithEval = False,runInParentScope = False):
        self.output = []
        self.input = input
        self.wrapWithEval = wrapWithEval
        self.runInParentScope = runInParentScope

    def encode(self):
        if not self.input:
            return ""
        
        r = ""
        for i in SIMPLE:
            r += i + "|"
        r += "."
    
        # self.input = re.sub(r,self.encodeReplacer,self.input)
        re.sub(r,self.encodeReplacer,self.input)
        ## 此处未改变input的值 后面 re.search 因为会判断input 是否为数字 

    
        self.output = "+".join(self.output)
        # print self.input
        # print self.output
        if re.search(r'^\d$',self.input):
            # print "digital"
            self.output += "+[]"
    
        if self.wrapWithEval:
            if self.runInParentScope:
                self.output = "[][" + encode("fill").encode() + "]" +\
                "[" + encode("constructor").encode() + "]" +\
                "(" + encode("return eval").encode() +  ")()" +\
                "(" + self.output + ")"
            else :
                self.output = "[][" + encode("fill").encode() + "]" +\
                "[" + encode("constructor").encode() + "]" +\
                "(" + self.output + ")()"
    
        return self.output 
        # print self.output



# def encodeReplacer(c):
#     c = c.group()
#     replacement = SIMPLE.has_key(c)
#     if replacement:
#         output.append("[" + SIMPLE[c] + "]+[]")
#     else:
#         replacement = MAPPING.has_key(c)
#         if replacement:
#             output.append(MAPPING[c])
#         else:
#             replacement ="([]+[])[" + encode("constructor") + "]" +\
#             "[" + encode("fromCharCode") + "]" +\
#             "(" + encode(c.charCodeAt(0) + "") + ")"
#             output.append(replacement)
#             MAPPING[c] = replacement
    

# def encode(input,wrapWithEval = False, runInParentScope = False):
#     output = []
#     if not input:
#         return ""

#     r = ""
#     for i in SIMPLE:
#         r += i + "|"
#     r += "."

#     input = re.sub(r,encodeReplacer,input)
#     output = "+".join(output)
#     if re.search(r'^\d$',input):
#         output += "+[]"
#     if wrapWithEval:
#         if runInParentScope:
#             output = "[][" + encode("fill") + "]" +\
#             "[" + encode("constructor") + "]" +\
#             "(" + encode("return eval") +  ")()" +\
#             "(" + output + ")"
#         else :
#             output = "[][" + encode("fill") + "]" +\
#             "[" + encode("constructor") + "]" +\
#             "(" + output + ")()"
#     return output 
#     # print output

if __name__ == '__main__':
    fillMissingChars()
    fillMissingDigits()
    replaceMap()
    replaceStrings()

    # for i in sorted(MAPPING):
    #     print i,MAPPING[i]

    # print MAPPING['~']
    # print MAPPING['0']
    # print MAPPING['a']
    # print MAPPING[']']
    # print MAPPING['H']

    string = 'global'
    # print encode(string,True,True).encode()
    print encode(string).encode()
