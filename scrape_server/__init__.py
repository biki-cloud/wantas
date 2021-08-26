"""
各ホスト環境でインポートするためのパスが違うため、ここで一気にsys.pathに追加する。
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.resolve()))
sys.path.append(str(Path(__file__).parent.parent.resolve()))
sys.path.append(str(Path(__file__).parent.parent.parent.resolve()))
