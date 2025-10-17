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
WEBAPP_URL = os.getenv('WEBAPP_URL', 'https://your-domain.com')  # Replace with your actual domain

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
                'games_played': 0,
                'last_daily': None
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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command handler"""
    user = casino.get_user(update.effective_user.id)
    
    welcome_message = f"""
🎰 **Welcome to Casino Bot!** 🎰

💰 Your balance: ${user['balance']}

**Available Games:**
🎰 /slots - Slot Machine (Bet: $10-100)
🎲 /dice - Dice Roll (Bet: $5-50)
🪙 /coinflip - Coin Flip (Bet: $5-100)
🃏 /blackjack - Blackjack (Bet: $20-200)

**Other Commands:**
💳 /balance - Check your balance
📊 /stats - View your statistics
🎁 /daily - Get daily bonus (500 coins)
ℹ️ /help - Show this message

Good luck and gamble responsibly! 🍀
    """
    
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show user balance"""
    user = casino.get_user(update.effective_user.id)
    await update.message.reply_text(f"💰 Your current balance: ${user['balance']}")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show user statistics"""
    user = casino.get_user(update.effective_user.id)
    
    stats_message = f"""
📊 **Your Casino Statistics** 📊

💰 Current Balance: ${user['balance']}
🏆 Total Winnings: ${user['total_winnings']}
📉 Total Losses: ${user['total_losses']}
🎮 Games Played: {user['games_played']}
📈 Net Profit: ${user['total_winnings'] - user['total_losses']}
    """
    
    await update.message.reply_text(stats_message, parse_mode='Markdown')

async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Daily bonus command"""
    user = casino.get_user(update.effective_user.id)
    today = datetime.now().strftime('%Y-%m-%d')
    
    if user['last_daily'] == today:
        await update.message.reply_text("🚫 You've already claimed your daily bonus today! Come back tomorrow.")
        return
    
    bonus = 500
    user['last_daily'] = today
    new_balance = casino.update_balance(update.effective_user.id, bonus)
    
    await update.message.reply_text(f"🎁 Daily bonus claimed! You received ${bonus}\n💰 New balance: ${new_balance}")

