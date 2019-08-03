import copy
import itertools

from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor


grammar = Grammar("""
     bold_text  = bracket_open collected_item (for current_item in current_iterable )+ bracket_close
     for = " for "
     in = " in "
     current_iterable      = ~"[A-Za-z0-9_]+"
     current_item  = ~"[A-Za-z0-9_]+"
     collected_item = ~"[A-Za-z0-9_\(\),\+\-\\\*]+"
     bracket_open  = "["
     bracket_close = "]"
""")


class XQL(NodeVisitor):
    def __init__(self):
        self.current_iterable = None
        self.collected_item = None
        self.current_item = None
        self.iter_depth = 0
        self.iterations = []
        self.ctx = {}

    def generic_visit(self, node, children):
        # print 'UNPARSED', node.text
        pass

    def visit_collected_item(self, node, children):
        self.collected_item = node.text

    def visit_current_item(self, node, children):
        self.current_item = node.text

    def visit_current_iterable(self, node, children):
        self.current_iterable = node.text
        self.iterations.append((self.current_iterable, self.current_item))
        self.iter_depth += 1

    def _eval(self, expression):
        # this is a hack! write grammar to parse this
        return eval(self.collected_item, {}, self.ctx)

    def eval(self, rule, data):
        self.ctx['data'] = data
        self.tree = grammar.parse(rule)
        self.visit(self.tree)

        for current_iterable, current_item in self.iterations:
            self.ctx[current_iterable] = iter(self.ctx[current_iterable])
            self.ctx[current_item] = next(self.ctx[current_iterable])

        results = []
        iterations = copy.deepcopy(self.iterations)
        while iterations:
            current_iterable, current_item = iterations.pop()
            citr = self.ctx[current_iterable]
            citm = self.ctx[current_item]
            print 'current_iterable:%s value:%s' % (current_iterable, citr)
            print 'current_item:%s value:%s' % (current_item, citm)
            print 'ctx', self.ctx
            for citm in [citm] + list(citr):
                self.ctx[current_item] = citm
                r = self._eval(self.collected_item, {}, self.ctx)
                print 'eval:%s value:%s' % (self.collected_item, r)
                results.append(r)
            if iterations:
                print 'add iteration'
                prev_iterable, prev_item = iterations[-1]
                try:
                    self.ctx[current_iterable] = iter(next(self.ctx[prev_iterable]))
                    self.ctx[current_item] = next(self.ctx[current_iterable])
                except StopIteration:
                    break
                else:
                    iterations.append((current_iterable, current_item))
        return results
