from pydantic import BaseModel

class CreateIssueRequest(BaseModel):
    project_key: str
    summary: str
    description: str
    issue_type: str
    fix_version: str
    priority: str
    original_estimate: str

    issue_key: str
    issue_link: str
    status: str
    assignee: str
    reporter: str
    created: str
    updated: str

class CreateCommentRequest(BaseModel):
    text: str
    author: str
    created: str
    updated: str
