# Mini Bank System

A complete banking application with both CLI and web-based dashboard interfaces for managing accounts, deposits, withdrawals, and transaction history.

## Features

✨ **Account Management**
- Create new bank accounts (Savings or Current account type)
- Unique account ID generation (MB + 6 digits)
- Account holder name registration
- Account type selection

💳 **Banking Operations**
- Deposit money to your account
- Withdraw money (with balance validation)
- Real-time balance updates
- Transaction history with timestamps

📊 **Dashboard**
- Professional HTML/CSS web interface
- Account summary display
- Live balance and account type display
- Complete transaction history
- Back and Exit buttons for navigation

💾 **Data Persistence**
- Browser localStorage for client-side data storage
- Automatic account data saving
- Session persistence between page refreshes

## Project Files

| File | Description |
|------|-------------|
| `bank.html` | Web-based Mini Bank dashboard interface |
| `bank.css` | Professional styling for the dashboard |
| `mini bank2.py` | Command-line banking interface |
| `bank_core.py` | Core banking logic and account model |
| `bank_server.py` | Optional HTTP server for backend support |

## How to Use

### Web Interface

1. Open `bank.html` in your web browser
2. Enter your full name in the "Account holder name" field
3. Select account type (Savings or Current) from the dropdown
4. Click "Create New Account" to open your account
5. Use the "Bank actions" section to:
   - **Deposit**: Enter amount and click "Deposit"
   - **Withdraw**: Enter amount and click "Withdraw"
6. View your transaction history in real-time
7. Click "Create Another Account" to manage multiple accounts
8. Click "Exit Bank" to return to login screen

### CLI Interface

Run the Python CLI application:

```bash
python "mini bank2.py"
```

Follow the on-screen menu to:
- Create new accounts
- Deposit and withdraw funds
- View account summaries
- Check transaction history

## Account Type Details

- **Savings Account**: For regular savings and deposits
- **Current Account**: For frequent transactions

## Technical Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python (optional server support)
- **Storage**: Browser LocalStorage
- **Currency**: Indian Rupees (₹)

## Data Structure

Each account stores:
```json
{
  "id": "MB123456",
  "name": "Account Holder Name",
  "type": "Savings",
  "balance": 0,
  "history": [
    {
      "type": "Account opened",
      "amount": "₹0.00",
      "date": "timestamp"
    }
  ]
}
```

## Browser Compatibility

- Chrome/Edge (Recommended)
- Firefox
- Safari
- Any modern browser with JavaScript enabled

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/shrishant1974-beep/Mini-bank-system.git
```

2. Open `bank.html` directly in your browser (no server needed for web interface)

3. Or run the CLI:
```bash
python "mini bank2.py"
```

## Features Highlight

✅ **Zero External Dependencies** - Works with vanilla JavaScript
✅ **Instant Persistence** - Data saved automatically to browser
✅ **Professional UI** - Modern card-based design with smooth interactions
✅ **Complete Banking Flow** - Create account → Deposit → Withdraw → View History
✅ **Multiple Account Support** - Manage different account types
✅ **Real-time Updates** - Balance and history update instantly

## Notes

- Account data is stored in your browser's LocalStorage
- Data persists between sessions
- Starting fresh will reset all account information
- Each account gets a unique ID in format: `MB######`

## Author

Shrishant B Gupta

## License

Open source - feel free to use and modify
