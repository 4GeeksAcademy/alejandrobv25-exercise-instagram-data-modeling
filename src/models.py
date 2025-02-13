import os
import sys
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import backref
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(index=True, nullable=False)
    address1: Mapped[str]
    firstname: Mapped[str]
    lastname: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    comments: Mapped[list['Comment']] = relationship('Comment', backref='user')

    posts: Mapped[list['Post']] = relationship('Post', backref='user')

    followers: Mapped[list['Follower']] = relationship('Follower', foreign_keys='Follower.user_from_ID', backref='user_from')
    following: Mapped[list['Follower']] = relationship('Follower', foreign_keys='Follower.user_to_ID', backref='user_to')

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "address1": self.address1,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email
        }


class Comment(Base):
    __tablename__ = 'comment'
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    post_id: Mapped[int]

    user: Mapped['User'] = relationship('User', backref='comments')

    post: Mapped['Post'] = relationship('Post', backref='comments')

    def to_dict(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "user_id": self.user_id,
            "post_id": self.post_id
        }


class Post(Base):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    
    user: Mapped['User'] = relationship('User', backref='posts')

    comments: Mapped[list['Comment']] = relationship('Comment', backref='post')

    media: Mapped[list['Media']] = relationship('Media', backref='post')

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id
        }


class Media(Base):
    __tablename__ = 'media'
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str]  
    url: Mapped[str]
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))

    post: Mapped['Post'] = relationship('Post', backref='media')

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "post_id": self.post_id
        }


class Follower(Base):
    __tablename__ = 'follower'
    user_from_ID: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)
    user_to_ID: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)

    user_from: Mapped['User'] = relationship('User', foreign_keys=[user_from_ID], backref='followers')

    user_to: Mapped['User'] = relationship('User', foreign_keys=[user_to_ID], backref='following')

    def to_dict(self):
        return {
            "user_from_ID": self.user_from_ID,
            "user_to_ID": self.user_to_ID
        }

# Generar el diagrama a partir de la base de datos
try:
    result = render_er(Base, 'diagram.png')
    print("¡Éxito! Revisa el archivo diagram.png")
except Exception as e:
    print("Hubo un problema generando el diagrama")
    raise e
