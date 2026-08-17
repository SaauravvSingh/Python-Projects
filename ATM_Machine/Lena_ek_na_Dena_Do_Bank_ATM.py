import streamlit as st
from datetime import datetime
import time

st.set_page_config(
    page_title="Lena ek na Dena Do Bank • ATM",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
#                 LENA EK NA DENA DO BANK
#                    STREAMLIT ATM APP
# =========================================================

# -------------------- BANK DATA --------------------------
INITIAL_ACCOUNT = {
    "name": "Saurav",
    "account_no": "1234567890",
    "balance": 100000.0,
    "pin": "4321",
    "type": "Personal Account"
}

OTHER_ACCOUNTS = {
    "9876543210": {
        "name": "Rahul",
        "balance": 50000.0
    }
}

MAX_WITHDRAWAL = 20000.0
DAILY_WITHDRAWAL_LIMIT = 50000.0

# -------------------- SESSION STATE ----------------------
defaults = {
    "account": dict(INITIAL_ACCOUNT),
    "other_accounts": {k: dict(v) for k, v in OTHER_ACCOUNTS.items()},
    "daily_withdrawal": 0.0,
    "transaction_history": [],
    "transaction_id": 1000,
    "logged_in": False,
    "login_attempts": 3,
    "locked": False,
    "active_page": "Dashboard",
    "toast": None,
    "last_transaction": None,
    "deposit_amount": 1000.0,
    "withdraw_amount": 1000.0,
    "transfer_amount": 1000.0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -------------------- HELPERS ----------------------------
def money(value):
    return f"₹{value:,.2f}"

def generate_transaction_id():
    st.session_state.transaction_id += 1
    return f"TXN{st.session_state.transaction_id}"

def add_transaction(kind, amount, description, balance_after):
    txn_id = generate_transaction_id()
    now = datetime.now().strftime("%d %b %Y, %I:%M %p")
    st.session_state.transaction_history.insert(0, {
        "id": txn_id,
        "date": now,
        "type": kind,
        "amount": float(amount),
        "description": description,
        "balance": float(balance_after)
    })
    return txn_id

def masked_account():
    return "XXXXXX" + st.session_state.account["account_no"][-4:]

def flash(message, kind="success"):
    st.session_state.toast = {"message": message, "kind": kind}

def reset_demo():
    st.session_state.account = dict(INITIAL_ACCOUNT)
    st.session_state.other_accounts = {k: dict(v) for k, v in OTHER_ACCOUNTS.items()}
    st.session_state.daily_withdrawal = 0.0
    st.session_state.transaction_history = []
    st.session_state.transaction_id = 1000
    st.session_state.logged_in = False
    st.session_state.login_attempts = 3
    st.session_state.locked = False
    st.session_state.active_page = "Dashboard"
    st.session_state.last_transaction = None
    st.session_state.toast = None

# -------------------- CUSTOM CSS -------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --navy: #07111f;
    --navy2: #0d1b2e;
    --blue: #1d9bf0;
    --cyan: #31d7ff;
    --green: #20d49b;
    --red: #ff5c7a;
    --gold: #f7c948;
    --text: #eef6ff;
    --muted: #8ea4bd;
    --card: rgba(15, 31, 51, 0.82);
    --border: rgba(115, 174, 224, 0.16);
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 5%, rgba(29,155,240,.15), transparent 27%),
        radial-gradient(circle at 90% 20%, rgba(49,215,255,.10), transparent 24%),
        linear-gradient(135deg, #050b14 0%, #07111f 45%, #0b1829 100%);
    color: var(--text);
}

.block-container {
    max-width: 1400px;
    padding: 1.4rem 2rem 3rem;
}

#MainMenu, footer, header {visibility: hidden;}

.bank-header {
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding:18px 22px;
    border:1px solid var(--border);
    border-radius:24px;
    background:linear-gradient(135deg, rgba(19,40,64,.95), rgba(8,20,35,.88));
    box-shadow:0 18px 55px rgba(0,0,0,.28);
    margin-bottom:20px;
}

.brand {
    display:flex;
    align-items:center;
    gap:14px;
}

.logo {
    width:54px;
    height:54px;
    border-radius:16px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:28px;
    background:linear-gradient(135deg,#31d7ff,#1d9bf0);
    box-shadow:0 0 28px rgba(49,215,255,.30);
}

.bank-name {
    font-family:'Space Grotesk',sans-serif;
    font-size:22px;
    font-weight:800;
    letter-spacing:-.5px;
}

.tagline {
    color:var(--muted);
    font-size:12px;
    margin-top:2px;
}

.status {
    padding:8px 13px;
    border-radius:999px;
    color:#a7f5d9;
    background:rgba(32,212,155,.10);
    border:1px solid rgba(32,212,155,.25);
    font-size:12px;
    font-weight:700;
}

.hero {
    padding:28px;
    border-radius:26px;
    background:linear-gradient(135deg, rgba(22,47,75,.90), rgba(10,24,41,.88));
    border:1px solid var(--border);
    box-shadow:0 20px 60px rgba(0,0,0,.20);
    position:relative;
    overflow:hidden;
}

.hero:after {
    content:"";
    position:absolute;
    width:280px;
    height:280px;
    right:-90px;
    top:-120px;
    border-radius:50%;
    background:rgba(49,215,255,.10);
    filter:blur(8px);
}

.hero-title {
    font-family:'Space Grotesk',sans-serif;
    font-size:38px;
    font-weight:800;
    margin:0 0 6px;
}

.hero-sub {
    color:var(--muted);
    font-size:14px;
}

.balance-card {
    padding:26px;
    border-radius:24px;
    background:linear-gradient(135deg,#102b48,#0b1d32);
    border:1px solid rgba(49,215,255,.20);
    box-shadow:inset 0 1px 0 rgba(255,255,255,.04), 0 20px 50px rgba(0,0,0,.18);
}

.balance-label { color:#8fa9c4; font-size:13px; }
.balance {
    font-family:'Space Grotesk',sans-serif;
    font-size:36px;
    font-weight:800;
    margin:8px 0 4px;
}
.account-small { color:#b7c8d9; font-size:12px; }

.metric-card {
    padding:18px;
    border-radius:19px;
    background:var(--card);
    border:1px solid var(--border);
    min-height:110px;
}
.metric-label { color:var(--muted); font-size:12px; }
.metric-value { font-size:23px; font-weight:800; margin-top:8px; }

.section-title {
    font-family:'Space Grotesk',sans-serif;
    font-size:22px;
    font-weight:800;
    margin:26px 0 12px;
}

.txn-card {
    padding:15px 17px;
    margin:8px 0;
    border-radius:16px;
    background:rgba(12,27,45,.80);
    border:1px solid var(--border);
    display:flex;
    align-items:center;
    justify-content:space-between;
}

.txn-left { display:flex; gap:12px; align-items:center; }
.txn-icon {
    width:40px; height:40px; border-radius:13px;
    display:flex; align-items:center; justify-content:center;
    background:rgba(49,215,255,.09);
    font-size:18px;
}
.txn-name { font-weight:700; font-size:13px; }
.txn-date { color:var(--muted); font-size:11px; margin-top:3px; }
.txn-amount { font-weight:800; }
.credit { color:#39e6ae; }
.debit { color:#ff718c; }

.receipt {
    border-radius:22px;
    padding:22px;
    background:linear-gradient(135deg, rgba(16,48,64,.92), rgba(9,28,40,.92));
    border:1px solid rgba(32,212,155,.20);
    animation:pop .45s ease;
}
@keyframes pop {
    0% {transform:scale(.97); opacity:.2;}
    100% {transform:scale(1); opacity:1;}
}

div.stButton > button {
    width:100%;
    border-radius:14px;
    border:1px solid rgba(115,174,224,.16);
    background:linear-gradient(135deg,#112a44,#0d2035);
    color:#edf7ff;
    font-weight:700;
    padding:11px 14px;
    transition:all .2s ease;
}
div.stButton > button:hover {
    border-color:rgba(49,215,255,.55);
    transform:translateY(-2px);
    box-shadow:0 8px 25px rgba(29,155,240,.16);
}

div[data-testid="stForm"] {
    background:rgba(12,27,45,.72);
    padding:22px;
    border-radius:22px;
    border:1px solid var(--border);
}

.stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
    background:#0a1b2e !important;
    color:#eef6ff !important;
    border-radius:12px !important;
}

div[data-testid="stMetric"] {
    background:rgba(12,27,45,.70);
    padding:15px;
    border-radius:16px;
    border:1px solid var(--border);
}

.login-box {
    max-width:520px;
    margin:55px auto 0;
    padding:34px;
    border-radius:28px;
    background:linear-gradient(145deg,rgba(17,39,64,.96),rgba(7,19,32,.96));
    border:1px solid rgba(49,215,255,.18);
    box-shadow:0 25px 80px rgba(0,0,0,.36);
}

.login-logo {
    text-align:center;
    font-size:55px;
    margin-bottom:8px;
}

.login-title {
    text-align:center;
    font-family:'Space Grotesk',sans-serif;
    font-size:30px;
    font-weight:800;
}

.login-sub {
    text-align:center;
    color:var(--muted);
    font-size:13px;
    margin-bottom:22px;
}

.sidebar-note {
    padding:14px;
    border-radius:16px;
    background:rgba(49,215,255,.07);
    border:1px solid rgba(49,215,255,.13);
    color:#a8bfd5;
    font-size:12px;
    line-height:1.6;
}

.small-footer {
    text-align:center;
    color:#60778e;
    font-size:11px;
    padding-top:30px;
}

[data-testid="stSidebar"] {
    background:linear-gradient(180deg,#07111f,#081728);
}
</style>
""", unsafe_allow_html=True)

# -------------------- LOGIN SCREEN -----------------------
def login_screen():
    st.markdown("""
    <div class="login-box">
        <div class="login-logo">🏦</div>
        <div class="login-title">Lena ek na Dena Do Bank</div>
        <div class="login-sub">Secure ATM Banking • Smart • Simple • Reliable</div>
    </div>
    """, unsafe_allow_html=True)

    _, center, _ = st.columns([1, 2, 1])
    with center:
        with st.form("login_form"):
            st.markdown("### 🔐 Enter Your PIN")
            pin = st.text_input(
                "4-digit PIN",
                type="password",
                max_chars=4,
                placeholder="Enter PIN"
            )
            submitted = st.form_submit_button("🔓 Secure Login", use_container_width=True)

        st.caption(f"Attempts remaining: **{st.session_state.login_attempts}**")

        if submitted:
            if not pin.isdigit() or len(pin) != 4:
                st.error("PIN must contain exactly 4 digits.")
            elif pin == st.session_state.account["pin"]:
                st.session_state.logged_in = True
                st.session_state.login_attempts = 3
                st.session_state.active_page = "Dashboard"
                st.session_state.last_transaction = None
                st.rerun()
            else:
                st.session_state.login_attempts -= 1
                if st.session_state.login_attempts <= 0:
                    st.session_state.locked = True
                    st.error("🔒 Account locked after 3 incorrect attempts.")
                else:
                    st.error(f"Invalid PIN. {st.session_state.login_attempts} attempt(s) remaining.")

        st.markdown("""
        <div class="sidebar-note" style="margin-top:15px;">
        <b>Demo account</b><br>
        Use the PIN <b>4321</b> to test the ATM.<br>
        This is a local Streamlit demo and does not connect to a real bank.
        </div>
        """, unsafe_allow_html=True)

    if st.session_state.locked:
        st.warning("For this demo, refresh the page to restart the session.")

# -------------------- SIDEBAR ----------------------------
def sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center;padding:10px 0 18px;">
            <div style="font-size:40px;">🏦</div>
            <div style="font-family:'Space Grotesk';font-size:17px;font-weight:800;">
                Lena ek na Dena Do Bank
            </div>
        </div>
        """, unsafe_allow_html=True)

        pages = [
            ("🏠", "Dashboard"),
            ("💰", "Deposit Money"),
            ("💸", "Withdraw Money"),
            ("🔄", "Transfer Money"),
            ("👤", "Account Details"),
            ("🔐", "Change PIN"),
            ("🧾", "Mini Statement"),
            ("📊", "Transaction History"),
        ]

        for icon, page in pages:
            if st.button(f"{icon}  {page}", key=f"nav_{page}", use_container_width=True):
                st.session_state.active_page = page
                st.session_state.last_transaction = None
                st.rerun()

        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.active_page = "Dashboard"
            st.session_state.last_transaction = None
            st.rerun()

        if st.button("♻️ Reset Demo Data", use_container_width=True):
            reset_demo()
            st.rerun()

        st.markdown("""
        <div class="sidebar-note">
        <b>ATM Limits</b><br>
        Max single withdrawal: ₹20,000<br>
        Daily withdrawal limit: ₹50,000
        </div>
        """, unsafe_allow_html=True)

# -------------------- HEADER ------------------------------
def header():
    st.markdown("""
    <div class="bank-header">
        <div class="brand">
            <div class="logo">🏦</div>
            <div>
                <div class="bank-name">Lena ek na Dena Do Bank</div>
                <div class="tagline">Your money. Your control. Your ATM.</div>
            </div>
        </div>
        <div class="status">● ATM ONLINE</div>
    </div>
    """, unsafe_allow_html=True)

# -------------------- DASHBOARD --------------------------
def dashboard():
    acc = st.session_state.account
    remaining = max(DAILY_WITHDRAWAL_LIMIT - st.session_state.daily_withdrawal, 0)

    st.markdown(f"""
    <div class="hero">
        <div class="hero-title">Good to see you, {acc["name"]} 👋</div>
        <div class="hero-sub">Welcome to your secure digital ATM dashboard.</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    c1, c2 = st.columns([1.55, 1])
    with c1:
        st.markdown(f"""
        <div class="balance-card">
            <div class="balance-label">AVAILABLE BALANCE</div>
            <div class="balance">{money(acc["balance"])}</div>
            <div class="account-small">{acc["type"]} • {masked_account()}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">TODAY'S WITHDRAWAL</div>
            <div class="metric-value">%s</div>
            <div class="metric-label">Remaining limit: %s</div>
        </div>
        """ % (money(st.session_state.daily_withdrawal), money(remaining)), unsafe_allow_html=True)

    st.markdown('<div class="section-title">⚡ Quick Actions</div>', unsafe_allow_html=True)
    q1, q2, q3, q4 = st.columns(4)
    if q1.button("💰 Deposit", use_container_width=True):
        st.session_state.active_page = "Deposit Money"
        st.rerun()
    if q2.button("💸 Withdraw", use_container_width=True):
        st.session_state.active_page = "Withdraw Money"
        st.rerun()
    if q3.button("🔄 Transfer", use_container_width=True):
        st.session_state.active_page = "Transfer Money"
        st.rerun()
    if q4.button("🧾 Statement", use_container_width=True):
        st.session_state.active_page = "Mini Statement"
        st.rerun()

    st.markdown('<div class="section-title">🕘 Recent Transactions</div>', unsafe_allow_html=True)
    if not st.session_state.transaction_history:
        st.info("No transactions yet. Make a deposit, withdrawal, or transfer to see activity here.")
    else:
        for txn in st.session_state.transaction_history[:5]:
            is_credit = txn["type"] == "Deposit"
            icon = "↓" if is_credit else ("↗" if txn["type"] == "Withdrawal" else "⇄")
            cls = "credit" if is_credit else "debit"
            sign = "+" if is_credit else "-"
            st.markdown(f"""
            <div class="txn-card">
                <div class="txn-left">
                    <div class="txn-icon">{icon}</div>
                    <div>
                        <div class="txn-name">{txn["description"]}</div>
                        <div class="txn-date">{txn["date"]} • {txn["id"]}</div>
                    </div>
                </div>
                <div class="txn-amount {cls}">{sign}{money(txn["amount"])}</div>
            </div>
            """, unsafe_allow_html=True)

# -------------------- DEPOSIT ----------------------------
def deposit_page():
    st.markdown('<div class="section-title">💰 Deposit Money</div>', unsafe_allow_html=True)
    st.caption("Add money to your account. The balance and transaction history update immediately.")

    with st.form("deposit_form"):
        amount = st.number_input(
            "Deposit Amount (₹)",
            min_value=0.0,
            step=500.0,
            value=float(st.session_state.deposit_amount),
            format="%.2f"
        )
        confirm = st.form_submit_button("💰 Deposit Money", use_container_width=True)

    if confirm:
        if amount <= 0:
            st.error("Deposit amount must be greater than ₹0.")
        else:
            # IMPORTANT: balance is updated first, then the transaction is recorded.
            st.session_state.account["balance"] += float(amount)
            txn_id = add_transaction(
                "Deposit",
                amount,
                "Cash Deposit",
                st.session_state.account["balance"]
            )
            st.session_state.last_transaction = {
                "type": "Deposit",
                "amount": amount,
                "txn_id": txn_id,
                "balance": st.session_state.account["balance"]
            }
            flash(f"{money(amount)} deposited successfully.")
            st.rerun()

    if st.session_state.last_transaction and st.session_state.last_transaction["type"] == "Deposit":
        r = st.session_state.last_transaction
        st.markdown(f"""
        <div class="receipt">
            <h3>✅ Deposit Successful</h3>
            <p><b>Amount:</b> {money(r["amount"])}</p>
            <p><b>Transaction ID:</b> {r["txn_id"]}</p>
            <p><b>New Balance:</b> {money(r["balance"])}</p>
        </div>
        """, unsafe_allow_html=True)

# -------------------- WITHDRAW ---------------------------
def withdraw_page():
    st.markdown('<div class="section-title">💸 Withdraw Money</div>', unsafe_allow_html=True)

    balance = st.session_state.account["balance"]
    remaining_limit = DAILY_WITHDRAWAL_LIMIT - st.session_state.daily_withdrawal

    st.info(
        f"Available balance: **{money(balance)}**  •  "
        f"Remaining daily withdrawal limit: **{money(remaining_limit)}**"
    )

    with st.form("withdraw_form"):
        amount = st.number_input(
            "Withdrawal Amount (₹)",
            min_value=0.0,
            step=500.0,
            value=float(st.session_state.withdraw_amount),
            format="%.2f"
        )
        confirm = st.form_submit_button("💸 Withdraw Money", use_container_width=True)

    if confirm:
        if amount <= 0:
            st.error("Withdrawal amount must be greater than ₹0.")
        elif amount > MAX_WITHDRAWAL:
            st.error(f"Maximum withdrawal per transaction is {money(MAX_WITHDRAWAL)}.")
        elif amount > remaining_limit:
            st.error(f"Daily limit exceeded. You can withdraw only {money(remaining_limit)} more today.")
        elif amount > st.session_state.account["balance"]:
            st.error("Insufficient balance.")
        else:
            # IMPORTANT: all validations happen before changing the balance.
            st.session_state.account["balance"] -= float(amount)
            st.session_state.daily_withdrawal += float(amount)
            txn_id = add_transaction(
                "Withdrawal",
                amount,
                "ATM Cash Withdrawal",
                st.session_state.account["balance"]
            )
            st.session_state.last_transaction = {
                "type": "Withdrawal",
                "amount": amount,
                "txn_id": txn_id,
                "balance": st.session_state.account["balance"]
            }
            flash(f"{money(amount)} withdrawn successfully.")
            st.rerun()

    if st.session_state.last_transaction and st.session_state.last_transaction["type"] == "Withdrawal":
        r = st.session_state.last_transaction
        st.markdown(f"""
        <div class="receipt">
            <h3>✅ Withdrawal Successful</h3>
            <p><b>Amount:</b> {money(r["amount"])}</p>
            <p><b>Transaction ID:</b> {r["txn_id"]}</p>
            <p><b>Remaining Balance:</b> {money(r["balance"])}</p>
            <hr>
            <p style="color:#8ea4bd;font-size:12px;">Please collect your cash and card.</p>
        </div>
        """, unsafe_allow_html=True)

# -------------------- TRANSFER ---------------------------
def transfer_page():
    st.markdown('<div class="section-title">🔄 Transfer Money</div>', unsafe_allow_html=True)

    with st.form("transfer_form"):
        recipient = st.text_input("Recipient Account Number", max_chars=10, placeholder="9876543210")
        amount = st.number_input(
            "Transfer Amount (₹)",
            min_value=0.0,
            step=500.0,
            value=float(st.session_state.transfer_amount),
            format="%.2f"
        )
        confirm = st.form_submit_button("🔄 Transfer Money", use_container_width=True)

    if confirm:
        recipient = recipient.strip()

        if not recipient.isdigit() or len(recipient) != 10:
            st.error("Enter a valid 10-digit recipient account number.")
        elif recipient == st.session_state.account["account_no"]:
            st.error("You cannot transfer money to your own account.")
        elif recipient not in st.session_state.other_accounts:
            st.error("Recipient account not found.")
        elif amount <= 0:
            st.error("Transfer amount must be greater than ₹0.")
        elif amount > st.session_state.account["balance"]:
            st.error("Insufficient balance.")
        else:
            st.session_state.account["balance"] -= float(amount)
            st.session_state.other_accounts[recipient]["balance"] += float(amount)
            recipient_name = st.session_state.other_accounts[recipient]["name"]
            txn_id = add_transaction(
                "Transfer",
                amount,
                f"Transfer to {recipient_name}",
                st.session_state.account["balance"]
            )
            st.session_state.last_transaction = {
                "type": "Transfer",
                "amount": amount,
                "txn_id": txn_id,
                "balance": st.session_state.account["balance"],
                "recipient": recipient_name
            }
            flash(f"{money(amount)} transferred successfully.")
            st.rerun()

    if st.session_state.last_transaction and st.session_state.last_transaction["type"] == "Transfer":
        r = st.session_state.last_transaction
        st.markdown(f"""
        <div class="receipt">
            <h3>✅ Transfer Successful</h3>
            <p><b>Recipient:</b> {r["recipient"]}</p>
            <p><b>Amount:</b> {money(r["amount"])}</p>
            <p><b>Transaction ID:</b> {r["txn_id"]}</p>
            <p><b>New Balance:</b> {money(r["balance"])}</p>
        </div>
        """, unsafe_allow_html=True)

# -------------------- ACCOUNT DETAILS --------------------
def account_page():
    acc = st.session_state.account
    st.markdown('<div class="section-title">👤 Account Details</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">ACCOUNT HOLDER</div>
            <div class="metric-value">{acc["name"]}</div>
            <div class="metric-label">Account Type: {acc["type"]}</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">ACCOUNT NUMBER</div>
            <div class="metric-value">{masked_account()}</div>
            <div class="metric-label">Balance: {money(acc["balance"])}</div>
        </div>
        """, unsafe_allow_html=True)

# -------------------- CHANGE PIN -------------------------
def change_pin_page():
    st.markdown('<div class="section-title">🔐 Change PIN</div>', unsafe_allow_html=True)

    with st.form("change_pin_form"):
        old_pin = st.text_input("Current PIN", type="password", max_chars=4)
        new_pin = st.text_input("New 4-digit PIN", type="password", max_chars=4)
        confirm_pin = st.text_input("Confirm New PIN", type="password", max_chars=4)
        confirm = st.form_submit_button("🔐 Change PIN", use_container_width=True)

    if confirm:
        if old_pin != st.session_state.account["pin"]:
            st.error("Incorrect current PIN.")
        elif not new_pin.isdigit() or len(new_pin) != 4:
            st.error("New PIN must contain exactly 4 digits.")
        elif new_pin != confirm_pin:
            st.error("New PINs do not match.")
        elif new_pin == old_pin:
            st.error("New PIN must be different from the current PIN.")
        else:
            st.session_state.account["pin"] = new_pin
            st.success("✅ PIN changed successfully.")

# -------------------- STATEMENT --------------------------
def statement_page():
    st.markdown('<div class="section-title">🧾 Mini Statement</div>', unsafe_allow_html=True)

    if not st.session_state.transaction_history:
        st.info("No transactions yet.")
    else:
        for txn in st.session_state.transaction_history[:10]:
            sign = "+" if txn["type"] == "Deposit" else "-"
            cls = "credit" if txn["type"] == "Deposit" else "debit"
            st.markdown(f"""
            <div class="txn-card">
                <div>
                    <div class="txn-name">{txn["description"]}</div>
                    <div class="txn-date">{txn["date"]} • {txn["id"]}</div>
                </div>
                <div>
                    <div class="txn-amount {cls}">{sign}{money(txn["amount"])}</div>
                    <div class="txn-date">Balance: {money(txn["balance"])}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="balance-card" style="margin-top:15px;">
        <div class="balance-label">CURRENT BALANCE</div>
        <div class="balance">{money(st.session_state.account["balance"])}</div>
    </div>
    """, unsafe_allow_html=True)

# -------------------- HISTORY ----------------------------
def history_page():
    st.markdown('<div class="section-title">📊 Transaction History</div>', unsafe_allow_html=True)

    history = st.session_state.transaction_history
    if not history:
        st.info("No transactions found.")
        return

    deposits = sum(x["amount"] for x in history if x["type"] == "Deposit")
    withdrawals = sum(x["amount"] for x in history if x["type"] == "Withdrawal")
    transfers = sum(x["amount"] for x in history if x["type"] == "Transfer")

    a, b, c = st.columns(3)
    a.metric("Total Deposits", money(deposits))
    b.metric("Total Withdrawals", money(withdrawals))
    c.metric("Total Transfers", money(transfers))

    st.write("")
    for txn in history:
        sign = "+" if txn["type"] == "Deposit" else "-"
        cls = "credit" if txn["type"] == "Deposit" else "debit"
        icon = {"Deposit": "💰", "Withdrawal": "💸", "Transfer": "🔄"}.get(txn["type"], "💳")
        st.markdown(f"""
        <div class="txn-card">
            <div class="txn-left">
                <div class="txn-icon">{icon}</div>
                <div>
                    <div class="txn-name">{txn["description"]}</div>
                    <div class="txn-date">{txn["date"]} • {txn["id"]}</div>
                </div>
            </div>
            <div>
                <div class="txn-amount {cls}">{sign}{money(txn["amount"])}</div>
                <div class="txn-date">Balance: {money(txn["balance"])}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# -------------------- MAIN APP ---------------------------
if not st.session_state.logged_in:
    login_screen()
else:
    sidebar()
    header()

    if st.session_state.toast:
        kind = st.session_state.toast["kind"]
        message = st.session_state.toast["message"]
        if kind == "success":
            st.success(message)
        else:
            st.error(message)
        st.session_state.toast = None

    page = st.session_state.active_page

    if page == "Dashboard":
        dashboard()
    elif page == "Deposit Money":
        deposit_page()
    elif page == "Withdraw Money":
        withdraw_page()
    elif page == "Transfer Money":
        transfer_page()
    elif page == "Account Details":
        account_page()
    elif page == "Change PIN":
        change_pin_page()
    elif page == "Mini Statement":
        statement_page()
    elif page == "Transaction History":
        history_page()

    st.markdown("""
    <div class="small-footer">
        Lena ek na Dena Do Bank • Demo ATM Interface • Built with Python + Streamlit
    </div>
    """, unsafe_allow_html=True)
