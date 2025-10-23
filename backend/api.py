from pydantic import BaseModel
from fastapi import FastAPI
from backend.routers import js, jc

app = FastAPI(title="Jira Integration")

# includi i router con prefissi e, facoltativamente, tag
app.include_router(jc.router, prefix="/jc", tags=["Jira Cloud"])
app.include_router(js.router, prefix="/js", tags=["Jira Server"])

#class Item(BaseModel):
#    name: str
#    value: float

#class CopyIssue(BaseModel):
#    code: str
#    xapikey: str

#@app.get("/ping")
#def ping():
#    return {"message": "pong"}

#@app.post("/process")
#def process_item(item: Item):
#    result = {"name": item.name, "processed_value": item.value * 2}
#    return result

#@app.post("/copyIssue")
#def copyIssue(item: CopyIssue):
#    if item.xapikey == "gg":
#        result = "ok"
#        return result
#    return "error"

