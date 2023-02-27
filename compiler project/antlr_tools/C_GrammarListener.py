# Generated from C_Grammar.g4 by ANTLR 4.11.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .C_GrammarParser import C_GrammarParser
else:
    from C_GrammarParser import C_GrammarParser

# This class defines a complete listener for a parse tree produced by C_GrammarParser.
class C_GrammarListener(ParseTreeListener):

    # Enter a parse tree produced by C_GrammarParser#start.
    def enterStart(self, ctx:C_GrammarParser.StartContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#start.
    def exitStart(self, ctx:C_GrammarParser.StartContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#global_var.
    def enterGlobal_var(self, ctx:C_GrammarParser.Global_varContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#global_var.
    def exitGlobal_var(self, ctx:C_GrammarParser.Global_varContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#function.
    def enterFunction(self, ctx:C_GrammarParser.FunctionContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#function.
    def exitFunction(self, ctx:C_GrammarParser.FunctionContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#firstCodeBlock.
    def enterFirstCodeBlock(self, ctx:C_GrammarParser.FirstCodeBlockContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#firstCodeBlock.
    def exitFirstCodeBlock(self, ctx:C_GrammarParser.FirstCodeBlockContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#StEos.
    def enterStEos(self, ctx:C_GrammarParser.StEosContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#StEos.
    def exitStEos(self, ctx:C_GrammarParser.StEosContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#ifStat.
    def enterIfStat(self, ctx:C_GrammarParser.IfStatContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#ifStat.
    def exitIfStat(self, ctx:C_GrammarParser.IfStatContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#whileStat.
    def enterWhileStat(self, ctx:C_GrammarParser.WhileStatContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#whileStat.
    def exitWhileStat(self, ctx:C_GrammarParser.WhileStatContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#forStat.
    def enterForStat(self, ctx:C_GrammarParser.ForStatContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#forStat.
    def exitForStat(self, ctx:C_GrammarParser.ForStatContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#codeBlock.
    def enterCodeBlock(self, ctx:C_GrammarParser.CodeBlockContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#codeBlock.
    def exitCodeBlock(self, ctx:C_GrammarParser.CodeBlockContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#return.
    def enterReturn(self, ctx:C_GrammarParser.ReturnContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#return.
    def exitReturn(self, ctx:C_GrammarParser.ReturnContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#if.
    def enterIf(self, ctx:C_GrammarParser.IfContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#if.
    def exitIf(self, ctx:C_GrammarParser.IfContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#whileSt.
    def enterWhileSt(self, ctx:C_GrammarParser.WhileStContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#whileSt.
    def exitWhileSt(self, ctx:C_GrammarParser.WhileStContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#forSt.
    def enterForSt(self, ctx:C_GrammarParser.ForStContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#forSt.
    def exitForSt(self, ctx:C_GrammarParser.ForStContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#expr.
    def enterExpr(self, ctx:C_GrammarParser.ExprContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#expr.
    def exitExpr(self, ctx:C_GrammarParser.ExprContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#eos.
    def enterEos(self, ctx:C_GrammarParser.EosContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#eos.
    def exitEos(self, ctx:C_GrammarParser.EosContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#bA.
    def enterBA(self, ctx:C_GrammarParser.BAContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#bA.
    def exitBA(self, ctx:C_GrammarParser.BAContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#aDA.
    def enterADA(self, ctx:C_GrammarParser.ADAContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#aDA.
    def exitADA(self, ctx:C_GrammarParser.ADAContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#basicAss.
    def enterBasicAss(self, ctx:C_GrammarParser.BasicAssContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#basicAss.
    def exitBasicAss(self, ctx:C_GrammarParser.BasicAssContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#arrayDeclAss.
    def enterArrayDeclAss(self, ctx:C_GrammarParser.ArrayDeclAssContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#arrayDeclAss.
    def exitArrayDeclAss(self, ctx:C_GrammarParser.ArrayDeclAssContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#arrayDecl.
    def enterArrayDecl(self, ctx:C_GrammarParser.ArrayDeclContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#arrayDecl.
    def exitArrayDecl(self, ctx:C_GrammarParser.ArrayDeclContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#typeID.
    def enterTypeID(self, ctx:C_GrammarParser.TypeIDContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#typeID.
    def exitTypeID(self, ctx:C_GrammarParser.TypeIDContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#leftboth.
    def enterLeftboth(self, ctx:C_GrammarParser.LeftbothContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#leftboth.
    def exitLeftboth(self, ctx:C_GrammarParser.LeftbothContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#typeValue.
    def enterTypeValue(self, ctx:C_GrammarParser.TypeValueContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#typeValue.
    def exitTypeValue(self, ctx:C_GrammarParser.TypeValueContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#bracedExpr.
    def enterBracedExpr(self, ctx:C_GrammarParser.BracedExprContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#bracedExpr.
    def exitBracedExpr(self, ctx:C_GrammarParser.BracedExprContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#funcExpr.
    def enterFuncExpr(self, ctx:C_GrammarParser.FuncExprContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#funcExpr.
    def exitFuncExpr(self, ctx:C_GrammarParser.FuncExprContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#rightboth.
    def enterRightboth(self, ctx:C_GrammarParser.RightbothContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#rightboth.
    def exitRightboth(self, ctx:C_GrammarParser.RightbothContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#rightArith.
    def enterRightArith(self, ctx:C_GrammarParser.RightArithContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#rightArith.
    def exitRightArith(self, ctx:C_GrammarParser.RightArithContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#comp.
    def enterComp(self, ctx:C_GrammarParser.CompContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#comp.
    def exitComp(self, ctx:C_GrammarParser.CompContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#compExpr.
    def enterCompExpr(self, ctx:C_GrammarParser.CompExprContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#compExpr.
    def exitCompExpr(self, ctx:C_GrammarParser.CompExprContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#arrayExpr.
    def enterArrayExpr(self, ctx:C_GrammarParser.ArrayExprContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#arrayExpr.
    def exitArrayExpr(self, ctx:C_GrammarParser.ArrayExprContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#fact.
    def enterFact(self, ctx:C_GrammarParser.FactContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#fact.
    def exitFact(self, ctx:C_GrammarParser.FactContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#multTerm.
    def enterMultTerm(self, ctx:C_GrammarParser.MultTermContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#multTerm.
    def exitMultTerm(self, ctx:C_GrammarParser.MultTermContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#tm.
    def enterTm(self, ctx:C_GrammarParser.TmContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#tm.
    def exitTm(self, ctx:C_GrammarParser.TmContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#divTerm.
    def enterDivTerm(self, ctx:C_GrammarParser.DivTermContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#divTerm.
    def exitDivTerm(self, ctx:C_GrammarParser.DivTermContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#arith.
    def enterArith(self, ctx:C_GrammarParser.ArithContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#arith.
    def exitArith(self, ctx:C_GrammarParser.ArithContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#minArith.
    def enterMinArith(self, ctx:C_GrammarParser.MinArithContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#minArith.
    def exitMinArith(self, ctx:C_GrammarParser.MinArithContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#plusArith.
    def enterPlusArith(self, ctx:C_GrammarParser.PlusArithContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#plusArith.
    def exitPlusArith(self, ctx:C_GrammarParser.PlusArithContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#compare.
    def enterCompare(self, ctx:C_GrammarParser.CompareContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#compare.
    def exitCompare(self, ctx:C_GrammarParser.CompareContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#types.
    def enterTypes(self, ctx:C_GrammarParser.TypesContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#types.
    def exitTypes(self, ctx:C_GrammarParser.TypesContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#type_name.
    def enterType_name(self, ctx:C_GrammarParser.Type_nameContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#type_name.
    def exitType_name(self, ctx:C_GrammarParser.Type_nameContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#identifier.
    def enterIdentifier(self, ctx:C_GrammarParser.IdentifierContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#identifier.
    def exitIdentifier(self, ctx:C_GrammarParser.IdentifierContext):
        pass


    # Enter a parse tree produced by C_GrammarParser#comment.
    def enterComment(self, ctx:C_GrammarParser.CommentContext):
        pass

    # Exit a parse tree produced by C_GrammarParser#comment.
    def exitComment(self, ctx:C_GrammarParser.CommentContext):
        pass



del C_GrammarParser