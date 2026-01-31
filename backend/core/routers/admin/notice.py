from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from backend.core.o2auth import get_current_user
from ...import database,models,schemas
router=APIRouter()
# will be available soon
@router.post('/notice')
def post_notice(n_data:schemas.Post_notice,admin=Depends(get_current_user),db:Session=Depends(database.get_db)):
    n=models.Notices(**n_data.dict())
    db.add(n) 
    db.commit()
    return {"status":True,"message":"Notice posted Successfully"}
