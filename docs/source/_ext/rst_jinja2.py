# -- jinja2 customizations
# inspired by
#   * https://github.com/dropseed/combine/blob/47e7c75ca74fc056c7169206732b7cc1e3256773/combine/jinja/include_raw.py,
#   * https://www.ericholscher.com/blog/2016/jul/25/integrating-jinja-rst-sphinx/
from jinja2 import nodes
from jinja2.ext import Extension
from jinja2 import Markup


class IncludeRawExtension(Extension):
    tags = {"include_raw"}

    def parse(self, parser):
        lineno = parser.stream.expect("name:include_raw").lineno
        filename = nodes.Const(parser.parse_expression().value)
        result = self.call_method("_render", [filename], lineno=lineno)
        return nodes.Output([result], lineno=lineno)

    def _render(self, filename):
        return self.environment.loader.get_source(self.environment, filename)[0]


def rst_jinja2(app, docname, source):
    """
    Render our pages as a jinja template.
    """
    src = source[0]
    app.builder.templates.environment.add_extension(IncludeRawExtension)
    rendered = app.builder.templates.render_string(
        src, app.config.jinja_context
    )
    source[0] = rendered



def setup(app):
    app.connect("source-read", rst_jinja2)
    app.add_config_value("jinja_context", {}, 'env')
