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

	type = relationship('CatalogUserType')
	user = relationship('User')


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
	price = Column(
		Integer,
		nullable=False,
		index=True,
		server_default=text("0")
	)


class ProductAttribute(Base):
	__tablename__ = 'product_attribute'

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


class ProductFabric(Base):
	__tablename__ = 'product_fabric'

	id = Column(
		Integer,
		primary_key=True,
		index=True,
		server_default=text("nextval('product_fabric_id_seq'::regclass)")
	)
	name = Column(
		String,
		nullable=False,
		index=True
	)


class ProductManufacturer(Base):
	__tablename__ = 'product_manufacturer'

	id = Column(
		Integer,
		primary_key=True,
		index=True,
		server_default=text("nextval('product_manufacturer_id_seq'::regclass)")
	)
	name = Column(
		String(255),
		nullable=False,
		index=True
	)


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
	tumbl_name = Column(
		String(255),
		nullable=False
	)
	tumbl_path = Column(
		String(255),
		nullable=False
	)


class ProductsProductAttribute(Base):
	__tablename__ = 'products_product_attributes'
	__table_args__ = (
		Index('idx_products_product_attributes_id', 'product_id', 'product_attribute_id'),
	)

	id = Column(
		Integer,
		primary_key=True,
		server_default=text("nextval('products_product_attributes_id_seq'::regclass)")
	)
	product_id = Column(
		ForeignKey('product.id', onupdate='CASCADE')
	)
	product_attribute_id = Column(
		ForeignKey('product_attribute.id', onupdate='CASCADE')
	)

	product_attribute = relationship('ProductAttribute')
	product = relationship('Product')


class ProductsProductFabric(Base):
	__tablename__ = 'products_product_fabrics'
	__table_args__ = (
		Index('idx_products_product_fabrics_id', 'product_id', 'product_fabric_id'),
	)

	id = Column(
		Integer,
		primary_key=True,
		server_default=text("nextval('products_product_fabrics_id_seq'::regclass)")
	)
	product_id = Column(
		ForeignKey('product.id', onupdate='CASCADE')
	)
	product_fabric_id = Column(
		ForeignKey('product_fabric.id', onupdate='CASCADE')
	)

	product_fabric = relationship('ProductFabric')
	product = relationship('Product')


class ProductsProductManufacturer(Base):
	__tablename__ = 'products_product_manufacturers'
	__table_args__ = (
		Index('idx_products_product_manufacturers_id', 'product_id', 'product_manufacturer_id'),
	)

	id = Column(
		Integer,
		primary_key=True,
		server_default=text("nextval('products_product_manufacturers_id_seq'::regclass)")
	)
	product_id = Column(
		ForeignKey('product.id', onupdate='CASCADE')
	)
	product_manufacturer_id = Column(
		ForeignKey('product_manufacturer.id', onupdate='CASCADE')
	)

	product = relationship('Product')
	product_manufacturer = relationship('ProductManufacturer')


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
