from sqlalchemy.orm import Session
from db.models import Comment
from routers.schemas import CommentBase
from datetime import datetime

def create(db: Session , request: CommentBase):
    new_comment = Comment(
        user_comment = request.user_comment,
        username = request.username,
        post_id = request.post_id,
        timestamp = datetime.now(),
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

def get_all(db: Session, post_id: int):
    all_comments = db.query(Comment).filter(Comment.post_id == post_id)
    return all_comments