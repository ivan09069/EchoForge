# EchoForge Integration Guide

> **Complete step-by-step guide** for integrating EchoForge into your project or setting it up as a standalone application.

This guide covers everything from prerequisites to advanced configuration, with clear examples for different integration scenarios.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Integration Scenarios](#integration-scenarios)
   - [Standalone Application](#scenario-1-standalone-application)
   - [React Application Integration](#scenario-2-react-application-integration)
   - [Vanilla JavaScript Integration](#scenario-3-vanilla-javascript-integration)
5. [Component Usage](#component-usage)
6. [Configuration](#configuration)
7. [Troubleshooting](#troubleshooting)
8. [Next Steps](#next-steps)

---

## Prerequisites

Before you begin, ensure you have the following:

### System Requirements

- **Node.js**: Version 18.x or higher
  ```bash
  # Check your Node.js version
  node --version
  ```
  If you need to install or upgrade Node.js, visit [nodejs.org](https://nodejs.org/)

- **npm**: Version 9.x or higher (comes with Node.js)
  ```bash
  # Check your npm version
  npm --version
  ```

### Browser Requirements

EchoForge requires a modern browser with WebAuthn support:

| Browser | Minimum Version | FIDO2 Support |
|---------|----------------|---------------|
| Chrome | 67+ | ✅ Full support |
| Firefox | 60+ | ✅ Full support |
| Safari | 14+ | ✅ Full support |
| Edge | 18+ | ✅ Full support |

### FIDO2 Authenticator

For biometric authentication, you need one of the following:

- **Built-in authenticators**:
  - Fingerprint scanner (Touch ID, Windows Hello)
  - Face recognition (Face ID)
  - Device PIN

- **External authenticators**:
  - YubiKey
  - Google Titan Security Key
  - Other FIDO2-certified hardware keys

### Development Tools (Optional)

- **Git**: For cloning the repository
- **Code editor**: VS Code, Sublime Text, or your preferred editor
- **Terminal**: Command line interface for running commands

---

## Installation

### Step 1: Clone the Repository

```bash
# Clone EchoForge from GitHub
git clone https://github.com/ivan09069/EchoForge.git

# Navigate to the project directory
cd EchoForge
```

### Step 2: Install Dependencies

```bash
# Install all required npm packages
npm install
```

This installs:
- **React 18**: UI framework
- **React DOM**: React rendering
- **Axios**: HTTP client for API requests
- **Vite**: Build tool and dev server

### Step 3: Verify Installation

```bash
# Check that all dependencies are installed correctly
npm list --depth=0
```

You should see output similar to:
```
echoforge@1.0.0 /path/to/EchoForge
├── axios@1.7.9
├── react@18.3.1
└── react-dom@18.3.1
```

---

## Quick Start

### Step 1: Start the Development Server

```bash
npm run dev
```

You should see output like:
```
VITE v6.0.1  ready in 324 ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
➜  press h + enter to show help
```

### Step 2: Open in Browser

Open your browser and navigate to:
```
http://localhost:5173/
```

### Step 3: Test the Application

1. **View the landing page**: You should see the EchoForge login interface
2. **Click "Login with Biometrics"**: This will simulate the FIDO2 authentication
3. **Access the dashboard**: After login, you'll see the portfolio dashboard with crypto momentum tracking

---

## Integration Scenarios

Choose the scenario that best fits your needs:

### Scenario 1: Standalone Application

**Use case**: Running EchoForge as a complete, standalone portfolio tracker.

#### Steps:

1. **Follow the installation steps** above (Clone → Install → Run)

2. **Customize the application**:
   ```bash
   # Edit the main configuration
   nano src/App.jsx
   ```

3. **Add your crypto holdings**:
   ```javascript
   // In components/Dashboard.js
   const holdings = [
     { symbol: 'BTC', label: 'Bitcoin', amount: 1.2 },
     { symbol: 'ETH', label: 'Ethereum', amount: 5.7 },
     { symbol: 'SOL', label: 'Solana', amount: 150 },
   ];
   ```

4. **Build for production**:
   ```bash
   npm run build
   ```

5. **Deploy** (see [Deployment Options](#deployment-options))

---

### Scenario 2: React Application Integration

**Use case**: Adding EchoForge components to an existing React application.

#### Step 1: Install Dependencies

In your existing React project:

```bash
npm install axios
```

#### Step 2: Copy Required Files

Copy the following files from EchoForge to your project:

```bash
# From EchoForge repository
├── components/
│   ├── CryptoSparks.jsx      # Crypto momentum tracker UI
│   ├── Dashboard.js          # Portfolio dashboard
│   ├── LoginFIDO2.js         # FIDO2 authentication
│   └── PriceFeed.js          # Price feed component
├── hooks/
│   ├── useCryptoMomentum.js  # RM²E scoring hook
│   └── useZcashShield.js     # Privacy-focused hook
```

Copy to your project:

```bash
# Create directories if they don't exist
mkdir -p src/components/echoforge
mkdir -p src/hooks

# Copy files (adjust paths as needed)
cp -r path/to/EchoForge/components/* src/components/echoforge/
cp -r path/to/EchoForge/hooks/* src/hooks/
```

#### Step 3: Import and Use Components

In your React component:

```javascript
import CryptoSparks from './components/echoforge/CryptoSparks';
import Dashboard from './components/echoforge/Dashboard';

function MyPortfolioPage() {
  return (
    <div className="portfolio-container">
      <h1>My Investment Dashboard</h1>
      
      {/* Add crypto momentum tracking */}
      <CryptoSparks 
        symbols={['bitcoin', 'ethereum', 'solana']}
        pollingInterval={2500}
      />
      
      {/* Or use the full dashboard */}
      <Dashboard />
    </div>
  );
}

export default MyPortfolioPage;
```

#### Step 4: Add Routing (Optional)

If using React Router:

```javascript
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LoginFIDO2 from './components/echoforge/LoginFIDO2';
import Dashboard from './components/echoforge/Dashboard';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginFIDO2 />} />
        <Route path="/portfolio" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  );
}
```

---

### Scenario 3: Vanilla JavaScript Integration

**Use case**: Adding crypto momentum tracking to a non-React application.

#### Step 1: Include Required Libraries

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My Portfolio Tracker</title>
</head>
<body>
  <div id="crypto-tracker"></div>
  
  <!-- Include Axios for API requests -->
  <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
  
  <script>
    // See next step for implementation
  </script>
</body>
</html>
```

#### Step 2: Implement Basic Crypto Tracking

```javascript
// Vanilla JS version of crypto momentum tracking
async function fetchCryptoMomentum(symbols) {
  const response = await axios.get(
    'https://api.coingecko.com/api/v3/coins/markets',
    {
      params: {
        vs_currency: 'usd',
        ids: symbols.join(','),
        price_change_percentage: '24h,7d'
      }
    }
  );
  
  return response.data.map(coin => {
    // Calculate RM²E score
    const change24h = coin.price_change_percentage_24h || 0;
    const change7d = coin.price_change_percentage_7d || 0;
    const marketCap = coin.market_cap || 1;
    
    const risk = Math.max(0.1, Math.sqrt(
      Math.pow(change24h, 2) + Math.pow(change7d / 7, 2)
    ) / 10);
    
    const momentum = Math.max(0, change24h * 0.7 + change7d * 0.3);
    
    let magic = 1;
    if (change24h > 10) magic = 20;
    else if (change24h > 5) magic = 15;
    else if (change24h > 0) magic = 10;
    
    const effort = Math.max(1, 100 / Math.log10(marketCap + 10));
    const rm2e = (momentum * magic) / (risk * effort) * 100;
    
    return {
      name: coin.name,
      symbol: coin.symbol,
      price: coin.current_price,
      change24h,
      rm2e: rm2e.toFixed(2)
    };
  });
}

// Display results
async function displayCryptoTracker() {
  const container = document.getElementById('crypto-tracker');
  const coins = await fetchCryptoMomentum(['bitcoin', 'ethereum', 'solana']);
  
  container.innerHTML = '<h2>⚡ Crypto Momentum Tracker</h2>';
  
  coins.forEach(coin => {
    const div = document.createElement('div');
    div.style.cssText = 'padding: 15px; margin: 10px 0; background: #1a1a2e; border-radius: 8px; color: white;';
    div.innerHTML = `
      <h3>${coin.name} (${coin.symbol.toUpperCase()})</h3>
      <p>Price: $${coin.price.toLocaleString()}</p>
      <p>24h Change: ${coin.change24h.toFixed(2)}%</p>
      <p>RM²E Score: ${coin.rm2e}</p>
    `;
    container.appendChild(div);
  });
}

// Initialize on page load
displayCryptoTracker();

// Update every 5 seconds
setInterval(displayCryptoTracker, 5000);
```

---

## Component Usage

### CryptoSparks Component

The main crypto momentum tracking UI component.

#### Basic Usage

```javascript
import CryptoSparks from './components/CryptoSparks';

<CryptoSparks 
  symbols={['bitcoin', 'ethereum', 'solana']}
  pollingInterval={2500}
/>
```

#### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `symbols` | `Array<string>` | Required | Array of CoinGecko coin IDs |
| `pollingInterval` | `number` | `2500` | Update interval in milliseconds |

#### Example with Custom Configuration

```javascript
<CryptoSparks 
  symbols={[
    'bitcoin',
    'ethereum',
    'solana',
    'cardano',
    'polkadot',
    'chainlink'
  ]}
  pollingInterval={5000}  // Update every 5 seconds
/>
```

---

### useCryptoMomentum Hook

Custom React hook for accessing crypto momentum data directly.

#### Basic Usage

```javascript
import useCryptoMomentum from './hooks/useCryptoMomentum';

function MyComponent() {
  const { data, rm2eScores, isOnline } = useCryptoMomentum(
    ['bitcoin', 'ethereum'],
    2500
  );
  
  return (
    <div>
      <p>Status: {isOnline ? 'Online' : 'Offline'}</p>
      {rm2eScores.map(coin => (
        <div key={coin.id}>
          <h3>{coin.name}</h3>
          <p>RM²E Score: {coin.rm2e}</p>
          <p>Signal: {coin.signal}</p>
        </div>
      ))}
    </div>
  );
}
```

#### Return Values

| Property | Type | Description |
|----------|------|-------------|
| `data` | `Array` | Raw CoinGecko API response |
| `rm2eScores` | `Array` | Calculated RM²E scores with components |
| `isOnline` | `boolean` | API connectivity status |

#### RM²E Score Object

```javascript
{
  id: 'bitcoin',
  name: 'Bitcoin',
  symbol: 'btc',
  price: 45000.50,
  change24h: 5.2,
  change7d: 12.5,
  market_cap: 850000000000,
  risk: 0.52,
  momentum: 7.39,
  magic: 15,
  effort: 1.23,
  rm2e: 142.5,
  signal: 'BUY'
}
```

---

### Dashboard Component

Complete portfolio overview with asset tracking.

#### Basic Usage

```javascript
import Dashboard from './components/Dashboard';

<Dashboard />
```

#### Customization

Edit the holdings array in `components/Dashboard.js`:

```javascript
const holdings = [
  { symbol: 'BTC', label: 'Bitcoin', amount: 1.2 },
  { symbol: 'ETH', label: 'Ethereum', amount: 5.7 },
  { symbol: 'SOL', label: 'Solana', amount: 150 },
  { symbol: 'ADA', label: 'Cardano', amount: 1000 },
];
```

---

### LoginFIDO2 Component

FIDO2 biometric authentication interface.

#### Basic Usage

```javascript
import LoginFIDO2 from './components/LoginFIDO2';

<LoginFIDO2 />
```

#### Integration with Authentication Flow

```javascript
function LoginPage() {
  const navigate = useNavigate();
  
  const handleLoginSuccess = () => {
    // Set authentication state
    localStorage.setItem('authenticated', 'true');
    navigate('/dashboard');
  };
  
  return (
    <div className="login-container">
      <h1>Welcome to EchoForge</h1>
      <LoginFIDO2 onSuccess={handleLoginSuccess} />
    </div>
  );
}
```

**Note**: The current implementation is a placeholder. For production FIDO2 authentication, see [Security Architecture](./security-architecture.md).

---

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# API Configuration
VITE_COINGECKO_API_URL=https://api.coingecko.com/api/v3
VITE_POLLING_INTERVAL=2500

# Security Settings
VITE_ENCRYPTION_ITERATIONS=600000
VITE_ENABLE_FIDO2=true

# Feature Flags
VITE_ENABLE_OFFLINE_MODE=true
VITE_ENABLE_AUDIO_ALERTS=true
```

### API Configuration

#### CoinGecko API Rate Limits

The free tier allows **50 calls per minute**. EchoForge's default configuration (2.5s polling) creates ~24 calls/minute, providing a safe margin.

#### Adjusting Polling Interval

```javascript
// Slower updates (reduce API calls)
<CryptoSparks pollingInterval={5000} />  // 12 calls/min

// Faster updates (increase API calls, monitor rate limits)
<CryptoSparks pollingInterval={1000} />  // 60 calls/min (at limit)
```

#### Custom API Endpoint

If using a CoinGecko Pro account or alternative API:

```javascript
// In hooks/useCryptoMomentum.js
const response = await axios.get(
  `${process.env.VITE_COINGECKO_API_URL}/coins/markets`,
  {
    headers: {
      'X-CG-Pro-API-Key': process.env.VITE_COINGECKO_API_KEY
    },
    // ... other config
  }
);
```

### Styling Customization

#### Using Custom Colors

The CryptoSparks component uses inline styles. To customize:

```javascript
// Create a themed version
import CryptoSparks from './components/CryptoSparks';

function ThemedCryptoSparks(props) {
  return (
    <div style={{
      background: 'linear-gradient(135deg, #667eea, #764ba2)',
      borderRadius: '16px',
      padding: '32px'
    }}>
      <CryptoSparks {...props} />
    </div>
  );
}
```

#### Using CSS Modules

1. Create a CSS module file:

```css
/* CryptoSparks.module.css */
.container {
  background: linear-gradient(135deg, #1a1a2e, #16213e);
  border-radius: 12px;
  padding: 24px;
  color: #fff;
}

.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.coin {
  background: rgba(255, 255, 255, 0.05);
  padding: 16px;
  border-radius: 8px;
  margin: 12px 0;
}
```

2. Import and use in your component.

---

## Troubleshooting

### Common Issues and Solutions

#### Issue: "Module not found: Can't resolve 'axios'"

**Solution**: Install axios dependency
```bash
npm install axios
```

#### Issue: "Network Error" or "API Rate Limit Exceeded"

**Solutions**:
1. Check your internet connection
2. Increase polling interval: `pollingInterval={5000}`
3. Wait 60 seconds for rate limit to reset
4. Consider upgrading to CoinGecko Pro API

#### Issue: CORS Error when Making API Requests

**Solution**: This typically occurs when running locally. The development server (Vite) should handle this automatically. If issues persist:

1. Verify you're using `npm run dev` (not opening index.html directly)
2. Check that your browser isn't blocking requests
3. Clear browser cache and cookies

#### Issue: WebAuthn/FIDO2 Not Working

**Solutions**:
1. Verify browser support (Chrome 67+, Firefox 60+, Safari 14+)
2. Ensure HTTPS is enabled (required for WebAuthn in production)
3. Check that your device has a compatible authenticator
4. For localhost development, some browsers require `localhost` not `127.0.0.1`

#### Issue: Components Not Rendering

**Solutions**:
1. Check console for errors: Open DevTools (F12) → Console tab
2. Verify all imports are correct
3. Ensure React and React DOM are installed:
   ```bash
   npm list react react-dom
   ```
4. Clear node_modules and reinstall:
   ```bash
   rm -rf node_modules
   npm install
   ```

#### Issue: Build Fails with "ENOSPC" Error

**Solution**: Increase file watcher limit (Linux)
```bash
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

### Debug Mode

Enable detailed logging:

```javascript
// In hooks/useCryptoMomentum.js
const fetchData = async () => {
  console.log('Fetching crypto data for:', symbols);
  try {
    const response = await axios.get(/* ... */);
    console.log('API Response:', response.data);
    // ... rest of code
  } catch (error) {
    console.error('Fetch error:', error.message);
  }
};
```

### Getting Help

If you're still experiencing issues:

1. **Check existing issues**: [GitHub Issues](https://github.com/ivan09069/EchoForge/issues)
2. **Ask in discussions**: [GitHub Discussions](https://github.com/ivan09069/EchoForge/discussions)
3. **Contact maintainer**: github0906@gmail.com

---

## Next Steps

### Security Hardening

- **Implement real FIDO2**: See [Security Architecture](./security-architecture.md)
- **Enable client-side encryption**: See encryption examples in security docs
- **Set up offline storage**: Implement IndexedDB for encrypted data storage

### Advanced Features

- **Multi-device sync**: End-to-end encrypted synchronization
- **Portfolio analytics**: Track performance over time
- **Tax optimization**: Automated wash sale detection and tax loss harvesting
- **DeFi integration**: Connect to Uniswap, Aave, and other protocols

### Deployment Options

#### Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel
```

#### Deploy to Netlify

```bash
# Build the project
npm run build

# Deploy the dist folder to Netlify
# Via Netlify CLI or drag-and-drop in web interface
```

#### Deploy to GitHub Pages

```bash
# Build the project
npm run build

# Deploy to gh-pages branch
npx gh-pages -d dist
```

### Further Reading

- **[RM²E Integration Guide](./rm2e-integration-guide.md)**: Deep dive into crypto momentum scoring
- **[Security Architecture](./security-architecture.md)**: Understanding zero-knowledge design
- **[Resilience Architecture](./resilience-architecture.md)**: System design and reliability
- **[API Documentation](./index.md)**: Complete component reference

---

## Summary

You now have everything you need to integrate EchoForge:

✅ **Installation**: Node.js setup, dependency installation, verification  
✅ **Integration**: Standalone app, React integration, or vanilla JS  
✅ **Components**: CryptoSparks, Dashboard, LoginFIDO2, and custom hooks  
✅ **Configuration**: API settings, polling intervals, styling customization  
✅ **Troubleshooting**: Common issues and solutions  
✅ **Next Steps**: Security hardening, advanced features, deployment

**Questions?** Open an issue or discussion on GitHub. We're here to help!

---

**Built with ❤️ by privacy advocates, for privacy advocates**

[⭐ Star on GitHub](https://github.com/ivan09069/EchoForge) • [📖 More Docs](./index.md) • [🐛 Report Issues](https://github.com/ivan09069/EchoForge/issues)
