import json
import os
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
import threading

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token from environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBAPP_URL = os.getenv('WEBAPP_URL', 'http://localhost:5000')  # Local development URL

class CasinoBot:
    def __init__(self):
        self.data_file = 'casino_data.json'
        self.load_data()
    
    def load_data(self):
        """Load user data from JSON file"""
        try:
            with open(self.data_file, 'r') as f:
                self.users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.users = {}
    
    def save_data(self):
        """Save user data to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def get_user(self, user_id):
        """Get or create user data"""
        user_id = str(user_id)
        if user_id not in self.users:
            self.users[user_id] = {
                'balance': 1000,  # Starting balance
                'total_winnings': 0,
                'total_losses': 0,
                'games_played': 0
            }
            self.save_data()
        return self.users[user_id]
    
    def update_balance(self, user_id, amount):
        """Update user balance"""
        user = self.get_user(user_id)
        user['balance'] += amount
        if amount > 0:
            user['total_winnings'] += amount
        else:
            user['total_losses'] += abs(amount)
        user['games_played'] += 1
        self.save_data()
        return user['balance']

# Initialize casino bot
casino = CasinoBot()

# Flask app for Mini App
app = Flask(__name__)

@app.route('/')
def index():
    """Serve the main casino Mini App page"""
    return render_template('casino.html')

@app.route('/api/user/<user_id>')
def get_user_data(user_id):
    """API endpoint to get user data"""
    user = casino.get_user(user_id)
    return jsonify(user)

@app.route('/api/play', methods=['POST'])
def play_game():
    """API endpoint to handle game results"""
    data = request.json
    user_id = data.get('user_id')
    game_type = data.get('game_type')
    bet_amount = data.get('bet_amount', 0)
    result = data.get('result', 'loss')
    
    # Calculate winnings based on result
    if result == 'win':
        winnings = bet_amount
    elif result == 'big_win':
        winnings = bet_amount * 2
    elif result == 'jackpot':
        winnings = bet_amount * 10
    else:
        winnings = -bet_amount
    
    # Update user balance
    new_balance = casino.update_balance(user_id, winnings)
    
    return jsonify({
        'success': True,
        'new_balance': new_balance,
        'winnings': winnings
    })

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command handler"""
    user = casino.get_user(update.effective_user.id)
    
    # Create inline keyboard with Mini App button
    keyboard = [
        [InlineKeyboardButton(
            "🎰 Open Casino", 
            web_app=WebAppInfo(url=f"{WEBAPP_URL}")
        )],
        [InlineKeyboardButton("💳 Balance", callback_data="balance")],
        [InlineKeyboardButton("📊 Statistics", callback_data="stats")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_message = f"""
🎰 **Welcome to Casino Mini App!** 🎰

💰 Your balance: ${user['balance']}

Click "🎰 Open Casino" to play games in our interactive Mini App!

**Available Games in Mini App:**
🎰 Slot Machine - Spin for big wins!
🎲 Dice Roll - Beat the house
🪙 Coin Flip - Double or nothing
🃏 Blackjack - 21 or bust

Good luck and have fun! 🍀
    """
    
    await update.message.reply_text(
        welcome_message, 
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline keyboard button presses"""
    query = update.callback_query
    await query.answer()
    
    user = casino.get_user(update.effective_user.id)
    
    if query.data == "balance":
        await query.edit_message_text(
            f"💰 Your current balance: ${user['balance']}\n\n"
            f"Click 🎰 Open Casino to play games!",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    "🎰 Open Casino", 
                    web_app=WebAppInfo(url=f"{WEBAPP_URL}")
                )
            ]])
        )
    
    elif query.data == "stats":
        stats_message = f"""
📊 **Your Casino Statistics** 📊

💰 Current Balance: ${user['balance']}
🏆 Total Winnings: ${user['total_winnings']}
📉 Total Losses: ${user['total_losses']}
🎮 Games Played: {user['games_played']}
📈 Net Profit: ${user['total_winnings'] - user['total_losses']}
        """
        
        await query.edit_message_text(
            stats_message,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    "🎰 Open Casino", 
                    web_app=WebAppInfo(url=f"{WEBAPP_URL}")
                )
            ]])
        )

async def balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Balance command"""
    user = casino.get_user(update.effective_user.id)
    
    keyboard = [[InlineKeyboardButton(
        "🎰 Open Casino", 
        web_app=WebAppInfo(url=f"{WEBAPP_URL}")
    )]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"💰 Your current balance: ${user['balance']}", 
        reply_markup=reply_markup
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Statistics command"""
    user = casino.get_user(update.effective_user.id)
    
    keyboard = [[InlineKeyboardButton(
        "🎰 Open Casino", 
        web_app=WebAppInfo(url=f"{WEBAPP_URL}")
    )]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    stats_message = f"""
📊 **Your Casino Statistics** 📊

💰 Current Balance: ${user['balance']}
🏆 Total Winnings: ${user['total_winnings']}
📉 Total Losses: ${user['total_losses']}
🎮 Games Played: {user['games_played']}
📈 Net Profit: ${user['total_winnings'] - user['total_losses']}
    """
    
    await update.message.reply_text(
        stats_message,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Help command"""
    await start(update, context)

def run_flask():
    """Run Flask app in a separate thread"""
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

def main() -> None:
    """Start the bot and Flask server"""
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN not found in environment variables!")
        print("Please set your bot token in the .env file")
        return
    
    # Start Flask server in a separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("balance", balance_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Run the bot
    print("Casino Mini App Bot is starting...")
    print(f"Flask server running on {WEBAPP_URL}")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()