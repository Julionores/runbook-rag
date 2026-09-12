import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "examples"))
from generate_runbooks import generate_runbooks  # noqa: E402


@pytest.fixture(scope="session")
def runbooks_dir(tmp_path_factory):
    """Genere les 5 PDF de runbooks une seule fois par session de test, dans
    un dossier temporaire -- aucun binaire n'est verse au depot."""
    output_dir = tmp_path_factory.mktemp("runbooks")
    generate_runbooks(str(output_dir))
    return str(output_dir)
