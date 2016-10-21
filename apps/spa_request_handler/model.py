# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, Text, text
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
        primary_key=True,
        server_default=text("nextval('user_id_seq'::regclass)")
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
        DateTime,
        nullable=False
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
        index=True,
        server_default=text("nextval('catalog_user_type_id_seq'::regclass)")
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
        primary_key=True,
        server_default=text("nextval('users_types_id_seq'::regclass)")
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
        index=True,
        server_default=text("nextval('product_id_seq'::regclass)")
    )
    name = Column(
        String(255),
        nullable=False,
        index=True
    )
    slug_name = Column(
        String(255),
        nullable=False,
        unique=True
    )
    description = Column(
        Text,
        nullable=False,
        index=True
    )
    attributes = relationship("CatalogProductAttribute", secondary="products_product_attributes")
    photos = relationship("ProductPhoto", secondary="products_product_photos")


class CatalogProductAttribute(Base):
    __tablename__ = 'catalog_product_attribute'

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        server_default=text("nextval('product_attribute_id_seq'::regclass)")
    )
    name = Column(
        String,
        nullable=False,
        index=True
    )

    def __repr__(self):
        return "%s" % self.name


class ProductPhoto(Base):
    __tablename__ = 'product_photo'

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        server_default=text("nextval('product_photo_id_seq'::regclass)")
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


class ProductsProductAttribute(Base):
    __tablename__ = 'products_product_attributes'
    __table_args__ = (
        Index('idx_products_product_attributes_id', 'product_id', 'catalog_product_attribute_id'),
    )

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('products_catalog_product_attribute_id_seq'::regclass)")
    )
    product_id = Column(
        ForeignKey('product.id', onupdate='CASCADE')
    )
    catalog_product_attribute_id = Column(
        ForeignKey('catalog_product_attribute.id', onupdate='CASCADE')
    )
    attribute_value = Column(
        String(255),
        nullable=False
    )

    catalog_product_attribute = relationship('CatalogProductAttribute')
    product = relationship('Product')


class ProductsProductPhoto(Base):
    __tablename__ = 'products_product_photos'
    __table_args__ = (
        Index('idx_products_product_photos_id', 'product_id', 'product_photo_id'),
    )

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('products_product_photos_id_seq'::regclass)")
    )
    product_id = Column(
        ForeignKey('product.id', onupdate='CASCADE')
    )
    product_photo_id = Column(
        ForeignKey('product_photo.id', onupdate='CASCADE')
    )

    product = relationship('Product')
    product_photo = relationship('ProductPhoto')
