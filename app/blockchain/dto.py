from datetime import datetime

from pydantic import BaseModel, Field


class TransactionDTO(BaseModel):
    tx_hash: str = Field(alias="txHash")
    from_address: str = Field(alias="from")
    to_address: str = Field(alias="to")
    value: str = Field(alias="value")
    gas_price: str = Field(alias="gasPrice")
    gas_used: int = Field(alias="gasUsed")
    block_number: int = Field(alias="blockNumber")
    timestamp: datetime = Field(alias="timeStamp")

    class Config:
        populate_by_name = True


class BlockDTO(BaseModel):
    block_number: int = Field(alias="number")
    block_hash: str = Field(alias="hash")
    parent_hash: str = Field(alias="parentHash")
    timestamp: datetime
    transactions: list[TransactionDTO] = Field(default_factory=list)
    gas_used: int = Field(alias="gasUsed")
    gas_limit: int = Field(alias="gasLimit")

    class Config:
        populate_by_name = True


class TokenBalanceDTO(BaseModel):
    token_address: str = Field(alias="tokenAddress")
    symbol: str
    balance: str
    decimals: int

    class Config:
        populate_by_name = True
