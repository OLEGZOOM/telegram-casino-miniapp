# Telegram Casino Mini App Bot

A modern Telegram casino bot that uses **Telegram Mini Apps** for an interactive gaming experience. Instead of text-based commands, users play games through a beautiful web interface launched directly within Telegram.

## 🎰 Features

### Mini App Games
- **🎰 Slot Machine** - Interactive spinning reels with animations
- **🎲 Dice Roll** - Visual dice rolling game
- **🪙 Coin Flip** - Choose heads or tails with animations
- **🃏 Blackjack** - Classic card game interface

### Key Benefits of Mini Apps
- **Rich UI/UX** - Beautiful, responsive web interface
- **Interactive Animations** - Smooth game animations and effects
- **Mobile Optimized** - Perfect experience on all devices
- **Secure** - Runs within Telegram's secure environment
- **No Installation** - Works instantly within Telegram

### User Management
- 💰 Virtual currency system (starts with $1000)
- 📊 Statistics tracking (wins, losses, games played)
- 💾 Persistent data storage
- 🎮 Real-time balance updates

## 🚀 Setup Instructions

### 1. **Configure Bot Token**
- Open the `.env` file
- Your bot token is already configured: `8491363145:AAG7zu_NitgxPR6L4qfx1_QCCSb41NAdVSo`

### 2. **Set Up Mini App with BotFather**
To enable Mini Apps for your bot, you need to register the web app URL:

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/mybots`
3. Select your casino bot
4. Click "Bot Settings" → "Menu Button"
5. Send "Configure Menu Button"
6. For the button text, send: `🎰 Play Casino`
7. For the URL, send: `http://localhost:5000` (for development)

### 3. **Install Dependencies & Run**
```bash
# Install required packages
pip install -r requirements.txt

# Run the bot (this starts both the Telegram bot and web server)
python casino_miniapp_bot.py
```

The bot will start:
- 🤖 **Telegram Bot** - Handles user interactions
- 🌐 **Flask Web Server** - Serves the Mini App on `http://localhost:5000`

## 📱 How to Use

### For Users:
1. **Start the bot** - Send `/start` to your bot in Telegram
2. **Open Mini App** - Click the "🎰 Open Casino" button
3. **Play Games** - Choose from 4 different casino games
4. **Check Stats** - View balance and statistics anytime

### Bot Commands:
- `/start` - Welcome message with Mini App button
- `/balance` - Quick balance check with Mini App access
- `/stats` - View detailed statistics
- `/help` - Show help information

## 🎮 Mini App Interface

The Mini App features:

### Main Menu
- Beautiful gradient background
- Balance display with real-time updates
- 4 game cards with hover effects
- Responsive grid layout

### Game Controls
- Adjustable bet amounts with +/- buttons
- Game-specific options (like coin choice for flip)
- Animated play buttons
- Results display with win/loss animations

### Visual Effects
- Spinning slot machine reels
- Smooth transitions and hover effects
- Color-coded results (green for wins, red for losses)
- Modern glassmorphism design

## 🔧 Development vs Production

### Local Development
- Uses `http://localhost:5000`
- Perfect for testing and development
- No HTTPS required for localhost

### Production Deployment
1. **Deploy to a web server** (Heroku, Railway, DigitalOcean, etc.)
2. **Get HTTPS URL** (Mini Apps require HTTPS in production)
3. **Update .env file** with your production URL
4. **Update BotFather** with your production URL

Example production setup:
```env
WEBAPP_URL=https://your-casino-bot.herokuapp.com
```

## 🛡️ Security & Privacy

- All game logic runs client-side for instant feedback
- Server validates and processes all transactions
- User data is stored locally in JSON format
- No real money involved - virtual currency only
- Telegram Web App security handles user authentication

## 📁 Project Structure

```
apollo/
├── casino_miniapp_bot.py     # Main bot and Flask server
├── templates/
│   └── casino.html           # Mini App HTML interface
├── static/                   # CSS/JS assets (if needed)
├── casino_data.json          # User data storage (auto-created)
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
└── README.md                # This file
```

## 🎯 Next Steps

1. **Test locally** - Make sure everything works with localhost
2. **Deploy to production** - Use a cloud service for public access
3. **Update URLs** - Configure production URLs in BotFather
4. **Customize games** - Modify HTML/CSS for your preferred style
5. **Add features** - Tournaments, leaderboards, daily bonuses, etc.

## 💡 Tips

- **Testing**: Use Telegram's test environment for development
- **Styling**: Customize the CSS in `casino.html` for your brand
- **Games**: Add new games by extending the JavaScript functions
- **Analytics**: Track user behavior through the Flask server logs
- **Scaling**: Use a proper database (PostgreSQL, MongoDB) for production

---

**Enjoy your modern Telegram Casino Mini App! 🎰✨**