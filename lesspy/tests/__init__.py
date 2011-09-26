from lesspy     import Less
from unittest   import TestCase

import os
import shutil
import errno
import tempfile


class TestLess(TestCase):

    root = tempfile.gettempdir()

    LESS = 'p { color: black; &.red { color: red; } }'
    COMPILED = 'p{color:black;}p.red{color:red;}'

    def setUp(self):
        super(TestLess, self).setUp()
        self.source = os.path.join(self.root, 'less')
        self.destination = os.path.join(self.root, 'public/css')

        # Make two temp directories for files
        try:
            os.makedirs(self.source)
            os.makedirs(self.destination)
        except OSError, e:
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
                raise

        open(filename, 'w').write(value)

    @property
    def written_files(self):
        return sum([[os.path.join(r,f) for f in files]
                for r, d, files in os.walk(self.destination)], [])
    
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

    def test_compile_no_files(self):
        Less(self.source, self.destination).compile([])
        assert self.written_files == []

    def test_compile_single_less_file(self):
        self.write('style.less', self.LESS)
        Less(self.source, self.destination).compile(['style.less'])
        assert self.written_files == [
            os.path.join(self.destination, 'style.css') 
        ]
        val = open(os.path.join(self.destination, 'style.css'), 'r').read()
        assert val.strip() == self.COMPILED.strip()

    def test_compile_single_lss_file(self):
        self.write('style.lss', self.LESS)
        Less(self.source, self.destination).compile(['style.lss'])
        assert self.written_files == [
            os.path.join(self.destination, 'style.css') 
        ]
        val = open(os.path.join(self.destination, 'style.css'), 'r').read()
        assert val.strip() == self.COMPILED.strip()

    def test_compile_single_css_file(self):
        self.write('raw.css', self.COMPILED)
        Less(self.source, self.destination).compile(['raw.css'])
        assert self.written_files == [
            os.path.join(self.destination, 'raw.css') 
        ]
        val = open(os.path.join(self.destination, 'raw.css'), 'r').read()
        assert val.strip() == self.COMPILED.strip()
