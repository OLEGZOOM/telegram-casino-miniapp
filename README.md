# Casino Bot

A Telegram casino bot built with Python that offers various gambling games with virtual currency.

## Features

- 🎰 **Slot Machine** - Spin the reels and try to match symbols
- 🎲 **Dice Roll** - Roll dice against the house
- 🪙 **Coin Flip** - Call heads or tails
- 🃏 **Blackjack** - Beat the dealer's hand
- 💰 **Virtual Currency System** - Earn and spend virtual coins
- 📊 **Statistics Tracking** - Track your wins, losses, and games played
- 🎁 **Daily Bonus** - Get free coins every day

## Setup

1. **Create a Telegram Bot**:
   - Message [@BotFather](https://t.me/botfather) on Telegram
   - Use the `/newbot` command
   - Follow the instructions to create your bot
   - Copy the bot token

2. **Configure the Bot**:
   - Open the `.env` file
   - Replace `YOUR_BOT_TOKEN_HERE` with your actual bot token

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Bot**:
   ```bash
   python casino_bot.py
   ```

## Commands

- `/start` - Start the bot and see available commands
- `/balance` - Check your current balance
- `/stats` - View your gambling statistics
- `/daily` - Claim daily bonus (500 coins)
- `/slots [bet]` - Play slot machine (bet: $10-100)
- `/dice [bet]` - Play dice roll (bet: $5-50)
- `/coinflip [bet] [heads/tails]` - Play coin flip (bet: $5-100)
- `/blackjack [bet]` - Play blackjack (bet: $20-200)
- `/help` - Show help message

## Game Rules

### Slot Machine
- Match 3 symbols to win
- Special symbols have higher payouts:
  - 💎 Diamond: 10x multiplier
  - 7️⃣ Seven: 8x multiplier
  - ⭐ Star: 5x multiplier
  - Other matches: 3x multiplier
- Two matching symbols: 1.5x multiplier

### Dice Roll
- Roll two dice against the house
- Higher total wins
- Ties return your bet

### Coin Flip
- Choose heads or tails
- 50/50 chance to win
- Correct guess doubles your bet

### Blackjack
- Simple blackjack rules
- Dealer draws until 17+
- Blackjack (21 with 2 cards) pays 1.5x
- Bust = automatic loss

## Files

- `casino_bot.py` - Main bot code
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (bot token)
- `casino_data.json` - User data storage (created automatically)

## Security Notes

- Keep your bot token secret
- Don't commit the `.env` file to version control
- This is for entertainment purposes only
- Virtual currency has no real-world value