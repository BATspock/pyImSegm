# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import glob
import inspect
import os
import re
import shutil
import sys

import m2r

PATH_UP = os.path.join('..', '..')
PATH_HERE = os.path.abspath(os.path.dirname(__file__))
PATH_ROOT = os.path.realpath(os.path.join(PATH_HERE, PATH_UP))
sys.path.insert(0, os.path.abspath(PATH_ROOT))

import imsegm  # noqa: E402

# -- Project information -----------------------------------------------------

project = 'ImSegm'
copyright = imsegm.__copyright__
author = imsegm.__author__

# The short X.Y version
version = imsegm.__version__
# The full version, including alpha/beta/rc tags
release = imsegm.__version__

# Options for the linkcode extension
# ----------------------------------
github_user = 'Borda'
github_repo = 'pyImSegm'

# -- Project documents -------------------------------------------------------

# export the documentation
with open('intro.rst', 'w') as fp:
    intro = imsegm.__long_doc__.replace(os.linesep + ' ', '')
    fp.write(m2r.convert(intro))
    # fp.write(imsegm.__doc__)

# export the READme
with open(os.path.join(PATH_ROOT, 'README.md'), 'r') as fp:
    readme = fp.read()
# replace all paths to relative
readme = readme.replace('](docs/source/', '](')
# Todo: this seems to replace only once per line
readme = re.sub(
    r' \[(.*)\]\((?!http)(.*)\)',
    r' [\1](https://github.com/%s/%s/blob/master/\2)' % (github_user, github_repo),
    readme,
)
# TODO: temp fix removing SVG badges and GIF, because PDF cannot show them
readme = re.sub(r'(\[!\[.*\))', '', readme)
readme = re.sub(r'(!\[.+\.[gif|svg|pdf].*\))', '', readme)
for dir_name in (os.path.basename(p) for p in glob.glob(os.path.join(PATH_ROOT, '*')) if os.path.isdir(p)):
    readme = readme.replace('](%s/' % dir_name, '](%s/%s/' % (PATH_UP, dir_name))
with open('readme.md', 'w') as fp:
    fp.write(readme)

# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.

needs_sphinx = '2.4'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    # 'sphinx.ext.viewcode',
    'sphinx.ext.linkcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosummary',
    # 'sphinxcontrib.rsvgconverter'
    'myst_parser',
    'nbsphinx',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# https://berkeley-stat159-f17.github.io/stat159-f17/lectures/14-sphinx..html#conf.py-(cont.)
# https://stackoverflow.com/questions/38526888/embed-ipython-notebook-in-sphinx-document
# I execute the notebooks manually in advance. If notebooks test the code,
# they should be run at build time.
nbsphinx_execute = 'never'
nbsphinx_allow_errors = True

myst_update_mathjax = False

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = ['.rst', '.md', '.ipynb']

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    'data-images',
    '*tests.*',
    '*.test_*',
    '*.so',
    '*.dll',
    'api/modules.rst',
    '*/transform-img-plane_inter-circle.ipynb',
]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = None

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
# http://www.sphinx-doc.org/en/master/usage/theming.html#builtin-themes
html_theme = 'nature'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []  # , '_static', 'notebooks'

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}

# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = project + 'Doc'

# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    # 'preamble': '',

    # Latex figure (float) alignment
    'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, project + '.tex', project + ' Documentation', author, 'manual'),
]

# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, project, project + ' Documentation', [author], 1)]

# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [(
    master_doc, project, project + ' Documentation', author, project, 'One line description of project.',
    'Miscellaneous'
)]

# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']

# -- Extension configuration -------------------------------------------------

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'https://docs.python.org/': None}

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# https://github.com/rtfd/readthedocs.org/issues/1139
# I use sphinx-apidoc to auto-generate API documentation for my project.
# Right now I have to commit these auto-generated files to my repository
# so that RTD can build them into HTML docs. It'd be cool if RTD could run
# sphinx-apidoc for me, since it's easy to forget to regen API docs
# and commit them to my repo after making changes to my code.

