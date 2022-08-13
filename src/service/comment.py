from src.database import db
from src.model.models import Comment, User

def get_comment(company_id):
    '''리뷰 읽기'''

    reviews = (db.session.query(Comment)
               .join(User, Comment.commenter_id == User.id)
               .filter(Comment.company_id == company_id)
               .values(User.nickname,
                       Comment.content))

    resultlist = []
    for r_nick, r_content in reviews:
        resultlist.append({'nickname': r_nick,
                           'content': r_content})
    return resultlist


def post_comment(company_id, input):
    '''리뷰 올리기'''
    u_id = User.query.filter(User.nickname == input['nickname']).first()

    add_review = Comment(
        commenter_id = u_id.id,
        content = input['content'],
        company_id = company_id
    )
    db.session.add(add_review)
    db.session.commit()


def delete_comment(company_id, commenter_id):
    '''리뷰 삭제하기'''
    del_comment = Comment.query.filter((Comment.company_id == company_id) & (Comment.commenter_id==commenter_id)).first()
    db.session.delete(del_comment)
    db.session.commit()