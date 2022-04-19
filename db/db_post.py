from datetime import datetime
from routers.schemas import PostBase
from sqlalchemy.orm.session import Session
from db.models import Post
import datetime
from fastapi import HTTPException, status, Response

def new_post(db:Session, request: PostBase):
    post = Post(
        image_url = request.image_url,
        image_url_type = request.image_url_type,
        caption = request.caption,
        timestamp = datetime.datetime.now(),
        user_id = request.creator_id,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def get_posts(db:Session):
    return db.query(Post).all()


def delete_post(db: Session, id: int, user_id: int):
    deleted_post = db.query(Post).filter(Post.id == id).first()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail='Post does not exist')

    if deleted_post.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
            detail='Action not authorized.')

    
    db.delete(deleted_post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
