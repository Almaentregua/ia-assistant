from datetime import datetime
from typing import Dict, List
from langchain_core.tools import tool

from src.agents.dependency_assistant.nodes.conversation.repository_search import (
    MavenRepositoryClient,
)


@tool("get_versions")
def get_versions(group_id: str, artifact_id: str) -> List[Dict[str, datetime]]:
    """Fetch and parse all available versions for a given artifact."""
    maven_repository = MavenRepositoryClient()
    return maven_repository.get_versions(group_id, artifact_id)
