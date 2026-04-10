import os
import sys

sys.path.insert(0, os.path.abspath('../..'))

project = 'System Resource Dashboard'
copyright = '2026'
author = 'HEO7777'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
master_doc = 'index'

autodoc_member_order = 'bysource'
