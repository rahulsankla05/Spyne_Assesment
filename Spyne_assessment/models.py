from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

# Association table for Many-to-Many relationship between Discussion and Hashtag
discussion_hashtag = Table(
    'discussion_hashtag',
    Base.metadata,
    Column('discussion_id', Integer, ForeignKey('discussions.id')),
    Column('hashtag_id', Integer, ForeignKey('hashtags.id'))
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    mobile = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    discussions = relationship("Discussion", back_populates="owner")
    following = relationship(
        "User",
        secondary="followers",
        primaryjoin=id == followers.c.follower_id,
        secondaryjoin=id == followers.c.followed_id
    )

class Discussion(Base):
    __tablename__ = 'discussions'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    image = Column(String, nullable=True)
    created_on = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User", back_populates="discussions")
    hashtags = relationship(
        "Hashtag",
        secondary=discussion_hashtag,
        back_populates="discussions"
    )
    comments = relationship("Comment", back_populates="discussion")
    likes = relationship("DiscussionLike", back_populates="discussion")

class Hashtag(Base):
    __tablename__ = 'hashtags'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    discussions = relationship(
        "Discussion",
        secondary=discussion_hashtag,
        back_populates="hashtags"
    )

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    created_on = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
    discussion_id = Column(Integer, ForeignKey('discussions.id'))

    user = relationship("User")
    discussion = relationship("Discussion", back_populates="comments")
    likes = relationship("CommentLike", back_populates="comment")

class DiscussionLike(Base):
    __tablename__ = 'discussion_likes'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    discussion_id = Column(Integer, ForeignKey('discussions.id'))

    user = relationship("User")
    discussion = relationship("Discussion", back_populates="likes")

class CommentLike(Base):
    __tablename__ = 'comment_likes'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    comment_id = Column(Integer, ForeignKey('comments.id'))

    user = relationship("User")
    comment = relationship("Comment", back_populates="likes")

# Association table for User follow relationships
followers = Table(
    'followers',
    Base.metadata,
    Column('follower_id', Integer, ForeignKey('users.id')),
    Column('followed_id', Integer, ForeignKey('users.id'))
)
