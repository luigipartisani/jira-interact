from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.requestDto import CreateIssueRequest
from backend.jiraUtils import get_issue

router = APIRouter()

class Item(BaseModel):
    id: int
    title: str


@router.get("/issue/{issueKey}", summary="Recupera la issue con chiave {issueKey}")
def get_js_issue(issueKey: str):
    
    try:

        print(f"Get issue {issueKey} from Jira Server...")
        return get_issue("Server", issueKey)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/issue/{issueKey}/comment", summary="Crea un nuovo commento nella issue con chiave {issueKey}")
def create_js_issue_comment(item: CreateIssueRequest):

    if item.x_api_key == "gg":
        result = "ok"
        return result
    return "error"

@router.post("/issue/{issueKey}/update", summary="Aggiorna la issue con chiave {issueKey}")
def update_js_issue(item: CreateIssueRequest):

    if item.x_api_key == "gg":
        result = "ok"
        return result
    return "error"
