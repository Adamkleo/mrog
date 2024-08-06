import unittest
from mrog.lexer import Lexer
from mrog.token import Token, TokenType

class TestLexer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """This method is run once before any tests are executed."""
        pass

    def setUp(self):
        """This method is run before each individual test."""
        pass

    def tearDown(self):
        """This method is run after each individual test."""
        pass

    @classmethod
    def tearDownClass(cls):
        """This method is run once after all tests are executed."""
        pass

    def test_arithmetic_operations(self):
        """Test case for a single token."""
        input_text = "3+1+3*2/5*3+2^2"
        lexer = Lexer(input_text)
        tokens = []
        current_token = lexer.get_next_token()
        while current_token.type != TokenType.EOF:
            tokens.append(current_token)
            current_token = lexer.get_next_token()
        
        expected_tokens = [
            Token(TokenType.NUMBER, 3.0),
            Token(TokenType.PLUS, '+'),
            Token(TokenType.NUMBER, 1.0),
            Token(TokenType.PLUS, '+'),
            Token(TokenType.NUMBER, 3.0),
            Token(TokenType.MUL, '*'),
            Token(TokenType.NUMBER, 2.0),
            Token(TokenType.DIV, '/'),
            Token(TokenType.NUMBER, 5.0),
            Token(TokenType.MUL, '*'),
            Token(TokenType.NUMBER, 3.0),
            Token(TokenType.PLUS, '+'),
            Token(TokenType.NUMBER, 2.0),
            Token(TokenType.POW, '^'),
            Token(TokenType.NUMBER, 2.0)
        ]

        for token, expected_token in zip(tokens, expected_tokens):
            self.assertEqual(token.type, expected_token.type)
            self.assertEqual(token.value, expected_token.value)


if __name__ == '__main__':
    unittest.main()
