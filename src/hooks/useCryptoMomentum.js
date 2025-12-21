import { useState, useEffect } from 'react';

const FALLBACK_DATA = [
  { id: 'bitcoin', symbol: 'BTC', name: 'Bitcoin', current_price: 43250, price_change_percentage_24h: 2.5, image: 'https://assets.coingecko.com/coins/images/1/small/bitcoin.png' },
  { id: 'ethereum', symbol: 'ETH', name: 'Ethereum', current_price: 2280, price_change_percentage_24h: 1.8, image: 'https://assets.coingecko.com/coins/images/279/small/ethereum.png' }
];

export const useCryptoMomentum = () => {
  const [coins, setCoins] = useState(FALLBACK_DATA);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchWithTimeout = async (retries = 3) => {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 15000); // 15s timeout

      try {
        const response = await fetch(
          'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=20&sparkline=false',
          { signal: controller.signal }
        );
        
        clearTimeout(timeout);

        if (response.status === 429 && retries > 0) {
          await new Promise(r => setTimeout(r, 2000 * (4 - retries))); // Exponential backoff
          return fetchWithTimeout(retries - 1);
        }

        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        
        const data = await response.json();
        setCoins(data);
        setError(null);
      } catch (err) {
        clearTimeout(timeout);
        console.error('API error:', err);
        setError(err.message);
        setCoins(FALLBACK_DATA); // Use fallback on error
      } finally {
        setLoading(false);
      }
    };

    fetchWithTimeout();
  }, []);

  return { coins, loading, error };
};
