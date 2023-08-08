from antlr4 import *
from yaplLexer import yaplLexer
from yaplParser import yaplParser
from antlr4.tree.Trees import Trees
from antlr4.error.ErrorListener import ErrorListener
from graphviz import Digraph


def visualize_tree(tree, filename):
    graph = Digraph(comment='YAPL Syntax Tree')
    build_graph(tree, graph)
    graph.render(filename, view=True)


def build_graph(tree, graph, parent=None):
    if tree.getText():
        node = str(hash(tree))
        graph.node(node, tree.getText())
        if parent:
            graph.edge(parent, node)
        for i in range(tree.getChildCount()):
            build_graph(tree.getChild(i), graph, node)


class CustomErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        # Personalizar el mensaje de error para el análisis sintáctico
        print(f"\nERROR sintáctico en línea {line}, columna {column}: {msg}\n")

    def reportError(self, recognizer, e):
        # Personalizar el mensaje de error para el análisis léxico
        token = recognizer.getCurrentToken()
        line = token.line
        column = token.column
        print(
            f"\nERROR léxico en línea {line}, columna {column}: Carácter inesperado '{token.text}'\n")


class yaplListener(ParseTreeListener):

    def enterExpression(self, ctx: yaplParser.ExpressionContext):
        print("Entrando en expresión:", ctx.getText())

    def exitExpression(self, ctx: yaplParser.ExpressionContext):
        print("Saliendo de expresión:", ctx.getText())


def main():
    # Lee el código fuente de YAPL desde un archivo o un string
    # input_stream = FileStream("codigo.yapl")
    with open("codigo.yapl", "r", encoding="utf-8") as file:
        input_text = file.read()
    input_stream = InputStream(input_text)

    lexer = yaplLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = yaplParser(stream)

    # Asignar el manejador de errores personalizado al analizador léxico y sintáctico
    lexer.removeErrorListeners()
    lexer.addErrorListener(CustomErrorListener())
    parser = yaplParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(CustomErrorListener())

    # tree = parser.expression()
    tree = parser.program()


    # Visualizar el árbol de análisis sintáctico en consola
    print('Arbol de analisis sintactico: ',
          Trees.toStringTree(tree, recog=parser), "\n")

    # Crear el árbol de análisis
    yl = yaplListener()
    walker = ParseTreeWalker()
    walker.walk(yl, tree)

    visualize_tree(tree, "arbol_sintactico.pdf")


if __name__ == '__main__':
    main()