async def slots(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Slot machine game"""
    try:
        # Get bet amount from command arguments
        if context.args:
            bet = int(context.args[0])
        else:
            bet = 10  # Default bet
        
        if bet < 10 or bet > 100:
            await update.message.reply_text("🎰 Bet amount must be between $10 and $100!")
            return
        
        user = casino.get_user(update.effective_user.id)
        
        if user['balance'] < bet:
            await update.message.reply_text(f"💸 Insufficient balance! You have ${user['balance']}")
            return
        
        # Slot symbols
        symbols = ['🍒', '🍋', '🍊', '🍇', '⭐', '💎', '7️⃣']
        weights = [25, 20, 20, 15, 10, 5, 5]  # Probability weights
        
        # Spin the slots
        result = random.choices(symbols, weights=weights, k=3)
        
        # Calculate winnings
        if result[0] == result[1] == result[2]:
            if result[0] == '💎':
                multiplier = 10
            elif result[0] == '7️⃣':
                multiplier = 8
            elif result[0] == '⭐':
                multiplier = 5
            else:
                multiplier = 3
        elif result[0] == result[1] or result[1] == result[2] or result[0] == result[2]:
            multiplier = 1.5
        else:
            multiplier = 0
        
        winnings = int(bet * multiplier) - bet
        new_balance = casino.update_balance(update.effective_user.id, winnings)
        
        result_text = f"🎰 **SLOT MACHINE** 🎰\n\n"
        result_text += f"[ {' | '.join(result)} ]\n\n"
        
        if winnings > 0:
            result_text += f"🎉 **WINNER!** 🎉\n"
            result_text += f"💰 You won ${winnings}!\n"
        else:
            result_text += f"😔 Better luck next time!\n"
            result_text += f"💸 You lost ${bet}\n"
        
        result_text += f"💳 Balance: ${new_balance}"
        
        await update.message.reply_text(result_text, parse_mode='Markdown')
        
    except (ValueError, IndexError):
        await update.message.reply_text("🎰 Usage: /slots [bet_amount]\nExample: /slots 25")

async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Dice roll game"""
    try:
        if context.args:
            bet = int(context.args[0])
        else:
            bet = 5
        
        if bet < 5 or bet > 50:
            await update.message.reply_text("🎲 Bet amount must be between $5 and $50!")
            return
        
        user = casino.get_user(update.effective_user.id)
        
        if user['balance'] < bet:
            await update.message.reply_text(f"💸 Insufficient balance! You have ${user['balance']}")
            return
        
        # Roll two dice
        player_dice = [random.randint(1, 6), random.randint(1, 6)]
        house_dice = [random.randint(1, 6), random.randint(1, 6)]
        
        player_total = sum(player_dice)
        house_total = sum(house_dice)
        
        # Determine winner
        if player_total > house_total:
            winnings = bet
            result = "🎉 **YOU WIN!** 🎉"
        elif player_total < house_total:
            winnings = -bet
            result = "😔 **HOUSE WINS!**"
        else:
            winnings = 0
            result = "🤝 **IT'S A TIE!**"
        
        new_balance = casino.update_balance(update.effective_user.id, winnings)
        
        result_text = f"🎲 **DICE ROLL** 🎲\n\n"
        result_text += f"Your dice: {player_dice[0]} + {player_dice[1]} = {player_total}\n"
        result_text += f"House dice: {house_dice[0]} + {house_dice[1]} = {house_total}\n\n"
        result_text += f"{result}\n"
        
        if winnings > 0:
            result_text += f"💰 You won ${winnings}!\n"
        elif winnings < 0:
            result_text += f"💸 You lost ${abs(winnings)}\n"
        
        result_text += f"💳 Balance: ${new_balance}"
        
        await update.message.reply_text(result_text, parse_mode='Markdown')
        
    except (ValueError, IndexError):
        await update.message.reply_text("🎲 Usage: /dice [bet_amount]\nExample: /dice 20")

async def coinflip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Coin flip game"""
    if len(context.args) < 2:
        await update.message.reply_text("🪙 Usage: /coinflip [bet_amount] [heads/tails]\nExample: /coinflip 50 heads")
        return
    
    try:
        bet = int(context.args[0])
        choice = context.args[1].lower()
        
        if bet < 5 or bet > 100:
            await update.message.reply_text("🪙 Bet amount must be between $5 and $100!")
            return
        
        if choice not in ['heads', 'tails']:
            await update.message.reply_text("🪙 Choose 'heads' or 'tails'!")
            return
        
        user = casino.get_user(update.effective_user.id)
        
        if user['balance'] < bet:
            await update.message.reply_text(f"💸 Insufficient balance! You have ${user['balance']}")
            return
        
        # Flip the coin
        result = random.choice(['heads', 'tails'])
        coin_emoji = '👤' if result == 'heads' else '🔶'
        
        if choice == result:
            winnings = bet
            outcome = "🎉 **YOU WIN!** 🎉"
        else:
            winnings = -bet
            outcome = "😔 **YOU LOSE!**"
        
        new_balance = casino.update_balance(update.effective_user.id, winnings)
        
        result_text = f"🪙 **COIN FLIP** 🪙\n\n"
        result_text += f"Your choice: {choice.capitalize()}\n"
        result_text += f"Result: {coin_emoji} {result.capitalize()}\n\n"
        result_text += f"{outcome}\n"
        
        if winnings > 0:
            result_text += f"💰 You won ${winnings}!\n"
        else:
            result_text += f"💸 You lost ${abs(winnings)}\n"
        
        result_text += f"💳 Balance: ${new_balance}"
        
        await update.message.reply_text(result_text, parse_mode='Markdown')
        
    except (ValueError, IndexError):
        await update.message.reply_text("🪙 Usage: /coinflip [bet_amount] [heads/tails]\nExample: /coinflip 50 heads")

async def blackjack(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Simple blackjack game"""
    try:
        if context.args:
            bet = int(context.args[0])
        else:
            bet = 20
        
        if bet < 20 or bet > 200:
            await update.message.reply_text("🃏 Bet amount must be between $20 and $200!")
            return
        
        user = casino.get_user(update.effective_user.id)
        
        if user['balance'] < bet:
            await update.message.reply_text(f"💸 Insufficient balance! You have ${user['balance']}")
            return
        
        # Simple blackjack simulation
        def get_card_value():
            return random.randint(1, 11)
        
        def calculate_hand(cards):
            total = sum(cards)
            # Simple ace handling
            while total > 21 and 11 in cards:
                cards[cards.index(11)] = 1
                total = sum(cards)
            return total
        
        # Deal initial cards
        player_cards = [get_card_value(), get_card_value()]
        dealer_cards = [get_card_value(), get_card_value()]
        
        # Player draws until they choose to stop or bust (simplified)
        player_total = calculate_hand(player_cards)
        
        # Dealer draws until 17 or higher
        dealer_total = calculate_hand(dealer_cards)
        while dealer_total < 17:
            dealer_cards.append(get_card_value())
            dealer_total = calculate_hand(dealer_cards)
        
        # Determine winner
        if player_total > 21:
            winnings = -bet
            result = "💥 **BUST! YOU LOSE!**"
        elif dealer_total > 21:
            winnings = bet
            result = "🎉 **DEALER BUST! YOU WIN!**"
        elif player_total > dealer_total:
            winnings = bet
            result = "🎉 **YOU WIN!**"
        elif player_total < dealer_total:
            winnings = -bet
            result = "😔 **DEALER WINS!**"
        else:
            winnings = 0
            result = "🤝 **PUSH! IT'S A TIE!**"
        
        # Blackjack bonus
        if player_total == 21 and len(player_cards) == 2 and dealer_total != 21:
            winnings = int(bet * 1.5)
            result = "♠️ **BLACKJACK! YOU WIN!** ♠️"
        
        new_balance = casino.update_balance(update.effective_user.id, winnings)
        
        result_text = f"🃏 **BLACKJACK** 🃏\n\n"
        result_text += f"Your cards: {player_cards} = {player_total}\n"
        result_text += f"Dealer cards: {dealer_cards} = {dealer_total}\n\n"
        result_text += f"{result}\n"
        
        if winnings > 0:
            result_text += f"💰 You won ${winnings}!\n"
        elif winnings < 0:
            result_text += f"💸 You lost ${abs(winnings)}\n"
        
        result_text += f"💳 Balance: ${new_balance}"
        
        await update.message.reply_text(result_text, parse_mode='Markdown')
        
    except (ValueError, IndexError):
        await update.message.reply_text("🃏 Usage: /blackjack [bet_amount]\nExample: /blackjack 50")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Help command"""
    await start(update, context)

def main() -> None:
    """Start the bot"""
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN not found in environment variables!")
        print("Please set your bot token in the .env file")
        return
    
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("balance", balance))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("daily", daily))
    application.add_handler(CommandHandler("slots", slots))
    application.add_handler(CommandHandler("dice", dice))
    application.add_handler(CommandHandler("coinflip", coinflip))
    application.add_handler(CommandHandler("blackjack", blackjack))
    
    # Run the bot
    print("Casino Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()