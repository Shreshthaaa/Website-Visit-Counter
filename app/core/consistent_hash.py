import hashlib
from typing import List, Dict
from bisect import bisect_left, insort

class ConsistentHash:
    def __init__(self, nodes: List[str]=[], virtual_nodes: int = 100):
        """
        Initialize the consistent hash ring

        Args:
            nodes: List of node identifiers (parsed from comma-separated string)
            virtual_nodes: Number of virtual nodes per physical node
        """
        self.virtual_nodes = virtual_nodes
        self.hash_ring: Dict[int, str] = {}
        self.sorted_keys: List[int] = []

        for node in nodes:
            self.add_node(node)

    def _hash(self, key: str) -> int:
        """Return a consistent hash value using MD5."""
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def add_node(self, node: str) -> None:
        """
        Add a new node to the hash ring
        
        Args:
            node: Node identifier to add
        """
        for i in range(self.virtual_nodes):
            virtual_node_id = f"{node}#{i}"
            hash_val = self._hash(virtual_node_id)

            if hash_val not in self.hash_ring:
                insort(self.sorted_keys, hash_val)
                self.hash_ring[hash_val] = node

    def remove_node(self, node: str) -> None:
        """
        Remove a node from the hash ring
        
        Args:
            node: Node identifier to remove
        """
        for i in range(self.virtual_nodes):
            virtual_node_id = f"{node}#{i}"
            hash_val = self._hash(virtual_node_id)

            index = bisect_left(self.sorted_keys, hash_val)
            if index < len(self.sorted_keys) and self.sorted_keys[index] == hash_val:
                del self.hash_ring[hash_val]
                del self.sorted_keys[index]

    def get_node(self, key: str) -> str:
        """
        Get the node responsible for the given key
        
        Args:
            key: The key to look up
            
        Returns:
            The node responsible for the key
        """
        if not self.hash_ring:
            return None

        hash_val = self._hash(key)
        index = bisect_left(self.sorted_keys, hash_val)

        if index == len(self.sorted_keys):
            index = 0

        return self.hash_ring[self.sorted_keys[index]]