import requests
import numpy as np
import matplotlib.pyplot as plt


def get_candlestick_data(symbol, interval, limit):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Bir hata oluştu:", response.text)
        return None

def calculate_average_prices(weekly_open_prices, weekly_close_prices, weekly_high_prices, weekly_low_prices, daily_close_prices):
    avgPrice = []
    avgPrice2 = []
    week_index = 0
    for i in range(len(daily_close_prices)):
        if i % 7 == 0:
            week_high = weekly_high_prices[week_index]
            week_low = weekly_low_prices[week_index]
            avg_price = (week_high + week_low) / 2
            avgPrice.extend([avg_price] * 7)

            week_open = weekly_open_prices[week_index]
            if week_index < len(weekly_close_prices):
                week_close = weekly_close_prices[week_index]
                avg_price2 = (week_open + week_close + week_high + week_low) / 4
                avgPrice2.extend([avg_price2] * 7)
            week_index += 1
    return avgPrice, avgPrice2

if __name__ == "__main__":
    symbol = "BTCUSDT"
    num_days = 365  # Son bir yıl içindeki günlük veri sayısı

    # Günlük verileri al
    candlestick_data = get_candlestick_data(symbol, '1d', num_days)

    if candlestick_data:
        daily_close_prices = [float(candle[4]) for candle in candlestick_data]  # Günlük kapanış fiyatlarını al

        # Haftalık verileri al
        weekly_open_prices = [float(candle[1]) for candle in candlestick_data[::7]]  # Haftalık açılış fiyatlarını al
        weekly_high_prices = [max(float(candle[2]) for candle in candlestick_data[i:i+7]) for i in range(0, len(candlestick_data), 7)]  # Haftalık en yüksek fiyatları al
        weekly_low_prices = [min(float(candle[3]) for candle in candlestick_data[i:i+7]) for i in range(0, len(candlestick_data), 7)]  # Haftalık en düşük fiyatları al
        weekly_close_prices = [float(candle[4]) for candle in candlestick_data[6::7]]  # Haftalık kapanış fiyatlarını al

        # Ortalama fiyatları hesapla
        avgPrice, avgPrice2 = calculate_average_prices(weekly_open_prices, weekly_close_prices, weekly_high_prices, weekly_low_prices, daily_close_prices)

        # BTC fiyat verisini al
        btc_prices = [float(candle[4]) for candle in candlestick_data]

        # Grafik çizimi
        plt.plot(btc_prices, label='BTC Price', color='blue')
        plt.plot(avgPrice, label='Average Zone Price', color='orange')
        plt.plot(avgPrice2, label='Average Zone Price 2', color='red')

        # Grafik ayarları
        plt.xlabel('Day')
        plt.ylabel('Price')
        plt.title('BTC Price vs Average Zone Prices')
        plt.legend()

        # Grafiği göster
        plt.show()
    else:
        print("Veri alınamadı. Lütfen bağlantınızı kontrol edin.")
