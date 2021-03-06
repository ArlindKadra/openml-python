import inspect
import os
import shutil
import unittest
import openml


class TestBase(unittest.TestCase):
    """Base class for tests

    Note
    ----
    Currently hard-codes a read-write key.
    Hopefully soon allows using a test server, not the production server.
    """

    def setUp(self):
        # This cache directory is checked in to git to simulate a populated
        # cache
        self.static_cache_dir = None
        static_cache_dir = os.path.dirname(os.path.abspath(inspect.getfile(self.__class__)))

        static_cache_dir = os.path.abspath(os.path.join(static_cache_dir, '..'))
        content = os.listdir(static_cache_dir)
        if 'files' in content:
            self.static_cache_dir = os.path.join(static_cache_dir, 'files')

        if self.static_cache_dir is None:
            raise ValueError('Cannot find test cache dir!')

        self.cwd = os.getcwd()
        workdir = os.path.dirname(os.path.abspath(__file__))
        self.workdir = os.path.join(workdir, "tmp")
        try:
            shutil.rmtree(self.workdir)
        except:
            pass

        os.mkdir(self.workdir)
        os.chdir(self.workdir)

        self.cached = True
        # amueller's read/write key that he will throw away later
        openml.config.apikey = "610344db6388d9ba34f6db45a3cf71de"
        self.production_server = openml.config.server
        self.test_server = "https://test.openml.org/api/v1/xml"
        openml.config.server = self.test_server
        openml.config.avoid_duplicate_runs = False

        openml.config.set_cache_directory(self.workdir)

    def tearDown(self):
        os.chdir(self.cwd)
        shutil.rmtree(self.workdir)
        openml.config.server = self.production_server

__all__ = ['TestBase']
