from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Depends, status, UploadFile, File
from routers.schemas import PostBase, PostDisplay, UserAuth
from db.db_post import new_post, get_posts, delete_post
from sqlalchemy.orm.session import Session
from db.database import get_db
from typing import List
import random
import string
import shutil
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix='/post',
    tags=['post']
)

image_url_types = ['absolute', 'relative']

@router.post('', response_model=PostDisplay)
def create_post(request: PostBase, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    if not request.image_url_type in image_url_types:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail="Parameter image_url_type can only take values 'absolute' or 'relative'")
    return new_post(db, request)

@router.get('/all', response_model=List[PostDisplay])
def all_posts(db: Session = Depends(get_db)):
    return get_posts(db)

@router.post('/image')
def upload_image(image: UploadFile = File(...), current_user: UserAuth = Depends(get_current_user)):
    letters = string.ascii_letters
    random_str = ''.join(random.choice(letters) for i in range(6))
    new = f'_{random_str}.'
    filename = new.join(image.filename.rsplit('.', 1))
    path = f'images/{filename}'

    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    return {'filename': path}

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def remove_post(id: int, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    return delete_post(db, id, current_user.id)