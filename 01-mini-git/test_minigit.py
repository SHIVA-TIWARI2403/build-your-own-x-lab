import os
import shutil
import tempfile
import unittest
import minigit

class TestMiniGit(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="minigit_test_")
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_init(self):
        minigit.init()
        self.assertTrue(os.path.exists(".minigit/objects"))
        self.assertTrue(os.path.exists(".minigit/refs/heads"))
        self.assertTrue(os.path.exists(".minigit/HEAD"))
        with open(".minigit/HEAD", "r") as f:
            self.assertEqual(f.read().strip(), "ref: refs/heads/main")

    def test_hash_object_and_cat_file(self):
        minigit.init()
        sample_data = b"Hello, MiniGit Architecture!"
        obj_hash = minigit.hash_object(sample_data, obj_type="blob", write=True)
        self.assertEqual(len(obj_hash), 40)

        obj_type, recovered_data = minigit.cat_file(obj_hash)
        self.assertEqual(obj_type, "blob")
        self.assertEqual(recovered_data, sample_data)

    def test_commit_lifecycle(self):
        minigit.init()
        with open("hello.txt", "w", encoding="utf-8") as f:
            f.write("Line 1: System started\n")

        commit1 = minigit.commit("Initial commit", author="Shiva <shiva@test.com>")
        self.assertEqual(len(commit1), 40)

        with open("hello.txt", "a", encoding="utf-8") as f:
            f.write("Line 2: New feature added\n")

        commit2 = minigit.commit("Second commit", author="Shiva <shiva@test.com>")
        self.assertEqual(len(commit2), 40)
        self.assertNotEqual(commit1, commit2)

        # Verify parent link
        _, commit2_body = minigit.cat_file(commit2)
        self.assertIn(f"parent {commit1}".encode("utf-8"), commit2_body)

if __name__ == "__main__":
    unittest.main()
