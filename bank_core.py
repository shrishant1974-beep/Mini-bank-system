import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

DATA_FILE = Path(__file__).with_name('bank_data.json')


def format_id(index: int) -> str:
    return f"BK{index:06d}"


class BankError(Exception):
    pass


class Account:
    def __init__(self, account_id: str, name: str, balance: float = 0.0, history: List[dict] = None, created: str = None):
        self.account_id = account_id
        self.name = name
        self.balance = float(balance)
        self.created = created or datetime.utcnow().isoformat()
        self.history = history or []

    def deposit(self, amount: float):
        if amount <= 0:
            raise BankError('Deposit amount must be greater than zero.')
        self.balance += amount
        self.record('Deposit', amount)

    def withdraw(self, amount: float):
        if amount <= 0:
            raise BankError('Withdrawal amount must be greater than zero.')
        if amount > self.balance:
            raise BankError('Insufficient funds.')
        self.balance -= amount
        self.record('Withdrawal', amount)

    def record(self, transaction_type: str, amount: float, other: str = None):
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'type': transaction_type,
            'amount': round(amount, 2),
            'balance': round(self.balance, 2),
            'details': other or ''
        }
        self.history.append(entry)

    def to_dict(self):
        return {
            'account_id': self.account_id,
            'name': self.name,
            'balance': round(self.balance, 2),
            'created': self.created,
            'history': self.history,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            account_id=data['account_id'],
            name=data['name'],
            balance=data.get('balance', 0.0),
            history=data.get('history', []),
            created=data.get('created')
        )


class Bank:
    def __init__(self, data_file: Path = DATA_FILE):
        self.data_file = data_file
        self.accounts: Dict[str, Account] = {}
        self.load()

    def load(self):
        if self.data_file.exists():
            try:
                with self.data_file.open('r', encoding='utf-8') as f:
                    payload = json.load(f)
                    self.accounts = {item['account_id']: Account.from_dict(item) for item in payload}
            except (json.JSONDecodeError, IOError):
                self.accounts = {}
        else:
            self.accounts = {}

    def save(self):
        self.data_file.write_text(json.dumps([account.to_dict() for account in self.accounts.values()], indent=2), encoding='utf-8')

    def next_account_id(self) -> str:
        next_index = len(self.accounts) + 1
        while format_id(next_index) in self.accounts:
            next_index += 1
        return format_id(next_index)

    def create_account(self, name: str) -> Account:
        name = name.strip()
        if not name:
            raise BankError('Account name cannot be empty.')
        account_id = self.next_account_id()
        account = Account(account_id=account_id, name=name)
        account.record('Account opened', 0.0)
        self.accounts[account_id] = account
        self.save()
        return account

    def get_account(self, account_id: str) -> Account:
        if account_id not in self.accounts:
            raise BankError(f'Account {account_id} not found.')
        return self.accounts[account_id]

    def deposit(self, account_id: str, amount: float) -> Account:
        account = self.get_account(account_id)
        account.deposit(amount)
        self.save()
        return account

    def withdraw(self, account_id: str, amount: float) -> Account:
        account = self.get_account(account_id)
        account.withdraw(amount)
        self.save()
        return account

    def transfer(self, source_id: str, target_id: str, amount: float):
        if source_id == target_id:
            raise BankError('Source and destination accounts must be different.')
        source = self.get_account(source_id)
        target = self.get_account(target_id)
        if amount <= 0:
            raise BankError('Transfer amount must be greater than zero.')
        source.withdraw(amount)
        target.deposit(amount)
        source.record('Transfer sent', -amount, f'To {target.account_id}')
        target.record('Transfer received', amount, f'From {source.account_id}')
        self.save()

    def list_accounts(self):
        return [account.to_dict() for account in sorted(self.accounts.values(), key=lambda x: x.account_id)]

    def summary(self):
        return {
            'total_accounts': len(self.accounts),
            'total_deposits': round(sum(a.balance for a in self.accounts.values()), 2),
        }
