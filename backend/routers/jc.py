import os
from dotenv import load_dotenv
from fastapi import APIRouter, Header, Depends, HTTPException, UploadFile, File
#from pydantic import BaseModel
from backend.jiraUtils import create_issue, get_issue, create_comment, create_attachment
from backend.requestDto import CreateIssueRequest, CreateCommentRequest

load_dotenv()
API_KEY = os.getenv("MY_API_KEY")

router = APIRouter()

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="X-API-Key non valido")
    
#class User(BaseModel):
#    id: int
#    name: str

# endpoint relativi agli utenti
#@router.get("/", response_model=list[User])
#async def list_users():
#    return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

@router.get("/issue/{issueKey}", summary="Recupera la issue con chiave {issueKey}")
def get_jc_issue(issueKey: str):
    
    try:

        print(f"Get issue {issueKey} from Jira Cloud...")
        return get_issue("Cloud", issueKey)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/issue", summary="Crea una nuova issue")
def create_jc_issue(item: CreateIssueRequest, _: None = Depends(verify_api_key)):
    
    try:
        
        print(f"Create issue in Jira Cloud...")
        return create_issue("Cloud", item)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/issue/{issueKey}/comment", summary="Crea un nuovo commento nella issue con chiave {issueKey}")
def create_jc_issue_comment(issueKey: str, item: CreateCommentRequest, _: None = Depends(verify_api_key)):

    try:

        print(f"Create issue comment in Jira Cloud...")
        return create_comment("Cloud", issueKey, item)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/issue/{issueKey}/attachment", summary="Crea un nuovo allegato alla issue con chiave {issueKey}")
def create_jc_issue_attachment(issueKey: str, file: UploadFile = File(...), _: None = Depends(verify_api_key)):

    try:
        
        print(f"Create issue attachment in Jira Cloud...")
        return create_attachment("Cloud", issueKey, file)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))