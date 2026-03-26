from lexer import Lexer, Token, TokenType
from dataclasses import dataclass
from ast_nodes import *

twoopnodes = {
	"add": AddNode,
	"sub": SubNode,
	"mul": MulNode,
	"smul": SMulNode,
	"div": DivNode,
	"sdiv": SDivNode,
	"awc": AwcNode,
	"swb": SwbNode,
	"and": AndNode,
	"or": OrNode,
	"xor": XorNode,
	"shl": ShlNode,
	"shr": ShrNode,
	"asr": AsrNode,
	"rotl": RotlNode,
	"rotr": RotrNode,
	"racl": RaclNode,
	"racr": RacrNode,
	"lma": LmaNode,
	"swap": SwapNode,
	"movesx": MoveSxNode,
	"movezx": MoveZxNode,
	"fadd": FaddNode,
	"fsub": FsubNode,
	"fmul": FmulNode,
	"fdiv": FdivNode,
	"fmove": FmoveNode,
	"fcmp": FcmpNode,
}

instructions = {"move", "add", "sub", "mul", "smul", "div", "sdiv", "awc", "swb", "and", "or", "xor", "not", "shl", "shr", "asr", "rotl", "rotr", "racl", "racr", "inc", "dec", "neg", "push", "pop", "call", "return", "go", "cmp", "loop", "lma", "swap", "movesx", "movezx", "fadd", "fsub", "fmul", "fdiv", "fmove", "fcmp", "set", "pr", "pw", "int", "syscall", "nope", "halt", "ioff", "ion", "reti", "rep", "extern"}

