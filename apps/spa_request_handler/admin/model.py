# coding=utf8

from sqlalchemy import (
    Column, DateTime, ForeignKey, Index,
    Integer, String, Text, Boolean, text,
    distinct, exists, and_, or_, desc
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


############################################
# USER


class User(Base):
    __tablename__ = 'user'

    id = Column(
        Integer,
        primary_key=True
    )
    username = Column(
        String(255),
        nullable=False
    )
    password = Column(
        String(255),
        nullable=False
    )
    email = Column(
        String(255)
    )
    firstname = Column(
        String(255)
    )
    lastname = Column(
        String(255)
    )
    created_at = Column(
        DateTime
    )
    last_login_at = Column(
        DateTime,
        nullable=False
    )
    types = relationship("CatalogUserType", secondary="users_types")

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return "%s" % self.username


class CatalogUserType(Base):
    __tablename__ = 'catalog_user_type'

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    name = Column(
        String(255)
    )
    users = relationship("User", secondary="users_types")

    def __repr__(self):
        return "%s" % self.name


class UsersType(Base):
    __tablename__ = 'users_types'
    __table_args__ = (
        Index('idx_users_types_id', 'user_id', 'type_id'),
    )

    id = Column(
        Integer,
        primary_key=True
    )
    user_id = Column(
        ForeignKey('user.id', onupdate='CASCADE')
    )
    type_id = Column(
        ForeignKey('catalog_user_type.id', onupdate='CASCADE')
    )


############################################
# PRODUCT


class Product(Base):
    __tablename__ = 'product'

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    product_type_id = Column(
        Integer,
        ForeignKey('product_type.id', onupdate='CASCADE', use_alter=True, name='product_product_type_id_fkey')
    )
    name = Column(
        String(255),
        nullable=False,
    )
    description = Column(
        Text,
        nullable=False,
    )
    slug_name = Column(
        String(255),
        # nullable=False,
        unique=True,
        index=True
    )
    product_type = relationship('ProductType', foreign_keys=product_type_id, post_update=True)

    photos = relationship("ProductPhoto", secondary="products_product_photos")

    def __repr__(self):
        return "%s" % self.name


class ProductType(Base):
    __tablename__ = 'product_type'

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    name = Column(
        String,
        nullable=False,
        index=True
    )
    description = Column(
        Text,
        nullable=False
    )

    # product = relationship(Product, backref='Type')

    def __repr__(self):
        return "%s" % self.name


class ProductTypeAttributeValue(Base):
    __tablename__ = 'product_type_attribute_value'
    __table_args__ = (
        Index('idx_product_type_attribute_value_id', 'product_type_id', 'attribute_value_id'),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    product_type_id = Column(
        ForeignKey('product_type.id', onupdate='CASCADE')
    )
    attribute_value_id = Column(
        ForeignKey('attribute_value.id', onupdate='CASCADE')
    )


class AttributeValue(Base):
    __tablename__ = 'attribute_value'

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    attribute_id = Column(
        ForeignKey('attribute.id', onupdate='CASCADE')
    )
    name = Column(
        String,
        nullable=False,
        index=True
    )
    description = Column(
        Text,
        nullable=False
    )

    def __repr__(self):
        return "%s" % self.name


class Attribute(Base):
    __tablename__ = 'attribute'

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    name = Column(
        String,
        nullable=False,
        index=True
    )
    description = Column(
        Text,
        nullable=False
    )
    type = Column(
        String,
        nullable=False
    )
    is_active = Column(
        Boolean,
        unique=False,
        default=True
    )

    def __repr__(self):
        return "%s" % self.name


class ProductAttributeValues(Base):
    __tablename__ = 'product_attribute_values'
    __table_args__ = (
        Index('idx_product_attribute_values_id', 'product_id', 'attribute_value_id'),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    product_id = Column(
        ForeignKey('product.id', onupdate='CASCADE')
    )
    attribute_value_id = Column(
        ForeignKey('attribute_value.id', onupdate='CASCADE')
    )


class ProductPhoto(Base):
    __tablename__ = 'product_photo'

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    name = Column(
        String(255),
        nullable=False
    )
    path = Column(
        String(255),
        nullable=False
    )
    thumb_name = Column(
        String(255),
        nullable=False
    )
    thumb_path = Column(
        String(255),
        nullable=False
    )

    def __repr__(self):
        return "%s" % self.name


class ProductsProductPhoto(Base):
    __tablename__ = 'products_product_photos'
    __table_args__ = (
        Index('idx_products_product_photos_id', 'product_id', 'product_photo_id'),
    )

    id = Column(
        Integer,
        primary_key=True
    )
    product_id = Column(
        ForeignKey('product.id', onupdate='CASCADE')
    )
    product_photo_id = Column(
        ForeignKey('product_photo.id', onupdate='CASCADE')
    )

    product = relationship('Product')
    product_photo = relationship('ProductPhoto')
