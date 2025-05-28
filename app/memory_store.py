from typing import Dict, List
from threading import Lock


class InMemoryPostStore:
    """Thread-safe in-memory store for user posts."""

    def __init__(self):
        """Initialize empty posts, user-post mapping, lock, and post ID counter."""
        self._posts: Dict[int, Dict] = {}
        self._user_posts: Dict[str, List[int]] = {}
        self._lock = Lock()
        self._next_post_id = 1

    def add_post(self, user_id: str, text: str) -> int:
        """Add a post with user ID and text; return new post ID."""
        with self._lock:
            post_id = self._next_post_id
            self._next_post_id += 1

            post = {"postID": post_id, "user_id": user_id, "text": text}
            self._posts[post_id] = post

            if user_id not in self._user_posts:
                self._user_posts[user_id] = []
            self._user_posts[user_id].append(post_id)

            return post_id

    def get_posts_for_user(self, user_id: str) -> List[Dict]:
        """Return list of posts belonging to given user ID."""
        post_ids = self._user_posts.get(user_id, [])
        return [self._posts[pid] for pid in post_ids]

    def delete_post(self, user_id: str, post_id: int) -> bool:
        """Delete post by ID if it belongs to user; return True if deleted."""
        with self._lock:
            post = self._posts.get(post_id)
            if post and post["user_id"] == user_id:
                del self._posts[post_id]
                self._user_posts[user_id].remove(post_id)
                return True
            return False
