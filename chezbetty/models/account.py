from .model import *
from .transaction import Transaction

class Account(Base):
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True, nullable=False)
    type = Column(Enum("user", "placeholder"), nullable=False)
    balance = Column(Float, nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)

    __mapper_args__ = {'polymorphic_on':type}
    
    def __init__(self, name, balance=0.0):
        self.name = name
        self.balance = balance

    @property
    def transactions(self):
        return object_session(self).query(Transaction)\
                .Filter(or_(
                        Transaction.to_account_id == self.id,
                        Transaction.from_account_id == self.id)).all()

class PlaceholderAccount(Account):
    __mapper_args__ = {'polymorphic_identity': 'placeholder'}


def make_account(name):
    t = DBSession.query(PlaceholderAccount).filter(PlaceholderAccount.name == name).first()
    if t:
        return t
    t = PlaceholderAccount(name)
    DBSession.add(t)
    return t