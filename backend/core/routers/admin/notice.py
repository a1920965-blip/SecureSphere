from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from backend.core.oauth2 import verify_admin
from ...import database,models,schemas
router=APIRouter()
# will be available soon
@router.post('/notice')
def post_notice(n_data:schemas.Post_notice,admin=Depends(verify_admin),db:Session=Depends(database.get_db)):
    n=models.Notices(**n_data.dict())
    db.add(n) 
    db.commit()
    return {"success":True,"message":"Notice posted Successfully"}
@router.get('/notice')
def get_notice(db:Session=Depends(database.get_db),admin=Depends(verify_admin)):
    notices=db.query(models.Notices).all()
    return{"status":True,"data":notices}