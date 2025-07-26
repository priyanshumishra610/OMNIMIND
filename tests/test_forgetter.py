"""
Tests for Forgetter — SentraAGI Phase 21: The Final Sovereign Trials
"""

import pytest
import time
from memory.forgetter import Forgetter, MemoryShard, ForgettingReceipt


class TestForgetter:
    """Test cases for Forgetter."""

    def test_instantiation(self):
        """Test Forgetter instantiation."""
        forgetter = Forgetter()
        assert forgetter.memory_manager is None
        assert forgetter.ledger_pipeline is None
        assert len(forgetter.forgotten_shards) == 0

    def test_instantiation_with_dependencies(self):
        """Test Forgetter instantiation with dependencies."""
        mock_memory_manager = object()
        mock_ledger_pipeline = object()
        forgetter = Forgetter(mock_memory_manager, mock_ledger_pipeline)
        assert forgetter.memory_manager == mock_memory_manager
        assert forgetter.ledger_pipeline == mock_ledger_pipeline

    def test_score_shard(self):
        """Test scoring memory shards."""
        forgetter = Forgetter()
        
        # Create test shards
        shard1 = MemoryShard("1", "old data", time.time() - 3600, 0.8, 0.9, 1)
        shard2 = MemoryShard("2", "new data", time.time(), 0.2, 0.1, 10)
        
        # Score shards
        score1 = forgetter.score_shard(shard1)
        score2 = forgetter.score_shard(shard2)
        
        assert isinstance(score1, float)
        assert isinstance(score2, float)
        assert score1 > score2  # Old, high entropy shard should score higher

    def test_score_shard_edge_cases(self):
        """Test scoring shards with edge cases."""
        forgetter = Forgetter()
        
        # Test with zero access count
        shard = MemoryShard("test", "data", time.time(), 0.5, 0.5, 0)
        score = forgetter.score_shard(shard)
        assert isinstance(score, float)
        assert score > 0

    def test_forget_stale_data_no_memory_manager(self):
        """Test forgetting when no memory manager is connected."""
        forgetter = Forgetter()
        receipt = forgetter.forget_stale_data()
        
        assert isinstance(receipt, ForgettingReceipt)
        assert len(receipt.shard_ids) == 0
        assert receipt.reason == "no_memory_manager"
        assert receipt.total_size_freed == 0

    def test_forget_stale_data_with_threshold(self):
        """Test forgetting with different thresholds."""
        forgetter = Forgetter()
        
        # Test with high threshold (should forget nothing)
        receipt1 = forgetter.forget_stale_data(threshold=1.0)
        assert len(receipt1.shard_ids) == 0
        
        # Test with low threshold (should forget everything)
        receipt2 = forgetter.forget_stale_data(threshold=0.0)
        # Since no actual shards are available, this should still return empty

    def test_get_forgetting_stats(self):
        """Test getting forgetting statistics."""
        forgetter = Forgetter()
        
        # Add some forgotten shards
        shard1 = MemoryShard("1", "forgotten1", time.time(), 0.5, 0.5, 1)
        shard2 = MemoryShard("2", "forgotten2", time.time(), 0.5, 0.5, 1)
        forgetter.forgotten_shards = [shard1, shard2]
        
        stats = forgetter.get_forgetting_stats()
        
        assert stats["total_forgotten"] == 2
        assert stats["total_size_freed"] > 0
        assert "1" in stats["forgotten_ids"]
        assert "2" in stats["forgotten_ids"]

    def test_get_forgetting_stats_empty(self):
        """Test getting forgetting statistics when no shards forgotten."""
        forgetter = Forgetter()
        stats = forgetter.get_forgetting_stats()
        
        assert stats["total_forgotten"] == 0
        assert stats["total_size_freed"] == 0
        assert len(stats["forgotten_ids"]) == 0

    def test_forgetting_receipt_structure(self):
        """Test ForgettingReceipt structure."""
        receipt = ForgettingReceipt(
            shard_ids=["1", "2", "3"],
            reason="test_reason",
            timestamp=time.time(),
            total_size_freed=1024
        )
        
        assert len(receipt.shard_ids) == 3
        assert receipt.reason == "test_reason"
        assert receipt.timestamp > 0
        assert receipt.total_size_freed == 1024

    def test_memory_shard_structure(self):
        """Test MemoryShard structure."""
        shard = MemoryShard(
            id="test_id",
            content="test_content",
            timestamp=time.time(),
            relevance_score=0.7,
            entropy_score=0.3,
            access_count=5
        )
        
        assert shard.id == "test_id"
        assert shard.content == "test_content"
        assert shard.relevance_score == 0.7
        assert shard.entropy_score == 0.3
        assert shard.access_count == 5

    def test_full_loop_proof(self):
        """Test complete forgetting workflow."""
        forgetter = Forgetter()
        
        # Create test shards
        shards = [
            MemoryShard("1", "old data", time.time() - 7200, 0.9, 0.8, 1),
            MemoryShard("2", "medium data", time.time() - 3600, 0.5, 0.5, 3),
            MemoryShard("3", "new data", time.time(), 0.1, 0.2, 10)
        ]
        
        # Score all shards
        scores = []
        for shard in shards:
            score = forgetter.score_shard(shard)
            scores.append(score)
        
        # Verify scoring logic
        assert scores[0] > scores[1]  # Oldest should score highest
        assert scores[1] > scores[2]  # Medium should score higher than newest
        
        # Test forgetting with different thresholds
        receipt_low = forgetter.forget_stale_data(threshold=0.3)
        receipt_high = forgetter.forget_stale_data(threshold=0.8)
        
        # Both should return valid receipts
        assert isinstance(receipt_low, ForgettingReceipt)
        assert isinstance(receipt_high, ForgettingReceipt)
        
        # Get stats
        stats = forgetter.get_forgetting_stats()
        assert isinstance(stats, dict)
        assert "total_forgotten" in stats
        assert "total_size_freed" in stats
        assert "forgotten_ids" in stats


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 