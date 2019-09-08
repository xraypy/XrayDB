#
# xraydb documentation build configuration file

import sys, os
import xraydb

sys.path.insert(0, '.')

import authorlist_format

release = xraydb.__version__.replace('-', ' ').replace('+', ' ')
version = release = release.split(' ')[0]

project = 'xraydb'
html_title = html_short_title = 'X-ray DB:  X-ray Reference Data in SQLite'

copyright = 'Public Domain, mostly written by Matthew Newville'

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.mathjax',
              'sphinx.ext.extlinks', 'sphinxcontrib.napoleon',
              'sphinxcontrib.bibtex' ]

todo_include_todos = True

templates_path = ['_templates']
source_suffix = '.rst'
source_encoding = 'utf-8'
master_doc = 'index'
today_fmt = '%Y-%B-%d'

exclude_trees = ['_build']

add_function_parentheses = True
add_module_names = False
pygments_style = 'sphinx'

# html themes: 'default', 'sphinxdoc',  'alabaster', 'agogo', 'nature'
html_theme = 'nature'

# html_theme_options = {'pagewidth':'85em',
#                       'documentwidth':'60em',
#                       'sidebarwidth': '25em',
#                       'headercolor1': '#000080',
#                       'headercolor2': '#0000A0',
#                       }

#html_logo = None
#html_favicon = None
html_static_path = ['_static']
html_last_updated_fmt = '%Y-%B-%d'
html_show_sourcelink = True
htmlhelp_basename = 'xraydbdoc'
