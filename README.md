lesspy
======
Helps compile collections of .less files into CSS files

* Given a source directory, recursively finds LESS (.less/lss) files
* Saves resulting CSS files to a destination_path, using the same
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

---

LESS
----
lesspy depends on LESS

LESS extends CSS with: variables, mixins, operations and nested rules. For more information, see http://lesscss.org.

Usage
-----

    # Compile specific .less files to .css
    lesspy.Less('/path/to/less/files', '/path/to/compiled').compile([
        'uncompiled.less',
        'uncompiled2.lss'
        'raw.css'
    ])

    # Auto-detect .less files and convert them to .css
    lesspy.Less('/path/to/less/files', '/path/to/compiled').compile()