PACKAGES = [imsegm.__name__]


def run_apidoc(_):
    for pkg in PACKAGES:
        argv = ['-e', '-o', os.path.join(PATH_HERE, 'api'), os.path.join(PATH_ROOT, pkg), 'tests/*', '--force']
        try:
            # Sphinx 1.7+
            from sphinx.ext import apidoc
            apidoc.main(argv)
        except ImportError:
            # Sphinx 1.6 (and earlier)
            from sphinx import apidoc
            argv.insert(0, apidoc.__file__)
            apidoc.main(argv)


def setup(app):
    app.connect('builder-inited', run_apidoc)


# copy all notebooks to local folder
path_docs_nbs = os.path.join(PATH_HERE, 'notebooks')
if not os.path.isdir(path_docs_nbs):
    os.mkdir(path_docs_nbs)
for path_ipynb_in in glob.glob(os.path.join(PATH_ROOT, 'notebooks', '*.ipynb')):
    path_ipynb_new = os.path.join(path_docs_nbs, os.path.basename(path_ipynb_in))
    shutil.copy(path_ipynb_in, path_ipynb_new)

# Ignoring Third-party packages
# https://stackoverflow.com/questions/15889621/sphinx-how-to-exclude-imports-in-automodule
PACKAGE_MAPPING = {
    'scikit-learn': 'sklearn',
    'scikit-image': 'skimage',
    'pillow': 'PIL',
    'pygco': 'gco',
    'pyyaml': 'yaml',
    'olefile': 'OleFileIO_PL',
}
MOCK_MODULES = []
with open(os.path.join(PATH_ROOT, 'requirements.txt'), 'r') as fp:
    for ln in fp.readlines():
        found = [ln.index(ch) for ch in list(',=<>#') if ch in ln]
        pkg = ln[:min(found)] if found else ln
        if pkg.rstrip():
            MOCK_MODULES.append(pkg.rstrip())

autodoc_mock_imports = [PACKAGE_MAPPING.get(pkg.lower(), pkg) for pkg in MOCK_MODULES]


# Resolve function
# This function is used to populate the (source) links in the API
def linkcode_resolve(domain, info):

    def find_source():
        # try to find the file and line number, based on code from numpy:
        # https://github.com/numpy/numpy/blob/master/doc/source/conf.py#L286
        obj = sys.modules[info['module']]
        for part in info['fullname'].split('.'):
            obj = getattr(obj, part)
        fname = inspect.getsourcefile(obj)
        # https://github.com/rtfd/readthedocs.org/issues/5735
        if any([s in fname for s in ('readthedocs', 'rtfd', 'checkouts')]):
            path_top = os.path.abspath(os.path.join('..', '..', '..'))
            fname = os.path.relpath(fname, start=path_top)
        else:
            # Local build, imitate master
            fname = 'master/' + os.path.relpath(fname, start=os.path.abspath('..'))
        source, lineno = inspect.getsourcelines(obj)
        return fname, lineno, lineno + len(source) - 1

    if domain != 'py' or not info['module']:
        return None
    try:
        filename = '%s#L%d-L%d' % find_source()
    except Exception:
        filename = info['module'].replace('.', '/') + '.py'
    # import subprocess
    # tag = subprocess.Popen(['git', 'rev-parse', 'HEAD'], stdout=subprocess.PIPE,
    #                        universal_newlines=True).communicate()[0][:-1]
    branch = filename.split('/')[0]
    # do mapping from latest tags to master
    branch = {'latest': 'master', 'stable': 'master'}.get(branch, branch)
    filename = '/'.join([branch] + filename.split('/')[1:])
    return "https://github.com/%s/%s/blob/%s" \
           % (github_user, github_repo, filename)


autodoc_member_order = 'groupwise'
autoclass_content = 'both'
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'private-members': True,
    'methods': True,
    'exclude-members': '_abc_impl',
    'show-inheritance': True,
}
