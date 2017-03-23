"""
Based on https://github.com/VTK-Revue/revue-flask-server (revue/utilities/ui/bootstrap)
"""
from hashlib import sha1

from dominate import tags
from flask_bootstrap.nav import BootstrapRenderer
from flask_nav.elements import Navbar, View


class CustomBootstrapRenderer(BootstrapRenderer):
    def visit_CustomNavbar(self, node):
        # create a navbar id that is somewhat fixed, but do not leak any
        # information about memory contents to the outside
        node_id = self.id or sha1(str(id(node)).encode()).hexdigest()

        root = tags.nav() if self.html5 else tags.div(role='navigation')
        root['class'] = 'navbar navbar-default'

        cont = root.add(tags.div(_class='container'))

        # collapse button
        header = cont.add(tags.div(_class='navbar-header'))
        btn = header.add(tags.button())
        btn['type'] = 'button'
        btn['class'] = 'navbar-toggle collapsed'
        btn['data-toggle'] = 'collapse'
        btn['data-target'] = '#' + node_id
        btn['aria-expanded'] = 'false'
        btn['aria-controls'] = 'navbar'

        btn.add(tags.span('Toggle navigation', _class='sr-only'))
        btn.add(tags.span(_class='icon-bar'))
        btn.add(tags.span(_class='icon-bar'))
        btn.add(tags.span(_class='icon-bar'))

        # title may also have a 'get_url()' method, in which case we render
        # a brand-link
        if node.title is not None:
            if hasattr(node.title, 'get_url'):
                header.add(tags.a(node.title.text, _class='navbar-brand',
                                  href=node.title.get_url()))
            else:
                header.add(tags.span(node.title, _class='navbar-brand'))

        bar = cont.add(tags.div(
            _class='navbar-collapse collapse',
            id=node_id,
        ))
        bar_list_left = bar.add(tags.ul(_class='nav navbar-nav'))
        bar_list_right = bar.add(tags.ul(_class='nav navbar-nav navbar-right'))

        for item in node.left_items:
            tag = self.visit(item)
            if tag is not None:
                bar_list_left.add(tag)

        for item in node.right_items:
            tag = self.visit(item)
            if tag is not None:
                bar_list_right.add(self.visit(item))

        return root


class CustomNavbar(Navbar):
    def __init__(self, title, left_items, right_items):
        super().__init__(title, left_items + right_items)
        self.left_items = left_items
        self.right_items = right_items
