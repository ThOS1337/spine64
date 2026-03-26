from enum import Enum, auto
from dataclasses import dataclass

class TokenType(Enum):
	IDENT = auto()
	NUMBER = auto()
	FLOAT = auto()
	STRING = auto()
	DOT_SIZE = auto()
	LBRACKET = auto()
	RBRACKET = auto()
	PLUS = auto()
	STAR = auto()
	COLON = auto()
	CMP_OP = auto()
	NEWLINE = auto()
	EOF = auto()

@dataclass 
class Token:
	type: TokenType
	value: str
	line: int

@dataclass
class Lexer:
	src: str
	pos: int = 0
	line: int = 1

	def peek(self):
		if self.pos < len(self.src):
			return self.src[self.pos]
		else:
			return None

	def advance(self):
		if self.pos < len(self.src):
			if self.src[self.pos] == '\n':
				char = self.src[self.pos]
				self.line += 1
				self.pos += 1
				return char
			else:
				char = self.src[self.pos]
				self.pos += 1
				return char
		else:
			return None

	def tokenize(self):
		tokenList = []
		word = ""

		while self.peek() is not None:
			char = self.peek()
			if char.isalpha() or char == "_":
				word = ""
				while self.peek() is not None and (self.peek().isalnum() or self.peek() == "_"):
					word += self.advance()
				tokenList.append(Token(TokenType.IDENT, word, self.line))
			elif char.isdigit():
				# check why its a digit
				if self.pos + 1 < len(self.src):
					if char == "0" and self.src[self.pos + 1] == "x":
						word = ""

						self.advance()
						self.advance()
						while self.peek() in "0123456789abcdefABCDEF":
							word += self.advance()
						tokenList.append(Token(TokenType.NUMBER, ("0x" + word), self.line))
					else:
						word = ""
						while self.peek() in "0123456789":
							word += self.advance()
						if self.peek() == ".":
							word += self.advance()

							while self.peek() in "0123456789":
								word += self.advance()
							tokenList.append(Token(TokenType.FLOAT, word, self.line))
						else:
							tokenList.append(Token(TokenType.NUMBER, word, self.line))
						
			else:
				char = self.peek()
				if char == "[":
					tokenList.append(Token(TokenType.LBRACKET, "[", self.line))
					self.advance()
				elif char == "]":
					tokenList.append(Token(TokenType.RBRACKET, "]", self.line))
					self.advance()
				elif char == "+":
					tokenList.append(Token(TokenType.PLUS, "+", self.line))
					self.advance()
				elif char == "*":
					tokenList.append(Token(TokenType.STAR, "*", self.line))
					self.advance()
				elif char == ":":
					tokenList.append(Token(TokenType.COLON, ":", self.line))
					self.advance()
				elif char == "\n":
					tokenList.append(Token(TokenType.NEWLINE, "\n", self.line))
					self.advance()
				elif char == " ":
					self.advance()
				elif char == "\t":
					self.advance()
				elif char == "#":
					while self.peek() is not None and self.peek() != '\n':
						self.advance()
				elif char == "=":
					if self.src[self.pos + 1] == "=":
						tokenList.append(Token(TokenType.CMP_OP, "==", self.line))
						self.advance()
						self.advance()   
				elif char == "!":
					if self.src[self.pos + 1] == "=":
						tokenList.append(Token(TokenType.CMP_OP, "!=", self.line))
						self.advance()
						self.advance()   
				elif char == "<":
					if self.src[self.pos + 1] == "=":
						tokenList.append(Token(TokenType.CMP_OP, "<=", self.line))
						self.advance()
						self.advance()   
					else:
						tokenList.append(Token(TokenType.CMP_OP, "<", self.line))
						self.advance()
				elif char == ">":
					if self.src[self.pos + 1] == "=":
						tokenList.append(Token(TokenType.CMP_OP, ">=", self.line))
						self.advance()
						self.advance()   
					else:
						tokenList.append(Token(TokenType.CMP_OP, ">", self.line))
						self.advance()
				elif char == ".":
					if self.pos + 1 < len(self.src) and self.src[self.pos + 1] in "1248":
						self.advance()
						size = self.advance()
						tokenList.append(Token(TokenType.DOT_SIZE, size, self.line))
					else:
						self.advance()
				elif char == '"':
					word = ""
					self.advance()
					while self.peek() != '"':
						word += self.advance()
					tokenList.append(Token(TokenType.STRING, word, self.line))
					self.advance()

		tokenList.append(Token(TokenType.EOF, '', self.line))

		return tokenList

if __name__ == "__main__":
	with open("source.s64") as f:
		src = f.read()
	lexer = Lexer(src)
	tokens = lexer.tokenize()
	for token in tokens:
		print(token)