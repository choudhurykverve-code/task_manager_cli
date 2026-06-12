import sys
import os

# Ensure the project root is on sys.path so that `models`, `services`, and
# `storage` packages can be imported without installing the project.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
