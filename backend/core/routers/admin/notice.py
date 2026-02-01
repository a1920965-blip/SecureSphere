from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from backend.core.o2auth import verify_admin
from ...import database,models,schemas
router=APIRouter()
# will be available soon
@router.post('/notice')
def post_notice(n_data:schemas.Post_notice,admin=Depends(verify_admin),db:Session=Depends(database.get_db)):
    n=models.Notices(**n_data.dict())
    db.add(n) 
    db.commit()
    return {"success":True,"message":"Notice posted Successfully"}
