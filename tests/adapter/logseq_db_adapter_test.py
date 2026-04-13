import os
from transit.writer import Writer
import pytest

from adapter.logseq_db_adapter import LogseqDBAdapter

# path to sample logseq transit file located in project root
SAMPLE_DB_PATH = os.path.join(os.path.dirname(__file__), "../..", "sample_logseq_db")

class TestLogseqDBAdapterReadAll:
    def test_given_a_transit_file_exists_when_reading_it_then_data_is_returned(self):
        adapter = LogseqDBAdapter(SAMPLE_DB_PATH)
        adapter.read_all()
        
        assert adapter.db["69dcbbc8-1e3d-437e-80f5-ca52449bcfcb"].content == "Chroma is the open-source data infrastructure for AI. It comes with everything you need to get started built-in."

    def test_given_nonexistent_file_when_reading_it_then_error_is_raised(self):
        nonexistent_path = "/nonexistent/path/to/file.transit"
        
        with pytest.raises(FileNotFoundError):
            adapter = LogseqDBAdapter(nonexistent_path)
            adapter.read_all()

class TestLogseqDBAdapterDbFilePathFromJournalPath:
    def test_given_a_directory_path_when_formatting_then_slashes_are_replaced_with_plus_signs(self):
        directory_path = "/Users/erica/notes"
        
        result = LogseqDBAdapter.db_file_path_from_journal_path(directory_path)
        
        assert result == "/Users/erica/.logseq/graphs/logseq_local_++Users++erica++notes.transit"

    def test_given_a_home_directory_path_when_formatting_then_tilde_is_expanded(self):
        directory_path = "~/notes"
        
        result = LogseqDBAdapter.db_file_path_from_journal_path(directory_path)
        
        assert result.startswith("/Users/")
        assert "notes" in result