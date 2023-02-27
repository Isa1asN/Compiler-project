grammar C_Grammar ;

start			: INCLUDE ? (function | global_var | (arr_decl EOS))* EOF ;

/*
*	PARSER RULES 
*/

global_var		: type_name identifier (ASS types)? EOS
				;

function		: (type_name | VOID) identifier LPAREN (type_name identifier (COMMA type_name identifier)*)? RPAREN codeblock
				;

codeblock       : LCURL statement* RCURL #firstCodeBlock
				| EOS #StEos
				;

ifStat			: IF LPAREN (assignment | all_right) RPAREN codeblock (ELSE (codeblock | ifStat | whileStat))?
				;

whileStat		: WHILE LPAREN (assignment | all_right) RPAREN codeblock
				;

forStat			: FOR LPAREN (left_expr | assignment) EOS compExpr EOS (left_expr | all_right |
					basicAss) RPAREN codeblock 
				;

statement		: LCURL statement* RCURL #codeBlock
				| RETURN (assignment | all_right) EOS #return
				| ifStat #if
				| whileStat #whileSt
				| forStat #forSt
				| (assignment | all_right | left_expr) EOS #expr
				| EOS #eos 
				; 

assignment		: basicAss #bA
				| arrayDeclAss #aDA
				;

basicAss		: left_expr (PLUS | MIN | MULT | DIV)? ASS all_right
				;

arrayDeclAss	: arr_decl
				;

arr_decl 		: type_name identifier LBRACK (all_right | both_expr)? RBRACK (ASS LCURL ((all_right | both_expr) (COMMA (all_right | 							both_expr))*)? RCURL)? #arrayDecl
				;

left_expr		: type_name? identifier #typeID
				| both_expr #leftboth
				;

right_expr		: (PLUS | MIN)? types #typeValue
				| LPAREN (assignment | arithmetic | right_expr) RPAREN #bracedExpr
				| identifier LPAREN ((all_right | both_expr) (COMMA (all_right | both_expr))*)? RPAREN #funcExpr
				| both_expr #rightboth
				;

all_right		: (right_expr | arithmetic) #rightArith
				| compExpr #comp
				;

compExpr		: (right_expr | arithmetic) compare (right_expr | arithmetic)
				;

both_expr		: (MULT | AMP)? identifier LBRACK (all_right | both_expr) RBRACK #arrayExpr
				;

factor			: (right_expr | both_expr) #fact
				;

term			: term MULT factor #multTerm
				| term DIV factor #divTerm
				| factor #tm
				;

arithmetic		: arithmetic PLUS term #plusArith
				| arithmetic MIN term #minArith
				| term #arith
				;

compare			: EQ | NEQ | LT | GT | LE | GE
				;

types			: FLOAT | INT | (MULT | AMP)? identifier | CHAR_T | STRING;
type_name		: (K_FLOAT | K_INT | K_CHAR) MULT?;
identifier		: WORD | CHAR ; 

comment   		: S_L_COMMENT | M_L_COMMENT ;

/*
*	LEXER RULES
*/

fragment DIGIT	: '0'..'9' ;
fragment UNDRSCR: '_' ;
fragment SPACE	: ' ' ;
fragment TAB	: '\t' ;
fragment NEWL   : '\n' ;
K_FLOAT			: 'float' ;
K_INT			: 'int' ;
K_CHAR			: 'char' ;

INCLUDE			: '#include <stdio.h>' ;

VOID 			: 'void' ;
WHILE 	 		: 'while' ;
FOR 			: 'for' ;
IF 				: 'if' ;
ELSE 			: 'else' ;
RETURN 			: 'return' ;
EQ 				: '==' ;
NEQ				: '!=' ;
GT 				: '>' ;
LT 				: '<' ;
GE				: '>=' ;
LE 				: '<=' ;
PLUS 			: '+' ;
MIN 			: '-' ;
MULT 			: '*' ;
DIV 			: '/' ;
ASS 			: '=' ;
LPAREN    		: '(' ;
RPAREN 			: ')' ;
LBRACK 			: '[' ;
RBRACK   		: ']' ;
LCURL 			: '{' ;
RCURL 			: '}' ;
EOS 			: ';' ;
ARROW 			: '->' ;
S_QUOTE 		: '\'' ;
D_QUOTE 		: '"' ;
COMMA			: ',' ;
AMP      		: '&' ;

STRING			: D_QUOTE (.)*? D_QUOTE ;
CHAR_T			: S_QUOTE (CHAR | SP_CHAR) S_QUOTE;
INT 			: DIGIT+ ;
FLOAT 			: DIGIT+ (. DIGIT+)? ;
CHAR 			: [a-z] | [A-Z] ;
SP_CHAR 		: '%' | '?' | '!' | '@' | '#' | '$' | '*' | '/' | '+' | '-' | '^' | '&' | '(' | ')' | '<' | '>' | '\\' ;
WORD 			: ([a-z] | [A-Z] | UNDRSCR) ([a-z] | [A-Z] | UNDRSCR | DIGIT)* ;

WS 				: (SPACE | TAB | NEWL)* -> skip;
S_L_COMMENT		: '//' (.)*? '\n' -> skip ;
M_L_COMMENT		: '/*' (.)*? '*/' -> skip ;
PRINTF			: 'printf' ;

