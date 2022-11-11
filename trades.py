import tokens
from flask import request, Request
from database import db
from models import User, Trade


def get_trade_by_id(id: int) -> dict:
    trade = db.session.query(Trade).get(id)
    if trade is not None:
        return trade.json()
    else:
        return f'Trade id {id} not found.', 404

def get_trades_by_user(username: str) -> list[dict]:
    user_id = get_user_id(username) 
    query = db.select(Trade).filter_by(user_id=user_id)
    trades = db.session.execute(query).scalars().all()

    return [t.json() for t in trades]

def get_portfolio(username: str) -> list[dict]:
    pass

def get_user_id(username: str) -> int:
    query = db.select(User).filter_by(username=username)
    user = db.session.execute(query).scalar_one()
    return user.id

def trade() -> list[dict]:
    if not token_is_valid(request):
        return 'Invalid or expired token.', 401

    new_trade = create_trade(request)
    cash_trade = create_cash_transaction(new_trade)

    db.session.add(new_trade)
    db.session.add(cash_trade)
    db.session.commit()

    return [new_trade.json(), cash_trade.json()], 201

def token_is_valid(request: Request) -> bool:
    token = get_token(request)
    return tokens.is_valid(token) and not tokens.is_expired(token)

def get_token(request: Request) -> str:
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(' ')[1]
    return token

def create_trade(request: Request) -> Trade:
    trade_obj = request.json
    user_id = get_user_id(trade_obj['username'])
    new_trade = Trade(
        user_id = user_id,
        symbol = trade_obj['symbol'],
        shares = trade_obj['shares'],
        price = trade_obj['price']
    )
    return new_trade

def create_cash_transaction(trade: Trade) -> Trade:
    cash_trade = Trade(
        user_id = trade.user_id,
        symbol = '$CASH',
        shares = -(trade.shares * trade.price),
        price = 1
    )
    return cash_trade