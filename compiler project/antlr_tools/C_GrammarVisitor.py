# Generated from C_Grammar.g4 by ANTLR 4.11.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .C_GrammarParser import C_GrammarParser
else:
    from C_GrammarParser import C_GrammarParser

# This class defines a complete generic visitor for a parse tree produced by C_GrammarParser.

class C_GrammarVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by C_GrammarParser#start.
    def visitStart(self, ctx:C_GrammarParser.StartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#global_var.
    def visitGlobal_var(self, ctx:C_GrammarParser.Global_varContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#function.
    def visitFunction(self, ctx:C_GrammarParser.FunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#firstCodeBlock.
    def visitFirstCodeBlock(self, ctx:C_GrammarParser.FirstCodeBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#StEos.
    def visitStEos(self, ctx:C_GrammarParser.StEosContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#ifStat.
    def visitIfStat(self, ctx:C_GrammarParser.IfStatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#whileStat.
    def visitWhileStat(self, ctx:C_GrammarParser.WhileStatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#forStat.
    def visitForStat(self, ctx:C_GrammarParser.ForStatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#codeBlock.
    def visitCodeBlock(self, ctx:C_GrammarParser.CodeBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#return.
    def visitReturn(self, ctx:C_GrammarParser.ReturnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#if.
    def visitIf(self, ctx:C_GrammarParser.IfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#whileSt.
    def visitWhileSt(self, ctx:C_GrammarParser.WhileStContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#forSt.
    def visitForSt(self, ctx:C_GrammarParser.ForStContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#expr.
    def visitExpr(self, ctx:C_GrammarParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#eos.
    def visitEos(self, ctx:C_GrammarParser.EosContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#bA.
    def visitBA(self, ctx:C_GrammarParser.BAContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#aDA.
    def visitADA(self, ctx:C_GrammarParser.ADAContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#basicAss.
    def visitBasicAss(self, ctx:C_GrammarParser.BasicAssContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#arrayDeclAss.
    def visitArrayDeclAss(self, ctx:C_GrammarParser.ArrayDeclAssContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#arrayDecl.
    def visitArrayDecl(self, ctx:C_GrammarParser.ArrayDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#typeID.
    def visitTypeID(self, ctx:C_GrammarParser.TypeIDContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#leftboth.
    def visitLeftboth(self, ctx:C_GrammarParser.LeftbothContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#typeValue.
    def visitTypeValue(self, ctx:C_GrammarParser.TypeValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#bracedExpr.
    def visitBracedExpr(self, ctx:C_GrammarParser.BracedExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#funcExpr.
    def visitFuncExpr(self, ctx:C_GrammarParser.FuncExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#rightboth.
    def visitRightboth(self, ctx:C_GrammarParser.RightbothContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#rightArith.
    def visitRightArith(self, ctx:C_GrammarParser.RightArithContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#comp.
    def visitComp(self, ctx:C_GrammarParser.CompContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#compExpr.
    def visitCompExpr(self, ctx:C_GrammarParser.CompExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#arrayExpr.
    def visitArrayExpr(self, ctx:C_GrammarParser.ArrayExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#fact.
    def visitFact(self, ctx:C_GrammarParser.FactContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#multTerm.
    def visitMultTerm(self, ctx:C_GrammarParser.MultTermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#tm.
    def visitTm(self, ctx:C_GrammarParser.TmContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#divTerm.
    def visitDivTerm(self, ctx:C_GrammarParser.DivTermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#arith.
    def visitArith(self, ctx:C_GrammarParser.ArithContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#minArith.
    def visitMinArith(self, ctx:C_GrammarParser.MinArithContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#plusArith.
    def visitPlusArith(self, ctx:C_GrammarParser.PlusArithContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#compare.
    def visitCompare(self, ctx:C_GrammarParser.CompareContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#types.
    def visitTypes(self, ctx:C_GrammarParser.TypesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#type_name.
    def visitType_name(self, ctx:C_GrammarParser.Type_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#identifier.
    def visitIdentifier(self, ctx:C_GrammarParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by C_GrammarParser#comment.
    def visitComment(self, ctx:C_GrammarParser.CommentContext):
        return self.visitChildren(ctx)



del C_GrammarParser