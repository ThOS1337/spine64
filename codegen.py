registers = {
	"ret": 0,   # rax
	"cnt": 1,   # rcx
	"dta": 2,   # rdx
	"r1":  3,   # rbx
	"stp": 4,   # rsp
	"sbp": 5,   # rbp
	"src": 6,   # rsi
	"dst": 7,   # rdi
	"r2":  8,   # r8
	"r3":  9,   # r9
	"r4":  10,  # r10
	"r5":  11,  # r11
	"r6":  12,  # r12
	"r7":  13,  # r13
	"r8":  14,  # r14
	"r9":  15,  # r15
}

class CodeGen:
	def __init__(self):
		self.output = bytearray()
		self.symbols = {}      # label name -> address
		self.patches = []      # (offset_in_output, label_name) to fix later
		self.origin = 0        # set by OriginNode, default 0
		self.aliases = {}      # alias name -> register name
	def currentAddr(self):
		return self.origin + len(self.output)
	def emitPass(self, ast):
		# empty
	def patchPass(self):
		# empty
	def outputPass(self, filename):
		# empty
var = currentAddr()
print(var)