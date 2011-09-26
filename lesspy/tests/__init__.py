from lesspy     import Less

import os
import shutil
import errno
import platform
import tempfile
import unittest

__all__ = ['suite' ,'TestLess']


class TestLess(unittest.TestCase):

    root = tempfile.gettempdir()

    LESS = 'p { color: black; &.red { color: red; } }'
    UNCOMPRESSED = 'p {\n  color: black;\n}\np.red {\n  color: red;\n}'
    COMPRESSED = 'p{color:black;}p.red{color:red;}'

    def setUp(self):
        super(TestLess, self).setUp()
        self.source = os.path.join(self.root, 'less')
        self.destination = os.path.join(self.root, 'public/css')

        # Make two temp directories for files
        try:
            os.makedirs(self.source)
            os.makedirs(self.destination)
        except OSError, e: # pragma: no cover
            if e.errno != errno.EEXIST:
                raise

    def tearDown(self):
        super(TestLess, self).tearDown()
        source = os.path.join(self.root, 'less')
        destination = os.path.join(self.root, 'public')

        # sanity check
        assert source.startswith(tempfile.gettempdir())
        assert destination.startswith(tempfile.gettempdir())

        shutil.rmtree(source)
        shutil.rmtree(destination)

    def write(self, filename, value):
        """
        Used to write a .less file relative to the tmp directory.
        """
        filename = os.path.join(self.source, filename)
        dirname, name = os.path.dirname(filename), os.path.basename(filename)
        try:
            os.makedirs(dirname)
        except OSError, e:
            if e.errno != errno.EEXIST:
                raise #pragma: no cover

        open(filename, 'w').write(value)

    def test_path_init(self):
        l = Less(self.source, self.destination)
        assert l.source_path == self.source
        assert l.destination_path == self.destination

    def test_compression_init(self):
        assert Less(self.source, self.destination).compress == True
        assert Less(
            self.source, 
            self.destination, 
            compress = False
        ).compress == False

    def test_simple_write(self):
        self.write('style.less', self.LESS)
        assert os.path.isfile(os.path.join(self.source, 'style.less'))
        value = open(os.path.join(self.source, 'style.less'), 'r').read()
        assert value == self.LESS

    def test_recursive_write(self):
        self.write('foo/style.less', self.LESS)
        assert os.path.isfile(os.path.join(self.source, 'foo/style.less'))
        value = open(os.path.join(self.source, 'foo/style.less'), 'r').read()
        assert value == self.LESS

    def test_compile_single_less_file(self):
        self.write('style.less', self.LESS)
        written_files = Less(self.source, self.destination).compile([
            'style.less'
        ])
        assert written_files == [
            os.path.join(self.destination, 'style.css') 
        ]
        val = open(os.path.join(self.destination, 'style.css'), 'r').read()
        assert val.strip() == self.COMPRESSED.strip()

    def test_compile_extension(self):
        self.write('style.less', self.LESS)
        self.write('raw.css', self.COMPRESSED)
        written_files = Less(
            self.source, 
            self.destination, 
            compiled_extension='min.css'
        ).compile(['style.less', 'raw.css'])

        assert os.path.join(self.destination, 'style.min.css') in written_files
        assert os.path.join(self.destination, 'raw.css') in written_files

        val = open(os.path.join(self.destination, 'style.min.css'), 'r').read()
        assert val.strip() == self.COMPRESSED.strip()

        val = open(os.path.join(self.destination, 'raw.css'), 'r').read()
        assert val.strip() == self.COMPRESSED.strip()

    def test_compile_without_compression(self):
        self.write('style.less', self.LESS)
        written_files = Less(
            self.source, 
            self.destination, 
            compress=False
        ).compile([
            'style.less'
        ])
        assert written_files == [
            os.path.join(self.destination, 'style.css') 
        ]
        val = open(os.path.join(self.destination, 'style.css'), 'r').read()
        assert val.strip() == self.UNCOMPRESSED.strip()

    def test_compile_single_lss_file(self):
        self.write('style.lss', self.LESS)
        written_files = Less(self.source, self.destination).compile([
            'style.lss'
        ])
        assert written_files == [
            os.path.join(self.destination, 'style.css') 
        ]
        val = open(os.path.join(self.destination, 'style.css'), 'r').read()
        assert val.strip() == self.COMPRESSED.strip()

    def test_compile_single_css_file(self):
        self.write('raw.css', self.COMPRESSED)
        written_files = Less(self.source, self.destination).compile([
            'raw.css'
        ])
        assert written_files == [
            os.path.join(self.destination, 'raw.css') 
        ]
        val = open(os.path.join(self.destination, 'raw.css'), 'r').read()
        assert val.strip() == self.COMPRESSED.strip()

    def test_multiple_files(self):
        self.write('one.less', self.LESS)
        self.write('two.lss', self.LESS)
        self.write('raw.css', self.COMPRESSED)
        written_files = Less(self.source, self.destination).compile([
            'one.less', 'two.lss', 'raw.css'
        ])
        assert os.path.join(self.destination, 'one.css') in written_files
        assert os.path.join(self.destination, 'two.css') in written_files
        assert os.path.join(self.destination, 'raw.css') in written_files

        val = open(os.path.join(self.destination, 'one.css'), 'r').read()
        assert val.strip() == self.COMPRESSED.strip()

        val = open(os.path.join(self.destination, 'two.css'), 'r').read()
        assert val.strip() == self.COMPRESSED.strip()

        val = open(os.path.join(self.destination, 'raw.css'), 'r').read()
        assert val.strip() == self.COMPRESSED.strip()

    def test_autodiscover(self):
        self.write('root.less', self.LESS)
        self.write('raw.css', self.COMPRESSED)
        self.write('sub/sub.LESS', self.LESS)
        self.write('sub/sub/sub.lss', self.LESS)
        self.write('sub/sub/sub/raw.CSS', self.COMPRESSED)
        written_files = Less(self.source, self.destination).compile()

        for fname in (
            'root.css', 
            'raw.css', 
            'sub/sub.css',
            'sub/sub/sub.css',
            'sub/sub/sub/raw.CSS'
        ):
            assert os.path.join(self.destination, fname) in written_files
            val = open(os.path.join(self.destination, fname), 'r').read()
            assert val.strip() == self.COMPRESSED.strip()

    def test_mtime_change(self):
        self.write('style.less', self.LESS)
        written_files = Less(self.source, self.destination).compile([
            'style.less'
        ])
        assert written_files == [
            os.path.join(self.destination, 'style.css') 
        ]
        val = open(os.path.join(self.destination, 'style.css'), 'r').read()
        assert val.strip() == self.COMPRESSED.strip()

        #
        # The mtimes of the compiled files haven't changed, so no new files
        # should have been written.
        #
        written_files = Less(self.source, self.destination).compile([
            'style.less'
        ])
        assert written_files == []

        # Touch a source file
        fname = os.path.join(self.source, 'style.less')
        with file(fname, 'a'):
            st = os.stat(fname)
            os.utime(fname, (st.st_atime, st.st_mtime + (5)))
            if platform.system() == 'Windows': # pragma: no cover
                time.sleep(3) # give (ahem) certain OS's a chance to catch up

        written_files = Less(self.source, self.destination).compile([
            'style.less'
        ])
        assert written_files == [
            os.path.join(self.destination, 'style.css') 
        ]

suite = unittest.TestLoader().loadTestsFromTestCase(TestLess)
