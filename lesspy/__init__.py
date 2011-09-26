import os, re, errno, subprocess

__version__ = 0.1
__all__ = ['__version__', 'Less']

__LESS_MISSING__ = "`lessc` could not found on the system path.  Please \
ensure that you've properly installed the LESS compiler (http://lesscss.org/)."

def _executable(less): #pragma: no cover
    def is_exe(fpath):
        return os.path.exists(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(less)
    if fpath:
        if is_exe(less):
            return True
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, less)
            if is_exe(exe_file):
                return True

    return False


class Less(object):
    """
    Used to automatically parse LESS files through ``lessc`` and output CSS.

    * Recursively looks for LESS (.less/.lss/.css) files in ``source_path``
    * Saves compiled CSS files to ``destination_path``, using the same
      directory structure as the source.

    If ``compress`` is True, compiled resources will also be minified.

    ``compiled_extension`` is the file extension used for compiled files,
    e.g., by default, ``style.less`` becomes ``style.css``.

    By default, the ``lessc`` executable will be searched for on the system
    path.  Optionally, ``less_path`` can be used to specify an absolute
    path to the ``lessc`` executable, e.g., ``"/some/path/to/less"``
    """

    CSS_RE = re.compile('(le?|c)ss$', re.I)

    def __init__(self, source_path, destination_path, compress=True,
            compiled_extension='css', less_path=''):
        self.source_path = os.path.abspath(source_path)
        self.destination_path = os.path.abspath(destination_path)
        self.compress = compress
        self.compiled_extension = compiled_extension
        self.lessc = os.path.join(less_path, 'lessc')

    def compile(self, files=[]):
        """
        Compile a list of relative (or absolute) filenames.

        When ``files`` is None or empty, ``Less.source_path`` will be
        recursively walked and searched for .less, .lss, and .css files to
        compile.

        Returns a list of absolute pathnames of written files, e.g.,
        ``['/compiled/path/style.css', '/compiled/path/example.css']``
        """
        written = []
        files = files or self.__allfiles__
        if isinstance(files, list):
            for f in files:
                written.append(self.__compile_one__(
                    os.path.join(self.source_path, f),
                    os.path.join(self.destination_path, f)
                ))
        return filter(None, written)

    def __compile_one__(self, source, destination):
        if os.path.splitext(source)[1].lower() == '.css':
            if self.__mtime__(destination) >= self.__mtime__(source):
                return
            print 'Copying %s to %s' % (source, destination)
            out = open(source, 'r').read()
        else:
            destination = self.__to_css__(destination)
            if self.__mtime__(destination) >= self.__mtime__(source):
                return
            #
            # First, attempt to call lessc without arguments (to ensure
            # that it exists and is executable on the path somewhere)
            #
            if not _executable(self.lessc):
                raise RuntimeError, __LESS_MISSING__ #pragma: no cover

            print 'Compiling %s to %s' % (source, destination)
            args = [self.lessc, source]
            if self.compress:
                args.append('-x')

            p = subprocess.Popen(args, stdout=subprocess.PIPE)
            out, err = p.communicate()

        try:
            os.makedirs(os.path.dirname(destination))
        except OSError, e:
            if e.errno != errno.EEXIST: #pragma: no cover
                raise

        open(destination, 'w').write(out)
        return destination

    def __mtime__(self, filename):
        if not os.path.isfile(filename): return 0
        return os.stat(filename).st_mtime

    def __to_css__(self, filename):
        return self.CSS_RE.sub(self.compiled_extension, filename)

    @property
    def __allfiles__(self):
        print 'Searching for uncompiled LESS files...'
        matches = []
        for root, dirnames, filenames in os.walk(self.source_path):
          for filename in [f for f in filenames if f.lower().endswith(('.less', '.lss', '.css'))]:
              matches.append(
                os.path.join(root, filename).replace(self.source_path+'/', '', 1)
              )
        return matches
