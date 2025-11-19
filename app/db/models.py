from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AssetMaster(Base):
    __tablename__ = "asset_master"
    
    asset_id = Column(Integer, primary_key=True, index=True)
    ticker_symbol = Column(String, nullable=False, unique=True) # e.g., RELIANCE
    asset_type = Column(String, nullable=False) # 'EQUITY' or 'BOND'
    sector = Column(String)
    sebi_regulated = Column(Boolean, default=True)
    
    # Relationships
    equity_data = relationship("EquityFundamentals", back_populates="asset", uselist=False)
    bond_data = relationship("FixedIncomeDetails", back_populates="asset", uselist=False)

class EquityFundamentals(Base):
    __tablename__ = "equity_fundamentals"
    
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("asset_master.asset_id"))
    
    roe = Column(Float)            # Return on Equity
    debt_to_equity = Column(Float) # Debt Ratio
    cagr_5yr = Column(Float)       # Growth
    graham_num = Column(Float)     # Valuation check
    
    asset = relationship("AssetMaster", back_populates="equity_data")

class FixedIncomeDetails(Base):
    __tablename__ = "fixed_income_details"
    
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("asset_master.asset_id"))
    
    coupon_rate = Column(Float)    # The Yield (e.g., 12.5)
    security_type = Column(String) # 'Secured' vs 'Unsecured'
    credit_rating = Column(String) # e.g., 'CRISIL AA'
    
    asset = relationship("AssetMaster", back_populates="bond_data")