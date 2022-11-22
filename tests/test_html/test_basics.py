"""Basic html tests.

poetry run pytest tests/test_html/test_basics.py
"""
import pytest

from src.djlint.formatter.indent import indent_html
from tests.conftest import printer

test_data = [
    pytest.param(
        (
            "<!--\n"
            "#7241,\n"
            "reproduction:\n"
            "two different element,\n"
            "linebreak\n"
            "\\`<\\`\n"
            "extra space(s)\n"
            "-->\n"
            "<div><span>\n"
            "<\n"
        ),
        (
            "<!--\n"
            "#7241,\n"
            "reproduction:\n"
            "two different element,\n"
            "linebreak\n"
            "\\`<\\`\n"
            "extra space(s)\n"
            "-->\n"
            "<div>\n"
            "   <span> <\n"
        ),
        id="broken_html",
    ),
    pytest.param("<!--hello world-->", "<!--hello world-->", id="comment"),
    pytest.param(
        (
            "<!doctype html>\n"
            "<html>\n"
            "<head></head>\n"
            "<body></body>\n"
            "</html>\n"
        ),
        (
            "<!DOCTYPE html>\n"
            "<html>\n"
            "    <head></head>\n"
            "    <body></body>\n"
            "</html>\n"
        ),
        id="emtpy_doc",
    ),
    pytest.param("", "\n", id="empty"),
    pytest.param(
        (
            "<form>\n"
            '  <div class="form-group">\n'
            '    <label for="exampleInputEmail1">Email address</label>\n'
            '    <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter email">\n'
            '    <small id="emailHelp" class="form-text text-muted">We\'ll never share your email with anyone else.</small>\n'
            "  </div>\n"
            '  <div class="form-group">\n'
            '    <label for="exampleInputPassword1">Password</label>\n'
            '    <input type="password" class="form-control" id="exampleInputPassword1" placeholder="Password">\n'
            "  </div>\n"
            '  <div class="form-group">\n'
            '    <label for="exampleSelect1">Example select</label>\n'
            '    <select class="form-control" id="exampleSelect1">\n'
            "      <option>1</option>\n"
            "      <option>2</option>\n"
            "      <option>3</option>\n"
            "      <option>4</option>\n"
            "      <option>5</option>\n"
            "    </select>\n"
            "  </div>\n"
            '  <div class="form-group">\n'
            '    <label for="exampleSelect2">Example multiple select</label>\n'
            '    <select multiple class="form-control" id="exampleSelect2">\n'
            "      <option>1</option>\n"
            "      <option>2</option>\n"
            "      <option>3</option>\n"
            "      <option>4</option>\n"
            "      <option>5</option>\n"
            "    </select>\n"
            "  </div>\n"
            '  <div class="form-group">\n'
            '    <label for="exampleTextarea">Example textarea</label>\n'
            '    <textarea class="form-control" id="exampleTextarea" rows="3"></textarea>\n'
            "  </div>\n"
            '  <div class="form-group">\n'
            '    <label for="exampleInputFile">File input</label>\n'
            '    <input type="file" class="form-control-file" id="exampleInputFile" aria-describedby="fileHelp">\n'
            '    <small id="fileHelp" class="form-text text-muted">This is some placeholder block-level help text for the above input. It\'s a bit lighter and easily wraps to a new line.</small>\n'
            "  </div>\n"
            '  <fieldset class="form-group">\n'
            "    <legend>Radio buttons</legend>\n"
            '    <div class="form-check">\n'
            '      <label class="form-check-label">\n'
            '        <input type="radio" class="form-check-input" name="optionsRadios" id="optionsRadios1" value="option1" checked>\n'
            "        Option one is this and that&mdash;be sure to include why it's great\n"
            "      </label>\n"
            "    </div>\n"
            '    <div class="form-check">\n'
            '      <label class="form-check-label">\n'
            '        <input type="radio" class="form-check-input" name="optionsRadios" id="optionsRadios2" value="option2">\n'
            "        Option two can be something else and selecting it will deselect option one\n"
            "      </label>\n"
            "    </div>\n"
            '    <div class="form-check disabled">\n'
            '      <label class="form-check-label">\n'
            '        <input type="radio" class="form-check-input" name="optionsRadios" id="optionsRadios3" value="option3" disabled>\n'
            "        Option three is disabled\n"
            "      </label>\n"
            "    </div>\n"
            "  </fieldset>\n"
            '  <div class="form-check">\n'
            '    <label class="form-check-label">\n'
            '      <input type="checkbox" class="form-check-input">\n'
            "      Check me out\n"
            "    </label>\n"
            "  </div>\n"
            '  <button type="submit" class="btn btn-primary">Submit</button>\n'
            "</form>\n"
        ),
        (
            "<form>\n"
            '    <div class="form-group">\n'
            '        <label for="exampleInputEmail1">Email address</label>\n'
            "            <input\n"
            '              type="email"\n'
            '              class="form-control"\n'
            '              id="exampleInputEmail1"\n'
            '              aria-describedby="emailHelp"\n'
            '              placeholder="Enter email"\n'
            "            />\n"
            '            <small id="emailHelp" class="form-text text-muted"\n'
            "              >We'll never share your email with anyone else.</small\n"
            "            >\n"
            "    </div>\n"
            '    <div class="form-group">\n'
            '        <label for="exampleInputPassword1">Password</label>\n'
            "        <input\n"
            '          type="password"\n'
            '          class="form-control"\n'
            '          id="exampleInputPassword1"\n'
            '          placeholder="Password"\n'
            "        />\n"
            "    </div>\n"
            '    <div class="form-group">\n'
            '        <label for="exampleSelect1">Example select</label>\n'
            '        <select class="form-control" id="exampleSelect1">\n'
            "            <option>1</option>\n"
            "            <option>2</option>\n"
            "            <option>3</option>\n"
            "            <option>4</option>\n"
            "            <option>5</option>\n"
            "        </select>\n"
            "    </div>\n"
            '    <div class="form-group">\n'
            '        <label for="exampleSelect2">Example multiple select</label>\n'
            '        <select multiple class="form-control" id="exampleSelect2">\n'
            "            <option>1</option>\n"
            "            <option>2</option>\n"
            "            <option>3</option>\n"
            "            <option>4</option>\n"
            "            <option>5</option>\n"
            "        </select>\n"
            "    </div>\n"
            '    <div class="form-group">\n'
            '        <label for="exampleTextarea">Example textarea</label>\n'
            '        <textarea class="form-control" id="exampleTextarea" rows="3"></textarea>\n'
            "    </div>\n"
            '    <div class="form-group">\n'
            '        <label for="exampleInputFile">File input</label>\n'
            "        <input\n"
            '            type="file"\n'
            '            class="form-control-file"\n'
            '            id="exampleInputFile"\n'
            '            aria-describedby="fileHelp"\n'
            "        />\n"
            '        <small id="fileHelp" class="form-text text-muted"\n'
            "            >This is some placeholder block-level help text for the above input. It's\n"
            "            a bit lighter and easily wraps to a new line.</small\n"
            "        >\n"
            "    </div>\n"
            '    <fieldset class="form-group">\n'
            "        <legend>Radio buttons</legend>\n"
            '        <div class="form-check">\n'
            '            <label class="form-check-label">\n'
            "                <input\n"
            '                    type="radio"\n'
            '                    class="form-check-input"\n'
            '                    name="optionsRadios"\n'
            '                    id="optionsRadios1"\n'
            '                    value="option1"\n'
            "                    checked\n"
            "                />\n"
            "                Option one is this and that&mdash;be sure to include why it's great\n"
            "            </label>\n"
            "        </div>\n"
            '        <div class="form-check">\n'
            '            <label class="form-check-label">\n'
            "                <input\n"
            '                    type="radio"\n'
            '                    class="form-check-input"\n'
            '                    name="optionsRadios"\n'
            '                    id="optionsRadios2"\n'
            '                    value="option2"\n'
            "                />\n"
            "                Option two can be something else and selecting it will deselect option\n"
            "                one\n"
            "            </label>\n"
            "        </div>\n"
            '        <div class="form-check disabled">\n'
            '            <label class="form-check-label">\n'
            "                <input\n"
            '                    type="radio"\n'
            '                    class="form-check-input"\n'
            '                    name="optionsRadios"\n'
            '                    id="optionsRadios3"\n'
            '                    value="option3"\n'
            "                    disabled\n"
            "                />\n"
            "                Option three is disabled\n"
            "            </label>\n"
            "        </div>\n"
            "    </fieldset>\n"
            '    <div class="form-check">\n'
            '        <label class="form-check-label">\n'
            '            <input type="checkbox" class="form-check-input" />\n'
            "            Check me out\n"
            "        </label>\n"
            "    </div>\n"
            '    <button type="submit" class="btn btn-primary">Submit</button>\n'
            "</form>\n"
        ),
        id="form",
    ),
    pytest.param(
        (
            "<!DOCTYPE html>\n"
            '<html lang="en">\n'
            "    <head>\n"
            '        <meta charset="UTF-8">\n'
            '        <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            '        <meta http-equiv="X-UA-Compatible" content="ie=edge">\n'
            "        <title>Document</title>\n"
            "    </head>\n"
            "    <body>\n"
            "        <!-- A comment -->\n"
            "        <h1>Hello World</h1>\n"
            "    </body>\n"
            "</html>\n"
        ),
        (
            "<!DOCTYPE html>\n"
            '<html lang="en">\n'
            "    <head>\n"
            '        <meta charset="UTF-8">\n'
            '        <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            '        <meta http-equiv="X-UA-Compatible" content="ie=edge">\n'
            "        <title>Document</title>\n"
            "    </head>\n"
            "    <body>\n"
            "        <!-- A comment -->\n"
            "        <h1>Hello World</h1>\n"
            "    </body>\n"
            "</html>\n"
        ),
        id="hello_world",
    ),
    pytest.param(
        (
            "<!-- htmlhint attr-lowercase: false -->\n"
            "<html>\n"
            "    <body>\n"
            '        <a href="#">Anchor</a>\n'
            '        <div hidden class="foo" id=bar></div>\n'
            "    </body>\n"
            "</html>\n"
        ),
        (
            "<!-- htmlhint attr-lowercase: false -->\n"
            "<html>\n"
            "    <body>\n"
            '        <a href="#">Anchor</a>\n'
            '        <div hidden class="foo" id=bar></div>\n'
            "    </body>\n"
            "</html>\n"
        ),
        id="html_comments",
    ),
    pytest.param(
        (
            "<!doctype html>\n"
            '<html class="no-js" lang="">\n'
            "  <head>\n"
            '    <meta charset="utf-8">\n'
            '    <meta http-equiv="x-ua-compatible" content="ie=edge">\n'
            "    <title></title>\n"
            '    <meta name="description" content="">\n'
            '    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">\n'
            '    <link rel="manifest" href="site.webmanifest">\n'
            '    <link rel="apple-touch-icon" href="icon.png">\n'
            "    <!-- Place favicon.ico in the root directory -->\n"
            '    <link rel="stylesheet" href="css/normalize.css">\n'
            '    <link rel="stylesheet" href="css/main.css">\n'
            "  </head>\n"
            "  <body>\n"
            "    <!--[if lte IE 9]>\n"
            '    <p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="https://browsehappy.com/">upgrade your browser</a> to improve your experience and security.</p>\n'
            "    <![endif]-->\n"
            "    <!-- Add your site or application content here -->\n"
            "    <p>Hello world! This is HTML5 Boilerplate.</p>\n"
            '    <script src="js/vendor/modernizr-3.6.0.min.js"></script>\n'
            '    <script src="https://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>\n'
            "    <script>window.jQuery || document.write('<script src=\"js/vendor/jquery-3.3.1.min.js\"><\\/script>')</script>\n"
            '    <script src="js/plugins.js"></script>\n'
            '    <script src="js/main.js"></script>\n'
            "    <!-- Google Analytics: change UA-XXXXX-Y to be your site's ID. -->\n"
            "    <script>\n"
            "      window.ga = function () { ga.q.push(arguments) }; ga.q = []; ga.l = +new Date;\n"
            "      ga('create', 'UA-XXXXX-Y', 'auto'); ga('send', 'pageview')\n"
            "    </script>\n"
            '    <script src="https://www.google-analytics.com/analytics.js" async defer></script>\n'
            "  </body>\n"
            "</html>\n"
        ),
        (
            "<!DOCTYPE html>\n"
            '<html class="no-js" lang="">\n'
            "    <head>\n"
            '        <meta charset="utf-8" />\n'
            '        <meta http-equiv="x-ua-compatible" content="ie=edge" />\n'
            "        <title></title>\n"
            '        <meta name="description" content="" />\n'
            "        <meta\n"
            '            name="viewport"\n'
            '            content="width=device-width, initial-scale=1, shrink-to-fit=no"\n'
            "        />\n"
            '        <link rel="manifest" href="site.webmanifest" />\n'
            '        <link rel="apple-touch-icon" href="icon.png" />\n'
            "        <!-- Place favicon.ico in the root directory -->\n"
            '        <link rel="stylesheet" href="css/normalize.css" />\n'
            '        <link rel="stylesheet" href="css/main.css" />\n'
            "    </head>\n"
            "    <body>\n"
            "        <!--[if lte IE 9]>\n"
            '            <p class="browserupgrade">\n'
            "                You are using an <strong>outdated</strong> browser. Please\n"
            '                <a href="https://browsehappy.com/">upgrade your browser</a> to improve\n'
            "                your experience and security.\n"
            "            </p>\n"
            "        <![endif]-->\n"
            "        <!-- Add your site or application content here -->\n"
            "        <p>Hello world! This is HTML5 Boilerplate.</p>\n"
            '        <script src="js/vendor/modernizr-3.6.0.min.js"></script>\n'
            "        <script\n"
            '            src="https://code.jquery.com/jquery-3.3.1.min.js"\n'
            '            integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8="\n'
            '            crossorigin="anonymous"\n'
            "        ></script>\n"
            "        <script>\n"
            "          window.jQuery ||\n"
            "            document.write(\n"
            "              '<script src=\"js/vendor/jquery-3.3.1.min.js\"><\\/script>'\n"
            "            );\n"
            "        </script>\n"
            '        <script src="js/plugins.js"></script>\n'
            '        <script src="js/main.js"></script>\n'
            "        <!-- Google Analytics: change UA-XXXXX-Y to be your site's ID. -->\n"
            "        <script>\n"
            "          window.ga = function () {\n"
            "            ga.q.push(arguments);\n"
            "          };\n"
            "          ga.q = [];\n"
            "          ga.l = +new Date();\n"
            '          ga("create", "UA-XXXXX-Y", "auto");\n'
            '          ga("send", "pageview");\n'
            "        </script>\n"
            "        <script\n"
            '          src="https://www.google-analytics.com/analytics.js"\n'
            "          async\n"
            "          defer\n"
            "        ></script>\n"
            "    </body>\n"
            "</html>\n"
        ),
        id="html5_boilerplate",
    ),
    pytest.param(
        "<strong>a</strong>-<strong>b</strong>-",
        "<strong>a</strong>-<strong>b</strong>-",
        id="issue_9368_2",
    ),
    pytest.param(
        "a track<strong>pad</strong>, or a <strong>gyro</strong>scope.",
        "a track<strong>pad</strong>, or a <strong>gyro</strong>scope.",
        id="issue_9368_3",
    ),
    pytest.param(
        "<strong>a</strong>-&gt;<strong>b</strong>-&gt;",
        "<strong>a</strong>-&gt;<strong>b</strong>-&gt;",
        id="issue_9368",
    ),
    pytest.param(
        (
            "<html>\n"
            "<head></head>\n"
            "<body>\n"
            '    <a href="#">Anchor</a>\n'
            '    <div hidden class="foo" id=bar></div>\n'
            "</body>\n"
            "</html>\n"
        ),
        (
            "<html>\n"
            "    <head></head>\n"
            "    <body>\n"
            '        <a href="#">Anchor</a>\n'
            '        <div hidden class="foo" id="bar"></div>\n'
            "    </body>\n"
            "</html>\n"
        ),
        id="more_html",
    ),
    pytest.param(
        (
            "<html>\n"
            "    <head>\n"
            '        <meta charset="UTF-8" />\n'
            '        <link rel="stylesheet" href="code-guide.css" />\n'
            "    </head>\n"
            "    <body></body>\n"
            "</html>\n"
        ),
        (
            "<html>\n"
            "    <head>\n"
            '        <meta charset="UTF-8" />\n'
            '        <link rel="stylesheet" href="code-guide.css" />\n'
            "    </head>\n"
            "    <body></body>\n"
            "</html>\n"
        ),
        id="void_elements",
    ),
    pytest.param(
        (
            '<video controls width="250">\n'
            '    <source src="/media/examples/flower.webm"\n'
            '            type="video/webm">\n'
            '    <source src="/media/examples/flower.mp4"\n'
            '            type="video/mp4"\n'
            "></video>text after\n"
            "<!-- #8626 -->\n"
            '<object data="horse.wav"><param name="autoplay" value="true"\n'
            '><param name="autoplay" value="true"\n'
            "></object>1\n"
            '<span><img  src="1.png"\n'
            '><img src="1.png"\n'
            "></span>1\n"
        ),
        (
            '<video controls width="250">\n'
            '    <source src="/media/examples/flower.webm" type="video/webm" />\n'
            '    <source src="/media/examples/flower.mp4" type="video/mp4" /></video\n'
            ">text after\n"
            "<!-- #8626 -->\n"
            '<object data="horse.wav">\n'
            '    <param name="autoplay" value="true" />\n'
            '    <param name="autoplay" value="true" /></object\n'
            ">1\n"
            '<span><img src="1.png" /><img src="1.png" /></span>1\n'
        ),
        id="more_void_elements",
    ),
    pytest.param(
        (
            "<!-- unknown tag with colon -->\n"
            "<div>\n"
            "<foo:bar>\n"
            "<div> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block </div>\n"
            "<div> block </div><DIV> BLOCK </DIV> <div> block </div><div> block </div><div> block </div>\n"
            "<pre> pre pr\n"
            "e</pre>\n"
            "<textarea> pre-wrap pr\n"
            "e-wrap </textarea>\n"
            "<span> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline </span>\n"
            "<span> inline </span><span> inline </span> <span> inline </span><span> inline </span>\n"
            "<html:div> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block </html:div>\n"
            "<html:DIV> block </html:DIV><HTML:DIV> BLOCK </HTML:DIV> <html:div> block </html:div><html:div> block </html:div><html:div> block </html:div>\n"
            "<html:pre> pre pr\n"
            "e</html:pre>\n"
            "<html:textarea> pre-wrap pr\n"
            "e-wrap </html:textarea>\n"
            "<html:span> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline </html:span>\n"
            "<html:span> inline </html:span><html:span> inline </html:span> <html:span> inline </html:span><html:span> inline </html:span></foo:bar>\n"
            "</div>\n"
            "<!-- block tag with colon -->\n"
            "<div>\n"
            "<foo:div>\n"
            "<div> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block </div>\n"
            "<div> block </div><DIV> BLOCK </DIV> <div> block </div><div> block </div><div> block </div>\n"
            "<pre> pre pr\n"
            "e</pre>\n"
            "<textarea> pre-wrap pr\n"
            "e-wrap </textarea>\n"
            "<span> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline </span>\n"
            "<span> inline </span><span> inline </span> <span> inline </span><span> inline </span>\n"
            "<html:div> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block </html:div>\n"
            "<html:DIV> block </html:DIV><HTML:DIV> BLOCK </HTML:DIV> <html:div> block </html:div><html:div> block </html:div><html:div> block </html:div>\n"
            "<html:pre> pre pr\n"
            "e</html:pre>\n"
            "<html:textarea> pre-wrap pr\n"
            "e-wrap </html:textarea>\n"
            "<html:span> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline </html:span>\n"
            "<html:span> inline </html:span><html:span> inline </html:span> <html:span> inline </html:span><html:span> inline </html:span></foo:div>\n"
            "</div>\n"
            "<!-- inline tag with colon -->\n"
            "<div>\n"
            "<foo:span>\n"
            "<div> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block </div>\n"
            "<div> block </div><DIV> BLOCK </DIV> <div> block </div><div> block </div><div> block </div>\n"
            "<pre> pre pr\n"
            "e</pre>\n"
            "<textarea> pre-wrap pr\n"
            "e-wrap </textarea>\n"
            "<span> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline </span>\n"
            "<span> inline </span><span> inline </span> <span> inline </span><span> inline </span>\n"
            "<html:div> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block </html:div>\n"
            "<html:DIV> block </html:DIV><HTML:DIV> BLOCK </HTML:DIV> <html:div> block </html:div><html:div> block </html:div><html:div> block </html:div>\n"
            "<html:pre> pre pr\n"
            "e</html:pre>\n"
            "<html:textarea> pre-wrap pr\n"
            "e-wrap </html:textarea>\n"
            "<html:span> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline </html:span>\n"
            "<html:span> inline </html:span><html:span> inline </html:span> <html:span> inline </html:span><html:span> inline </html:span></foo:span>\n"
            "</div>\n"
            "<!-- unknown -->\n"
            "<div>\n"
            "<foo-bar>\n"
            "<div> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block </div>\n"
            "<div> block </div><DIV> BLOCK </DIV> <div> block </div><div> block </div><div> block </div>\n"
            "<pre> pre pr\n"
            "e</pre>\n"
            "<textarea> pre-wrap pr\n"
            "e-wrap </textarea>\n"
            "<span> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline </span>\n"
            "<span> inline </span><span> inline </span> <span> inline </span><span> inline </span>\n"
            "<html:div> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block </html:div>\n"
            "<html:DIV> block </html:DIV><HTML:DIV> BLOCK </HTML:DIV> <html:div> block </html:div><html:div> block </html:div><html:div> block </html:div>\n"
            "<html:pre> pre pr\n"
            "e</html:pre>\n"
            "<html:textarea> pre-wrap pr\n"
            "e-wrap </html:textarea>\n"
            "<html:span> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline </html:span>\n"
            "<html:span> inline </html:span><html:span> inline </html:span> <html:span> inline </html:span><html:span> inline </html:span></foo-bar>\n"
            "</div>\n"
            "<!-- without colon -->\n"
            "<div>\n"
            "<div>\n"
            "<div> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block </div>\n"
            "<div> block </div><DIV> BLOCK </DIV> <div> block </div><div> block </div><div> block </div>\n"
            "<pre> pre pr\n"
            "e</pre>\n"
            "<textarea> pre-wrap pr\n"
            "e-wrap </textarea>\n"
            "<span> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline </span>\n"
            "<span> inline </span><span> inline </span> <span> inline </span><span> inline </span>\n"
            "<html:div> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block </html:div>\n"
            "<html:DIV> block </html:DIV><HTML:DIV> BLOCK </HTML:DIV> <html:div> block </html:div><html:div> block </html:div><html:div> block </html:div>\n"
            "<html:pre> pre pr\n"
            "e</html:pre>\n"
            "<html:textarea> pre-wrap pr\n"
            "e-wrap </html:textarea>\n"
            "<html:span> looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline </html:span>\n"
            "<html:span> inline </html:span><html:span> inline </html:span> <html:span> inline </html:span><html:span> inline </html:span></div>\n"
            "</div>\n"
            "<!-- #7236 -->\n"
            "<with:colon>\n"
            "  <div><h1> text  text  text  text  text  text  text  text  text  text  text  text  text  text </h1></div>\n"
            "  <script>\n"
            "  const func = function() { console.log('Hello, there');}\n"
            "  </script>\n"
            "  </with:colon>\n"
            "<!-- script like -->\n"
            "<with:colon>\n"
            "<style>.a{color:#f00}</style>\n"
            "  <SCRIPT>\n"
            "  const func = function() { console.log('Hello, there');}\n"
            "  </SCRIPT>\n"
            "<STYLE>.A{COLOR:#F00}</STYLE>\n"
            "<html:script>const func = function() { console.log('Hello, there');}</html:script>\n"
            "<html:style>.a{color:#f00}</html:style>\n"
            "<svg><style>.a{color:#f00}</style></svg>\n"
            "<svg><style>.a{color:#f00}</style></svg>\n"
            "</with:colon>\n"
            "<html:script>const func = function() { console.log('Hello, there');}</html:script>\n"
            "<html:style>.a{color:#f00}</html:style>\n"
        ),
        (
            "<!-- unknown tag with colon -->\n"
            "<div>\n"
            "    <foo:bar>\n"
            "        <div>\n"
            "            looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block\n"
            "        </div>\n"
            "        <div>block</div>\n"
            "        <div>BLOCK</div>\n"
            "        <div>block</div>\n"
            "        <div>block</div>\n"
            "        <div>block</div>\n"
            "        <pre>\n"
            " pre pr\n"
            "e</pre\n"
            "        >\n"
            "        <textarea>\n"
            " pre-wrap pr\n"
            "e-wrap </textarea\n"
            "        >\n"
            "        <span>\n"
            "            looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline\n"
            "        </span>\n"
            "        <span> inline </span><span> inline </span> <span> inline </span\n"
            "        ><span> inline </span>\n"
            "        <html:div>\n"
            "            looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block\n"
            "        </html:div>\n"
            "        <html:DIV> block </html:DIV><HTML:DIV> BLOCK </HTML:DIV>\n"
            "        <html:div> block </html:div><html:div> block </html:div\n"
            "        ><html:div> block </html:div>\n"
            "        <html:pre> pre pr e</html:pre>\n"
            "        <html:textarea> pre-wrap pr e-wrap </html:textarea>\n"
            "        <html:span>\n"
            "          looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline\n"
            "        </html:span>\n"
            "        <html:span> inline </html:span><html:span> inline </html:span>\n"
            "        <html:span> inline </html:span><html:span> inline </html:span></foo:bar\n"
            "        >\n"
            "    </div>\n"
            "<!-- block tag with colon -->\n"
            "<div>\n"
            "  <foo:div>\n"
            "    <div>\n"
            "      looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block\n"
            "    </div>\n"
            "    <div>block</div>\n"
            "    <div>BLOCK</div>\n"
            "    <div>block</div>\n"
            "    <div>block</div>\n"
            "    <div>block</div>\n"
            "    <pre>\n"
            " pre pr\n"
            "e</pre\n"
            "    >\n"
            "    <textarea>\n"
            " pre-wrap pr\n"
            "e-wrap </textarea\n"
            "    >\n"
            "    <span>\n"
            "      looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline\n"
            "    </span>\n"
            "    <span> inline </span><span> inline </span> <span> inline </span\n"
            "    ><span> inline </span>\n"
            "    <html:div>\n"
            "      looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block\n"
            "    </html:div>\n"
            "    <html:DIV> block </html:DIV><HTML:DIV> BLOCK </HTML:DIV>\n"
            "    <html:div> block </html:div><html:div> block </html:div\n"
            "    ><html:div> block </html:div>\n"
            "    <html:pre> pre pr e</html:pre>\n"
            "    <html:textarea> pre-wrap pr e-wrap </html:textarea>\n"
            "    <html:span>\n"
            "      looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline\n"
            "    </html:span>\n"
            "    <html:span> inline </html:span><html:span> inline </html:span>\n"
            "    <html:span> inline </html:span><html:span> inline </html:span></foo:div\n"
            "  >\n"
            "</div>\n"
            "<!-- inline tag with colon -->\n"
            "<div>\n"
            "  <foo:span>\n"
            "    <div>\n"
            "      looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block\n"
            "    </div>\n"
            "    <div>block</div>\n"
            "    <div>BLOCK</div>\n"
            "    <div>block</div>\n"
            "    <div>block</div>\n"
            "    <div>block</div>\n"
            "    <pre>\n"
            " pre pr\n"
            "e</pre\n"
            "    >\n"
            "    <textarea>\n"
            " pre-wrap pr\n"
            "e-wrap </textarea\n"
            "    >\n"
            "    <span>\n"
            "      looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline\n"
            "    </span>\n"
            "    <span> inline </span><span> inline </span> <span> inline </span\n"
            "    ><span> inline </span>\n"
            "    <html:div>\n"
            "      looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block\n"
            "    </html:div>\n"
            "    <html:DIV> block </html:DIV><HTML:DIV> BLOCK </HTML:DIV>\n"
            "    <html:div> block </html:div><html:div> block </html:div\n"
            "    ><html:div> block </html:div>\n"
            "    <html:pre> pre pr e</html:pre>\n"
            "    <html:textarea> pre-wrap pr e-wrap </html:textarea>\n"
            "    <html:span>\n"
            "      looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline\n"
            "    </html:span>\n"
            "    <html:span> inline </html:span><html:span> inline </html:span>\n"
            "    <html:span> inline </html:span><html:span> inline </html:span></foo:span\n"
            "  >\n"
            "</div>\n"
            "<!-- unknown -->\n"
            "<div>\n"
            "  <foo-bar>\n"
            "    <div>\n"
            "      looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block\n"
            "    </div>\n"
            "    <div>block</div>\n"
            "    <div>BLOCK</div>\n"
            "    <div>block</div>\n"
            "    <div>block</div>\n"
            "    <div>block</div>\n"
            "    <pre>\n"
            " pre pr\n"
            "e</pre\n"
            "    >\n"
            "    <textarea>\n"
            " pre-wrap pr\n"
            "e-wrap </textarea\n"
            "    >\n"
            "    <span>\n"
            "      looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline\n"
            "    </span>\n"
            "    <span> inline </span><span> inline </span> <span> inline </span\n"
            "    ><span> inline </span>\n"
            "    <html:div>\n"
            "      looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block\n"
            "    </html:div>\n"
            "    <html:DIV> block </html:DIV><HTML:DIV> BLOCK </HTML:DIV>\n"
            "    <html:div> block </html:div><html:div> block </html:div\n"
            "    ><html:div> block </html:div>\n"
            "    <html:pre> pre pr e</html:pre>\n"
            "    <html:textarea> pre-wrap pr e-wrap </html:textarea>\n"
            "    <html:span>\n"
            "      looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline\n"
            "    </html:span>\n"
            "    <html:span> inline </html:span><html:span> inline </html:span>\n"
            "    <html:span> inline </html:span><html:span> inline </html:span></foo-bar\n"
            "  >\n"
            "</div>\n"
            "<!-- without colon -->\n"
            "<div>\n"
            "  <div>\n"
            "    <div>\n"
            "      looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block\n"
            "    </div>\n"
            "    <div>block</div>\n"
            "    <div>BLOCK</div>\n"
            "    <div>block</div>\n"
            "    <div>block</div>\n"
            "    <div>block</div>\n"
            "    <pre>\n"
            " pre pr\n"
            "e</pre\n"
            "    >\n"
            "    <textarea>\n"
            " pre-wrap pr\n"
            "e-wrap </textarea\n"
            "    >\n"
            "    <span>\n"
            "      looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline\n"
            "    </span>\n"
            "    <span> inline </span><span> inline </span> <span> inline </span\n"
            "    ><span> inline </span>\n"
            "    <html:div>\n"
            "      looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog block\n"
            "    </html:div>\n"
            "    <html:DIV> block </html:DIV><HTML:DIV> BLOCK </HTML:DIV>\n"
            "    <html:div> block </html:div><html:div> block </html:div\n"
            "    ><html:div> block </html:div>\n"
            "    <html:pre> pre pr e</html:pre>\n"
            "    <html:textarea> pre-wrap pr e-wrap </html:textarea>\n"
            "    <html:span>\n"
            "      looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooog inline\n"
            "    </html:span>\n"
            "    <html:span> inline </html:span><html:span> inline </html:span>\n"
            "    <html:span> inline </html:span><html:span> inline </html:span>\n"
            "  </div>\n"
            "</div>\n"
            "<!-- #7236 -->\n"
            "<with:colon>\n"
            "  <div>\n"
            "    <h1>\n"
            "      text text text text text text text text text text text text text text\n"
            "    </h1>\n"
            "  </div>\n"
            "  <script>\n"
            "    const func = function () {\n"
            '      console.log("Hello, there");\n'
            "    };\n"
            "  </script>\n"
            "</with:colon>\n"
            "<!-- script like -->\n"
            "<with:colon>\n"
            "  <style>\n"
            "    .a {\n"
            "      color: #f00;\n"
            "    }\n"
            "  </style>\n"
            "  <script>\n"
            "    const func = function () {\n"
            '      console.log("Hello, there");\n'
            "    };\n"
            "  </script>\n"
            "  <style>\n"
            "    .A {\n"
            "      color: #f00;\n"
            "    }\n"
            "  </style>\n"
            "  <html:script\n"
            "    >const func = function() { console.log('Hello, there');}</html:script\n"
            "  >\n"
            "  <html:style\n"
            "    >.a{color:#f00}</html:style\n"
            "  >\n"
            "  <svg>\n"
            "    <style>\n"
            "      .a {\n"
            "        color: #f00;\n"
            "      }\n"
            "    </style>\n"
            "  </svg>\n"
            "  <svg>\n"
            "    <style>\n"
            "      .a {\n"
            "        color: #f00;\n"
            "      }\n"
            "    </style>\n"
            "  </svg>\n"
            "</with:colon>\n"
            "<html:script\n"
            "  >const func = function() { console.log('Hello, there');}</html:script\n"
            ">\n"
            "<html:style\n"
            "  >.a{color:#f00}</html:style\n"
            ">\n"
        ),
        id="with_colon",
    ),
]


@pytest.mark.parametrize("source,expected", test_data)
def test_base(source, expected, basic_config):
    output = indent_html(source, basic_config)

    printer(expected, output)
    assert expected == output
