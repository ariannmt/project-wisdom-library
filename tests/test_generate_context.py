import os
import shutil
import unittest
import sys
from tools import generate_context

class TestGenerateContext(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_env"
        self.target_slug = "test-target"
        os.makedirs(self.test_dir, exist_ok=True)

        # Map folders to their expected levels for test generation
        folder_map = {
            "analyses": 1,
            "atomic": 2,
            "process_memory": 3,
            "distillations": 4,
            "backlog": 5
        }

        for folder, level in folder_map.items():
            path = os.path.join(self.test_dir, folder, self.target_slug)
            os.makedirs(path, exist_ok=True)
            with open(os.path.join(path, f"file_lvl_{level}.md"), "w") as f:
                f.write(f"# Content for {folder}")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_scan_files(self):
        files = generate_context.scan_files(self.test_dir, self.target_slug)

        self.assertEqual(len(files), 5)

        # Check sorting: Level 1 -> Level 5
        for i, file_info in enumerate(files):
            expected_level = i + 1
            self.assertEqual(file_info["level"], expected_level)

            # Verify category mapping logic
            if expected_level == 1:
                self.assertEqual(file_info["category"], "analyses")
            elif expected_level == 2:
                self.assertEqual(file_info["category"], "atomic")
            elif expected_level == 3:
                self.assertEqual(file_info["category"], "process_memory")
            elif expected_level == 4:
                self.assertEqual(file_info["category"], "distillations")
            elif expected_level == 5:
                self.assertEqual(file_info["category"], "backlog")

    def test_generate_toc(self):
        files = []
        folder_map = {
            "analyses": 1,
            "atomic": 2,
            "process_memory": 3,
            "distillations": 4,
            "backlog": 5
        }
        # Recreate file list for TOC generation
        for folder, level in folder_map.items():
            files.append({
                "filename": f"file_lvl_{level}.md",
                "category": folder,
                "level": level
            })

        # scan_files sorts them, so we should sort them here to match expected input to generate_toc
        files.sort(key=lambda x: x["level"])

        toc = generate_context.generate_toc(files)

        self.assertIn("## Level 1: Analyses", toc)
        self.assertIn("- file_lvl_1.md (analyses)", toc)

        self.assertIn("## Level 2: Atomic", toc)
        self.assertIn("- file_lvl_2.md (atomic)", toc)

        self.assertIn("## Level 3: Process Memory", toc)
        self.assertIn("- file_lvl_3.md (process_memory)", toc)

        self.assertIn("## Level 4: Distillations", toc)
        self.assertIn("- file_lvl_4.md (distillations)", toc)

        self.assertIn("## Level 5: Backlog", toc)
        self.assertIn("- file_lvl_5.md (backlog)", toc)

if __name__ == "__main__":
    unittest.main()
