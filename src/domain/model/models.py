from enum import Enum
from datetime import datetime

from sqlalchemy import (
    String,
    Integer,
    ForeignKey,
    DateTime,
    Enum as SqlEnum,
    func
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from src.infra.connection_db import Base

### Enum Type ###
class WorkType(Enum):
    INBOUND = "Inbound"
    OUTBOUND = "Outbound"
    TRANSFER = "Transfer" 
###++++++++++++++++++++++++++++++###

### Hub ###
class Hub(Base):
    __tablename__ = "hubs"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(2), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    yards: Mapped[list["Yard"]] = relationship(back_populates="hub", cascade="all, delete-orphan")
    warehouses: Mapped[list["Warehouse"]] = relationship(back_populates="hub", cascade="all, delete-orphan")
###++++++++++++++++++++++++++++++###

### Yard ###
class Yard(Base):
    __tablename__ = "yards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    hub_id: Mapped[int] = mapped_column(ForeignKey("hubs.id"), nullable=False, index=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    hub: Mapped["Hub"] = relationship(back_populates="yards")
###++++++++++++++++++++++++++++++###

### Warehouse ###
class Warehouse(Base):
    __tablename__ = "warehouses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    hub_id: Mapped[int] = mapped_column(ForeignKey("hubs.id"), nullable=False, index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    hub: Mapped["Hub"] = relationship(back_populates="warehouses")
    products: Mapped[list["Product"]] = relationship(back_populates="warehouse", cascade="all, delete-orphan")
###++++++++++++++++++++++++++++++###

### Product ###
class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sku: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"), nullable=False, index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    warehouse: Mapped["Warehouse"] = relationship(back_populates="products")
    movements: Mapped[list["Movement"]] = relationship(back_populates="product")
###++++++++++++++++++++++++++++++###

### Movement ###
class Movement(Base):
    __tablename__ = "movements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False, index=True)
    type: Mapped[WorkType] = mapped_column(SqlEnum(WorkType), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    
    source_type: Mapped[str | None] = mapped_column(String(30), nullable=True)
    source_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    destination_type: Mapped[str | None] = mapped_column(String(30), nullable=True)
    destination_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    
    movement_date: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), index=True)

    product: Mapped["Product"] = relationship(back_populates="movements")