lesspy
======
Helps compile collections of LESS files into CSS files

* Given a source directory, recursively finds LESS (.less/.lss/.css) files
* Saves compiled CSS files to a destination path, using the same
  directory structure as the source, e.g.,

        ./source
        |-- shared
        |   |-- one.less
        |   `-- two.lss
        |-- three.less
        `-- four.css

    ...is compiled to...

        ./dest
        |-- shared
        |   |-- one.css
        |   `-- two.css
        |-- three.css
        `-- four.css

LESS
----
lesspy depends on LESS (http://lesscss.org/).

LESS extends CSS with dynamic behavior such as variables, mixins, operations
and functions.

Usage
-----

    # Compile specific .less files to .css
    lesspy.Less('/path/to/less/files', '/path/to/compiled').compile([
        'uncompiled.less',
        'uncompiled2.lss',
        'raw.css'
    ])

    # Auto-detect .less files and convert them to .css
    lesspy.Less('/path/to/less/files', '/path/to/compiled').compile()

CSS minification is enabled by default, but can be disabled optionally:

    lesspy.Less('/from', '/to', compress=False).compile()