@dataclass
class Parser:
	tokens: list
	pos: int = 0
	aliases: dict = None

	def peek(self):
		if self.pos < len(self.tokens):
			return self.tokens[self.pos]
		else:
			return None

	def advance(self):
		if self.pos < len(self.tokens):
			char = self.tokens[self.pos]
			self.pos += 1
			return char
		else:
			return None

	def parse_operand(self):
		string = ''
		if self.peek().type == TokenType.LBRACKET:
			self.advance()
			while self.peek().type != TokenType.RBRACKET:
				if self.peek().value in '+*':
					string += ' ' + self.advance().value + ' '
				else:
					string += self.advance().value
			self.advance()
			return string
		else:
			val = self.advance().value
			return self.aliases.get(val, val)

	def parse_statement(self):
		char = self.peek()
		if char.type == TokenType.NEWLINE:
			self.advance()
			return None
		elif char.type == TokenType.IDENT and char.value in twoopnodes: # this is only for dst+src nodes
			self.advance() # to consume add
			dst = self.advance().value
			src = self.advance().value
			return twoopnodes[char.value](dst=dst, src=src)
		elif char.type == TokenType.IDENT and char.value == "move":
			self.advance()  # skip move
			size = None
			if self.peek().type == TokenType.DOT_SIZE:
				size = self.advance().value
			dst = self.parse_operand()
			src = self.parse_operand()
			return MoveNode(dst=dst, src=src, size=size)
		# start of no field nodes
		elif char.type == TokenType.IDENT and char.value == "return":
			self.advance()
			return ReturnNode()
		elif char.type == TokenType.IDENT and char.value == "syscall":
			self.advance()
			return SyscallNode()
		elif char.type == TokenType.IDENT and char.value == "nope":
			self.advance()
			return NopeNode()
		elif char.type == TokenType.IDENT and char.value == "halt":
			self.advance()
			return HaltNode()
		elif char.type == TokenType.IDENT and char.value == "ioff":
			self.advance()
			return IoffNode()
		elif char.type == TokenType.IDENT and char.value == "ion":
			self.advance()
			return IonNode()
		elif char.type == TokenType.IDENT and char.value == "reti":
			self.advance()
			return RetiNode()
		elif char.type == TokenType.IDENT and char.value == "rep":
			self.advance()
			kind = self.advance().value
			if kind == "movs":
				return RepMovsNode()
			else:
				return RepStosNode()
		elif char.type == TokenType.IDENT and char.value == "inc":
			self.advance()
			reg = self.parse_operand()
			return IncNode(reg=reg)
		elif char.type == TokenType.IDENT and char.value == "dec":
			self.advance()
			reg = self.parse_operand()
			return DecNode(reg=reg)
		elif char.type == TokenType.IDENT and char.value == "neg":
			self.advance()
			reg = self.parse_operand()
			return NegNode(reg=reg)
		elif char.type == TokenType.IDENT and char.value == "not":
			self.advance()
			reg = self.parse_operand()
			return NotNode(reg=reg)
		elif char.type == TokenType.IDENT and char.value == "go":
			self.advance()
			label = self.parse_operand()
			return GoNode(label=label)
		elif char.type == TokenType.IDENT and char.value == "call":
			self.advance()
			name = self.parse_operand()
			return CallNode(name=name)
		elif char.type == TokenType.IDENT and char.value == "push":
			self.advance()
			value = self.parse_operand()
			return PushNode(value=value)
		elif char.type == TokenType.IDENT and char.value == "pop":
			self.advance()
			reg = self.parse_operand()
			return PopNode(reg=reg)
		elif char.type == TokenType.IDENT and char.value == "set":
			self.advance()
			reg = self.parse_operand()
			flag = self.parse_operand()
			return SetNode(reg=reg, flag=flag)
		elif char.type == TokenType.IDENT and char.value == "pr":
			self.advance()
			dst = self.parse_operand()
			port = self.parse_operand()
			return PrNode(dst=dst, port=port)
		elif char.type == TokenType.IDENT and char.value == "pw":
			self.advance()
			port = self.parse_operand()
			src = self.parse_operand()
			return PwNode(port=port, src=src)
		elif char.type == TokenType.IDENT and char.value == "int":
			self.advance()
			number = self.parse_operand()
			return IntNode(number=number)
		elif char.type == TokenType.IDENT and char.value == "extern":
			self.advance()
			name = self.parse_operand()
			return ExternNode(name=name)
		elif char.type == TokenType.IDENT and char.value == "loop":
			self.advance()
			while self.peek().type == TokenType.NEWLINE:
				self.advance()
			self.advance()
			loop_body = []
			while self.peek().type != TokenType.IDENT or self.peek().value != "end":
				node = self.parse_statement()
				if node is not None:
					loop_body.append(node)
			self.advance()
			return LoopNode(body=loop_body)
		elif char.type == TokenType.IDENT and self.tokens[self.pos + 1].type == TokenType.COLON:
			self.advance()
			self.advance()
			return LabelNode(name=char.value)
		elif char.type == TokenType.IDENT and char.value == "cmp":
			self.advance()
			if self.peek().value in ("carry", "zero", "overflow"):
				flag = self.parse_operand()
				self.advance()
				label = self.parse_operand()
				return CmpFlagNode(flag=flag, label=label)
			else:
				left = self.parse_operand()
				op = self.advance().value
				right = self.parse_operand()
				self.advance()
				label = self.parse_operand()
				return CmpNode(left=left, op=op, right=right, label=label)
		else:
			self.advance()
			return None

	def parse(self):
		nodes = []
		if self.aliases is None:
			self.aliases = {}
		while self.peek().type != TokenType.EOF:
			char = self.peek()
			if char.type == TokenType.NEWLINE:
				self.advance()
			elif char.type == TokenType.IDENT and char.value == "module":
				self.advance()
				kind = self.advance().value
				body = []
				if kind in ("data", "reserve"):
					while self.peek() is not None and not (self.peek().type == TokenType.IDENT and self.peek().value == "module") and self.peek().type != TokenType.EOF and not (self.peek().type == TokenType.IDENT and self.peek().value == "on"):
						char = self.peek()
						if char.type == TokenType.NEWLINE:
							self.advance()
						elif char.value == "alias":
							self.advance()
							reg = self.advance().value
							name = self.advance().value
							self.aliases[name] = reg
						elif char.type == TokenType.IDENT:
							name = self.advance().value
							value = self.parse_operand()
							size = None
							if self.peek().type not in (TokenType.NEWLINE, TokenType.EOF):
								size = self.parse_operand()
							body.append(DataDefNode(name=name, value=value, size=size))
						else:
							self.advance()
				else:					
					while self.peek() is not None and not (self.peek().type == TokenType.IDENT and self.peek().value == "module") and self.peek().type != TokenType.EOF:
						char = self.peek()
						if char.type == TokenType.NEWLINE:
							self.advance()
						elif char.type == TokenType.IDENT and char.value == "fn":
							self.advance()
							fn_type = "normal"
							if self.peek().type == TokenType.IDENT and self.peek().value in ("global", "raw"):
								fn_type = self.peek().value
								self.advance()
							name = self.advance().value
							while self.peek().type == TokenType.NEWLINE:
								self.advance()
							self.advance()
							fn_body = []
							while self.peek().type != TokenType.IDENT or self.peek().value != "end":
								node = self.parse_statement()
								if node is not None:
									fn_body.append(node)
							self.advance()
							body.append(FnNode(name, fn_body, fn_type))
						elif char.type == TokenType.IDENT and char.value == "extern":
							self.advance()
							name = self.advance().value
							body.append(ExternNode(name=name))
						elif char.type == TokenType.IDENT and self.tokens[self.pos + 1].type == TokenType.COLON:
							self.advance()
							self.advance()
							body.append(LabelNode(name=char.value))
						elif char.type == TokenType.IDENT and char.value in instructions:
							node = self.parse_statement()
							if node is not None:
								body.append(node)
						elif char.type == TokenType.IDENT and char.value == "on":
							self.advance()
							self.advance()
							number = self.parse_operand()
							while self.peek().type == TokenType.NEWLINE:
								self.advance()
							self.advance()
							handler_body = []
							while self.peek().type != TokenType.IDENT or self.peek().value != "end":
								node = self.parse_statement()
								if node is not None:
									handler_body.append(node)
							self.advance()
							body.append(InterruptHandlerNode(number=number, body=handler_body))
						elif char.type == TokenType.IDENT:
							name = self.advance().value
							value = self.parse_operand()
							size = None
							if self.peek().type not in (TokenType.NEWLINE, TokenType.EOF):
								size = self.parse_operand()
							body.append(DataDefNode(name=name, value=value, size=size))
						else:
							self.advance()

				nodes.append(ModuleNode(kind, body))

			elif char.type == TokenType.IDENT and char.value == "extern":
				self.advance()
				name = self.parse_operand()
				nodes.append(ExternNode(name=name))
			elif char.type == TokenType.IDENT and char.value == "origin":
				self.advance()
				address = self.parse_operand()
				nodes.append(OriginNode(address=address))
			elif char.value == "on":
						self.advance()
						self.advance()
						number = self.parse_operand()
						while self.peek().type == TokenType.NEWLINE:
							self.advance()
						self.advance()
						handler_body = []
						while self.peek().type != TokenType.IDENT or self.peek().value != "end":
							node = self.parse_statement()
							if node is not None:
								handler_body.append(node)
						self.advance()
						nodes.append(InterruptHandlerNode(number=number, body=handler_body))
			else:
				self.advance()
		return nodes

if __name__ == "__main__":
	with open("source.s64") as f:
		src = f.read()
	lexer = Lexer(src)
	tokens = lexer.tokenize()
	parser = Parser(tokens)
	ast = parser.parse()
	print(ast)