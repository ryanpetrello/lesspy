import os, re, errno, subprocess

__version__ = 0.1
__all__ = ['__version__', 'Less']


class Less(object):

    def __init__(self, source_path, destination_path, compress=True,
            extension='less.css'):
        """
        Used to automatically parse .less files through lessc and output CSS.

        * Recursively looks for LESS (.less/lss) files in ``source_path``
        * Saves resulting CSS files to ``destination_path``, using the same
          directory structure as the source.

        If ``compress`` is True, compiled resources will also be minified.

        ``extension`` is the file extension used for outputted files, e.g.,
        by default, ``style.less`` becomes ``style.less.css``.

        Usage:
        Less('/path/to/less/files', '/path/to/compiled').compile()
        """
        self.source_path = os.path.abspath(source_path)
        self.destination_path = os.path.abspath(destination_path)
        self.compress = compress
        self.extension = extension

    def compile(self, files=[]):
        """
        Used to compile a collection of relative (or absolute) filenames.

        When ``files`` is None or [], all ``source_path`` will be recursively
        walked and searched for .less, .lss, and .css files to compile.
        """
        files = files or self.__allfiles__
        if isinstance(files, list):
            for f in files:
                self.__compile_one__(
                    os.path.join(self.source_path, f),
                    self.__to_css__(os.path.join(self.destination_path, f))
                )

    def __compile_one__(self, source, destination):
        if self.__mtime__(destination) >= self.__mtime__(source):
            pass # nothing to do!
        else:

            if os.path.splitext(source)[1] == '.css':
                print 'Copying %s to %s' % (source, destination)
                out = open(source, 'r').read()
            else:
                print 'Compiling %s to %s' % (source, destination)
                args = ['lessc', source]
                if self.compress:
                    args.append('-x')

                p = subprocess.Popen(args, stdout=subprocess.PIPE, shell=False)
                out, err = p.communicate()

            try:
                os.makedirs(os.path.dirname(destination))
            except OSError, e:
                if e.errno != errno.EEXIST:
                    raise

            open(destination, 'w').write(out)

    def __mtime__(self, filename):
        if not os.path.isfile(filename): return 0
        return os.stat(filename).st_mtime

    def __to_css__(self, filename):
        return re.sub('(le?|c)ss$', self.extension, filename, re.I)

    @property
    def __allfiles__(self):
        print 'Searching for uncompiled LESS files...'
        matches = []
        for root, dirnames, filenames in os.walk(self.source_path):
          for filename in [f for f in filenames if f.endswith(('.less', '.lss', '.css'))]:
              matches.append(
                os.path.join(root, filename).replace(self.source_path+'/', '', 1)
              )
        return matches
