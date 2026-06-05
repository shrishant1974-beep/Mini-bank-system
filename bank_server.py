import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from bank_core import Bank, BankError

PORT = 8000
BASE_DIR = Path(__file__).resolve().parent


class BankHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == '/':
            self.send_response(302)
            self.send_header('Location', '/bank.html')
            self.end_headers()
            return

        if path == '/api/accounts':
            self.handle_accounts()
            return

        if path == '/api/account':
            self.handle_account(query)
            return

        if path == '/api/summary':
            self.handle_summary()
            return

        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == '/api/create':
            self.handle_create()
            return

        if path == '/api/deposit':
            self.handle_deposit()
            return

        if path == '/api/withdraw':
            self.handle_withdraw()
            return

        if path == '/api/transfer':
            self.handle_transfer()
            return

        self.send_error(404, 'Endpoint not found')

    def handle_accounts(self):
        accounts = self.server.bank.list_accounts()
        self.respond_json({'accounts': accounts})

    def handle_account(self, query):
        account_id = query.get('id', [None])[0]
        if not account_id:
            self.respond_json({'error': 'Missing account id'}, 400)
            return

        try:
            account = self.server.bank.get_account(account_id).to_dict()
            self.respond_json({'account': account})
        except BankError as exc:
            self.respond_json({'error': str(exc)}, 404)

    def handle_summary(self):
        self.respond_json({'summary': self.server.bank.summary()})

    def handle_create(self):
        data = self.read_json() or {}
        name = data.get('name', '').strip()
        try:
            account = self.server.bank.create_account(name)
            self.respond_json({'account': account.to_dict()})
        except BankError as exc:
            self.respond_json({'error': str(exc)}, 400)

    def handle_deposit(self):
        data = self.read_json() or {}
        try:
            account_id = data.get('account_id')
            amount = float(data.get('amount', 0))
            account = self.server.bank.deposit(account_id, amount)
            self.respond_json({'account': account.to_dict()})
        except (TypeError, ValueError):
            self.respond_json({'error': 'Invalid amount.'}, 400)
        except BankError as exc:
            self.respond_json({'error': str(exc)}, 400)

    def handle_withdraw(self):
        data = self.read_json() or {}
        try:
            account_id = data.get('account_id')
            amount = float(data.get('amount', 0))
            account = self.server.bank.withdraw(account_id, amount)
            self.respond_json({'account': account.to_dict()})
        except (TypeError, ValueError):
            self.respond_json({'error': 'Invalid amount.'}, 400)
        except BankError as exc:
            self.respond_json({'error': str(exc)}, 400)

    def handle_transfer(self):
        data = self.read_json() or {}
        try:
            source_id = data.get('source_id')
            target_id = data.get('target_id')
            amount = float(data.get('amount', 0))
            self.server.bank.transfer(source_id, target_id, amount)
            self.respond_json({'accounts': self.server.bank.list_accounts()})
        except (TypeError, ValueError):
            self.respond_json({'error': 'Invalid amount.'}, 400)
        except BankError as exc:
            self.respond_json({'error': str(exc)}, 400)

    def read_json(self):
        length = int(self.headers.get('Content-Length', 0))
        if length == 0:
            return None
        payload = self.rfile.read(length).decode('utf-8')
        try:
            return json.loads(payload)
        except json.JSONDecodeError:
            return None

    def respond_json(self, body, status=200):
        payload = json.dumps(body).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


class BankHTTPServer(HTTPServer):
    def __init__(self, server_address, RequestHandlerClass):
        super().__init__(server_address, RequestHandlerClass)
        self.bank = Bank()


if __name__ == '__main__':
    address = ('', PORT)
    server = BankHTTPServer(address, BankHTTPRequestHandler)
    print(f'Bank server ready at http://localhost:{PORT}/bank.html')
    print('Use Ctrl+C to stop the server.')
    server.serve_forever()
