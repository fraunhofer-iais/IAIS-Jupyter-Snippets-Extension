from IPython.display import SVG
from graphviz import Source
from sklearn import tree
import re

def plot_decision_tree(clf, feature_names, class_names):
    # generate dot-file
    dot = tree.export_graphviz(clf,
                               out_file=None,
                               feature_names=feature_names,
                               class_names=sorted(class_names),
                               filled=True,
                               rounded=True,
                               label='all',
                               impurity=False,
                               proportion=False, 
                               leaves_parallel=False,
                               rotate=True,
                               special_characters=True)
    # highlight the rules in bold
    lines = []
    for line in dot.split('\n'):
        prettyfied_line = re.sub(r'(.*label=<)(.*)(<br/>samples = .*)', r'\1<b>\2</b>\3', line)
        lines.append(prettyfied_line)
    dot = '\n'.join(lines)

    # plot the graph inline
    graph = Source(dot)
    display(SVG(graph.pipe(format='svg')))
