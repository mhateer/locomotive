from flask import Flask, jsonify, request
import requests
from flask_cors import CORS 
from datetime import datetime
import pytz

app = Flask(__name__)
CORS(app)

BYBIT_BASE_URL = "https://api.bybit.com"
VALID_CATEGORIES = ["spot", "linear"]
API_TIMEOUT = 10

# Supported coins list
robinhood_coins = [
    "AAVEUSDT", "ALGOUSDT", "ADAUSDT", "ARBUSDT", "ATOMUSDT",
    "AVAXUSDT", "BCHUSDT", "BONKUSDT", "BTCUSDT", "COMPUSDT",
    "DOGEUSDT", "DOTUSDT", "EOSUSDT", "ETCUSDT", "ETHUSDT",
    "EURCUSDT", "FLOKIUSDT", "GRTUSDT", "HBARUSDT", "IMXUSDT",
    "JUPUSDT", "LDOUSDT", "LINKUSDT", "LTCUSDT", "MANAUSDT",
    "NEARUSDT", "ONDOUSDT", "OPUSDT", "PENGUUSDT", "PEPEUSDT",
    "POLUSDT", "RENDERUSDT", "SUSUSDT", "SANDUSDT", "SHIBUSDT",
    "SOLUSDT", "STRKUSDT", "TIAUSDT", "TONUSDT", "TRUMPUSDT",
    "UNIUSDT", "USDCUSDT", "WIFUSDT", "XLMUSDT", "WUSDT",
    "XTZUSDT", "XRPUSDT", "ZKUSDT", "ZROUSDT"
]

datasetA = [
    "1INCHUSDT", "ABBCUSDT", "ACHUSDT", "AGLDUSDT", "AIDOGEUSDT", "AKROUSDT", "ALICEUSDT",
    "ALPHAUSDT", "AMBUSDT", "ANKRUSDT", "ANTUSDT", "APEUSDT", "API3USDT", "APTUSDT", "ARKMUSDT", 
    "ARKUSDT", "ARPAUSDT", "ARUSDT", "ASTRAFERUSDT", "ASTRUSDT", "AUCTIONUSDT", "AUDIOUSDT", 
]
datasetB = [
    "AXSUSDT", "BABYDOGEUSDT", "BADGERUSDT", "BAKEUSDT", "BALUSDT", "BANDUSDT", "BARUSDT", "BATUSDT", 
    "BELUSDT", "BICOUSDT", "BIGTIMEUSDT", "BITUSDT", "BLURUSDT", "BLZUSDT", "BNTUSDT", "BNXUSDT", 
    "BOBAUSDT", "BONEUSDT", "BSVUSDT", "BTC3LUSDT", "BTC3SUSDT", "BTC5LUSDT", "BTC5SUSDT", "BTCUSDC", 
]
datasetC = [
    "BTTUSDT", "C98USDT", "CAKEUSDT", "CEEKUSDT", "CELRUSDT", "CFXUSDT", "CHZUSDT", "CITYUSDT", 
    "CKBUSDT", "CLVUSDT", "COCOSUSDT", "COMBOUSDT", "COREUSDT", "COTIUSDT", "CROUSDT", "CRVUSDT", 
    "CTCUSDT", "CVCUSDT", "CVPUSDT", "CVXUSDT", "CYBERUSDT", "DARUSDT", "DASHUSDT", "DENTUSDT", 
]
datasetD = [
    "DEPUSDT", "DEXEUSDT", "DFUSDT", "DGBUSDT", "DIAUSDT", "DUSKUSDT", "DYDXUSDT", "EDUUSDT", "EGLDUSDT", 
    "ELFUSDT", "ENJUSDT", "ENSUSDT", "ERNUSDT", "ETH3LUSDT", "ETH3SUSDT", "ETH5LUSDT", "ETH5SUSDT", 
    "ETHUSDC", "FETUSDT", "FILUSDT", "FLOWUSDT", "FLRUSDT", "FORTHUSDT", "FRONTUSDT", "FTMUSDT", "FTTUSDT", 
]
datasetE = [
    "FXSUSDT", "GALAUSDT", "GALUSDT", "GMXUSDT", "GNSUSDT", "GTCUSDT", "HFTUSDT", "HIGHUSDT", "HNTUSDT", 
    "HOOKUSDT", "HOTUSDT", "ICPUSDT", "ICXUSDT", "IDEXUSDT", "IDUSDT", "ILVUSDT", "INJUSDT", "IOSTUSDT", 
    "IOTAUSDT", "IOTXUSDT", "JASMYUSDT", "JOEUSDT", "JSTUSDT", "KASUSDT", "KAVAUSDT", "KDAUSDT", "KLAYUSDT", 
]
datasetF = [
    "KNCUSDT", "KSMUSDT", "LEOUSDT", "LINAUSDT", "LITUSDT", "LOOKSUSDT", "LOOMUSDT", "LPTUSDT", "LQTYUSDT", 
    "LRCUSDT", "LSKUSDT", "LUNAUSDT", "LUNCUSDT", "MAGICUSDT", "MASKUSDT", "MATICUSDT", "MAVIAUSDT", "MAVUSDT", 
    "MBLUSDT", "MBOXUSDT", "MCUSDT", "MDTUSDT", "MEMEUSDT", "METISUSDT", "MINAUSDT", "MKRUSDT", "MLNUSDT", 
]
datasetG = [
    "MOVRUSDT", "MTLUSDT", "MULTIUSDT", "NACUSDT", "NEOUSDT", "NKNUSDT", "NMRUSDT", "NTRNUSDT", "OCEANUSDT", 
    "OGNUSDT", "OGUSDT", "OKBUSDT", "OMUSDT", "ONEUSDT", "ONGUSDT", "ONTUSDT", "ORDIUSDT", "OSMOUSDT", 
    "PAXGUSDT", "PERPUSDT", "PHAUSDT", "PLAUSDT", "PNTUSDT", "POLYXUSDT", "PONDUSDT", "PORTALUSDT", "POWRUSDT",
]
datasetH = [
    "PRIMEUSDT", "PROMUSDT", "PSGUSDT", "PUNDIXUSDT", "PYRUSDT", "QIUSDT", "QNTUSDT", "QTUMUSDT", "RADUSDT", 
    "RAREUSDT", "RDNTUSDT", "REEFUSDT", "REIUSDT", "RENUSDT", "REQUSDT", "RLCUSDT", "RNDRUSDT", "ROSEUSDT", 
    "RPLUSDT", "RSRUSDT", "RSS3USDT", "RUNEUSDT", "RVNUSDT", "SANTOSUSDT", "SFPUSDT", "SHIB1000USDT", "SKLUSDT", 
]
datasetI = [
    "SLPUSDT", "SNXUSDT", "SOLUSDC", "SPELLUSDT", "SSVUSDT", "STEEMUSDT", "STGUSDT", "STORJUSDT", "STPTUSDT", 
    "STRAXUSDT", "STXUSDT", "SUIUSDT", "SUNUSDT", "SUPERUSDT", "SUSHIUSDT", "SWEATUSDT", "SXPUSDT", "SYSUSDT", 
    "TAOUSDT", "TAPTUSDT", "TCRVUSDT", "TFUELUSDT", "THETAUSDT", "TLMUSDT", "TLOSUSDT", "TOMIUSDT", "TOMOUSDT",
]
datasetJ = [
    "TORNUSDT", "TRBUSDT", "TRUUSDT", "TRXUSDT", "TUSDUSDT", "TVKUSDT", "TWTUSDT", "UMAUSDT", "UNFIUSDT", 
    "USDDUSDT", "USTCUSDT", "UTKUSDT", "VANRYUSDT", "VELOUSDT", "VETUSDT", "VOXELUSDT", "WAVESUSDT", "WAXPUSDT", 
    "WEMIXUSDT", "WINGUSDT", "WLDUSDT", "WLKNUSDT", "WOOUSDT", "XAUTUSDT", "XCHUSDT", "XCNUSDT", "XEMUSDT", 
]
datasetK = [
    "XMRUSDT", "XNOUSDT", "XRDUSDT", "XRPUSDC", "XVGUSDT", "XVSUSDT", "YFIUSDT", "YGGUSDT", 
    "ZBCUSDT", "ZECUSDT", "ZENUSDT", "ZILUSDT", "ZRXUSDT"
]

# Combine all coins
all_coins = robinhood_coins + datasetA

def get_utc_minus_5_timestamps(selected_date=None):
    tz = pytz.timezone('America/New_York')
    if selected_date:
        date_obj = datetime.strptime(selected_date, '%Y-%m-%d').replace(tzinfo=tz)
    else:
        date_obj = datetime.now(tz)
    
    start = date_obj.replace(hour=0, minute=1, second=0, microsecond=0)
    end = date_obj.replace(hour=23, minute=59, second=59, microsecond=0)
    return int(start.timestamp()), int(end.timestamp())

def fetch_available_symbols():
    """Fetch valid symbols using Bybit v5 API"""
    symbols = {}
    try:
        response = requests.get(
            f"{BYBIT_BASE_URL}/v5/market/instruments-info",
            params={"category": "spot"},
            timeout=API_TIMEOUT
        )
        response.raise_for_status()
        data = response.json()
        
        if data.get("retCode") == 0 and data["result"].get("list"):
            for item in data["result"]["list"]:
                symbol = item["symbol"]
                symbols[symbol] = None  # No longer storing launch date
    except Exception as e:
        print(f"Error fetching symbols: {str(e)}")
    return symbols

def fetch_current_price(symbol):
    """Fetch current price with automatic category detection"""
    for category in VALID_CATEGORIES:
        try:
            response = requests.get(
                f"{BYBIT_BASE_URL}/v5/market/tickers",
                params={"category": category, "symbol": symbol},
                timeout=API_TIMEOUT
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("retCode") == 0 and data["result"]["list"]:
                return float(data["result"]["list"][0]["lastPrice"])
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 10002:  # Invalid symbol error
                continue
            print(f"HTTP error ({category}): {str(e)}")
        except Exception as e:
            print(f"Error fetching {symbol} price: {str(e)}")
    return None

def fetch_bybit_data(symbol, selected_date=None):
    """Fetch historical data with enhanced error handling"""
    start_ts, end_ts = get_utc_minus_5_timestamps(selected_date)
    try:
        response = requests.get(
            f"{BYBIT_BASE_URL}/v5/market/kline",
            params={
                "category": "spot",
                "symbol": symbol,
                "interval": "1",
                "start": start_ts * 1000,
                "end": end_ts * 1000,
                "limit": 1440
            },
            timeout=API_TIMEOUT
        )
        response.raise_for_status()
        data = response.json()
        
        if data.get("retCode") == 0 and data["result"].get("list"):
            return data["result"]["list"]
        print(f"API error: {data.get('retMsg', 'Unknown error')}")
    except Exception as e:
        print(f"Failed to fetch {symbol} data: {str(e)}")
    return None

def analyze_data(data):
    """Enhanced data analysis with validation"""
    if not data or not isinstance(data, list) or len(data) < 1:
        return (None,)*5
    
    try:
        # Extracting the necessary values
        start_price = float(data[0][1])  # Opening price of the first candle
        end_price = float(data[-1][4])    # Closing price of the last candle
        prices = [float(entry[4]) for entry in data if len(entry) > 4]  # Closing prices for fluctuation calculation
        high = max(prices)
        low = min(prices)
        fluctuation = round(((high - low) / low) * 100, 4) if low != 0 else 0
        return start_price, end_price, high, low, fluctuation
    except (IndexError, ValueError) as e:
        print(f"Data analysis error: {str(e)}")
        return (None,)*5

@app.route('/api/crypto-dataA', methods=['GET'])
def get_crypto_dataA():
    """Fetch data for dataset A"""
    selected_date = request.args.get('date')
    valid_symbols = fetch_available_symbols()
    
    # Validate requested symbols based on Bybit's available symbols
    filtered_coins = [coin for coin in all_coins if coin in valid_symbols]

    result_data = []
    now = datetime.now(pytz.timezone('America/New_York'))
    
    for index, coin in enumerate(filtered_coins, 1):
        historical_data = fetch_bybit_data(coin, selected_date)
        analysis = analyze_data(historical_data)
        current_price = fetch_current_price(coin)

        result_data.append({
            "number": index,
            "coin": coin,
            "rb": "🟢" if coin in robinhood_coins else " ",
            "start_price": analysis[0],
            "highest_price": analysis[2],
            "lowest_price": analysis[3],
            "end_price": analysis[1],
            "fluctuation": analysis[4],
            "cp_bb": current_price,
        })

    # Sorting logic
    sort_key = 'coin' if (selected_date == now.strftime('%Y-%m-%d')) else 'fluctuation'
    reverse = False if sort_key == 'coin' else True

    # Custom sorting for 'rb' column
    if sort_key == 'rb':
        result_data.sort(key=lambda x: (x['rb'] == " ", x[sort_key]), reverse=reverse)
    else:
        result_data.sort(key=lambda x: x[sort_key] if x[sort_key] is not None else float('inf'), reverse=reverse)

    return jsonify({
        "date_fetched": now.strftime('%I:%M %p'),
        "data": result_data
    })

@app.route('/api/crypto-dataB', methods=['GET'])
def get_crypto_dataB():
    """Fetch data for dataset B"""
    selected_date = request.args.get('date')
    valid_symbols = fetch_available_symbols()
    
    # Validate requested symbols based on Bybit's available symbols
    filtered_coins = [coin for coin in datasetB if coin in valid_symbols]

    result_data = []
    now = datetime.now(pytz.timezone('America/New_York'))
    
    for index, coin in enumerate(filtered_coins, 1):
        historical_data = fetch_bybit_data(coin, selected_date)
        analysis = analyze_data(historical_data)
        current_price = fetch_current_price(coin)

        result_data.append({
            "number": index,
            "coin": coin,
            "rb": "🟢" if coin in robinhood_coins else " ",
            "start_price": analysis[0],
            "highest_price": analysis[2],
            "lowest_price": analysis[3],
            "end_price": analysis[1],
            "fluctuation": analysis[4],
            "cp_bb": current_price,
        })

    # Sorting logic
    sort_key = 'coin' if (selected_date == now.strftime('%Y-%m-%d')) else 'fluctuation'
    reverse = False if sort_key == 'coin' else True

    # Custom sorting for 'rb' column
    if sort_key == 'rb':
        result_data.sort(key=lambda x: (x['rb'] == " ", x[sort_key]), reverse=reverse)
    else:
        result_data.sort(key=lambda x: x[sort_key] if x[sort_key] is not None else float('inf'), reverse=reverse)

    return jsonify({
        "date_fetched": now.strftime('%I:%M %p'),
        "data": result_data
    })

@app.route('/api/crypto-dataC', methods=['GET'])
def get_crypto_dataC():
    """Fetch data for dataset C"""
    selected_date = request.args.get('date')
    valid_symbols = fetch_available_symbols()
    
    # Validate requested symbols based on Bybit's available symbols
    filtered_coins = [coin for coin in datasetC if coin in valid_symbols]

    result_data = []
    now = datetime.now(pytz.timezone('America/New_York'))
    
    for index, coin in enumerate(filtered_coins, 1):
        historical_data = fetch_bybit_data(coin, selected_date)
        analysis = analyze_data(historical_data)
        current_price = fetch_current_price(coin)

        result_data.append({
            "number": index,
            "coin": coin,
            "rb": "🟢" if coin in robinhood_coins else " ",
            "start_price": analysis[0],
            "highest_price": analysis[2],
            "lowest_price": analysis[3],
            "end_price": analysis[1],
            "fluctuation": analysis[4],
            "cp_bb": current_price,
        })

    # Sorting logic
    sort_key = 'coin' if (selected_date == now.strftime('%Y-%m-%d')) else 'fluctuation'
    reverse = False if sort_key == 'coin' else True

    # Custom sorting for 'rb' column
    if sort_key == 'rb':
        result_data.sort(key=lambda x: (x['rb'] == " ", x[sort_key]), reverse=reverse)
    else:
        result_data.sort(key=lambda x: x[sort_key] if x[sort_key] is not None else float('inf'), reverse=reverse)

    return jsonify({
        "date_fetched": now.strftime('%I:%M %p'),
        "data": result_data
    })

@app.route('/api/crypto-dataD', methods=['GET'])
def get_crypto_dataD():
    """Fetch data for dataset D"""
    selected_date = request.args.get('date')
    valid_symbols = fetch_available_symbols()
    
    # Validate requested symbols based on Bybit's available symbols
    filtered_coins = [coin for coin in datasetD if coin in valid_symbols]

    result_data = []
    now = datetime.now(pytz.timezone('America/New_York'))
    
    for index, coin in enumerate(filtered_coins, 1):
        historical_data = fetch_bybit_data(coin, selected_date)
        analysis = analyze_data(historical_data)
        current_price = fetch_current_price(coin)

        result_data.append({
            "number": index,
            "coin": coin,
            "rb": "🟢" if coin in robinhood_coins else " ",
            "start_price": analysis[0],
            "highest_price": analysis[2],
            "lowest_price": analysis[3],
            "end_price": analysis[1],
            "fluctuation": analysis[4],
            "cp_bb": current_price,
        })

    # Sorting logic
    sort_key = 'coin' if (selected_date == now.strftime('%Y-%m-%d')) else 'fluctuation'
    reverse = False if sort_key == 'coin' else True

    # Custom sorting for 'rb' column
    if sort_key == 'rb':
        result_data.sort(key=lambda x: (x['rb'] == " ", x[sort_key]), reverse=reverse)
    else:
        result_data.sort(key=lambda x: x[sort_key] if x[sort_key] is not None else float('inf'), reverse=reverse)

    return jsonify({
        "date_fetched": now.strftime('%I:%M %p'),
        "data": result_data
    })

@app.route('/api/crypto-dataE', methods=['GET'])
def get_crypto_dataE():
    """Fetch data for dataset E"""
    selected_date = request.args.get('date')
    valid_symbols = fetch_available_symbols()
    
    # Validate requested symbols based on Bybit's available symbols
    filtered_coins = [coin for coin in datasetE if coin in valid_symbols]

    result_data = []
    now = datetime.now(pytz.timezone('America/New_York'))
    
    for index, coin in enumerate(filtered_coins, 1):
        historical_data = fetch_bybit_data(coin, selected_date)
        analysis = analyze_data(historical_data)
        current_price = fetch_current_price(coin)

        result_data.append({
            "number": index,
            "coin": coin,
            "rb": "🟢" if coin in robinhood_coins else " ",
            "start_price": analysis[0],
            "highest_price": analysis[2],
            "lowest_price": analysis[3],
            "end_price": analysis[1],
            "fluctuation": analysis[4],
            "cp_bb": current_price,
        })

    # Sorting logic
    sort_key = 'coin' if (selected_date == now.strftime('%Y-%m-%d')) else 'fluctuation'
    reverse = False if sort_key == 'coin' else True

    # Custom sorting for 'rb' column
    if sort_key == 'rb':
        result_data.sort(key=lambda x: (x['rb'] == " ", x[sort_key]), reverse=reverse)
    else:
        result_data.sort(key=lambda x: x[sort_key] if x[sort_key] is not None else float('inf'), reverse=reverse)

    return jsonify({
        "date_fetched": now.strftime('%I:%M %p'),
        "data": result_data
    })

@app.route('/api/crypto-dataF', methods=['GET'])
def get_crypto_dataF():
    """Fetch data for dataset F"""
    selected_date = request.args.get('date')
    valid_symbols = fetch_available_symbols()
    
    # Validate requested symbols based on Bybit's available symbols
    filtered_coins = [coin for coin in datasetF if coin in valid_symbols]

    result_data = []
    now = datetime.now(pytz.timezone('America/New_York'))
    
    for index, coin in enumerate(filtered_coins, 1):
        historical_data = fetch_bybit_data(coin, selected_date)
        analysis = analyze_data(historical_data)
        current_price = fetch_current_price(coin)

        result_data.append({
            "number": index,
            "coin": coin,
            "rb": "🟢" if coin in robinhood_coins else " ",
            "start_price": analysis[0],
            "highest_price": analysis[2],
            "lowest_price": analysis[3],
            "end_price": analysis[1],
            "fluctuation": analysis[4],
            "cp_bb": current_price,
        })

    # Sorting logic
    sort_key = 'coin' if (selected_date == now.strftime('%Y-%m-%d')) else 'fluctuation'
    reverse = False if sort_key == 'coin' else True

    # Custom sorting for 'rb' column
    if sort_key == 'rb':
        result_data.sort(key=lambda x: (x['rb'] == " ", x[sort_key]), reverse=reverse)
    else:
        result_data.sort(key=lambda x: x[sort_key] if x[sort_key] is not None else float('inf'), reverse=reverse)

    return jsonify({
        "date_fetched": now.strftime('%I:%M %p'),
        "data": result_data
    })

@app.route('/api/crypto-dataG', methods=['GET'])
def get_crypto_dataG():
    """Fetch data for dataset G"""
    selected_date = request.args.get('date')
    valid_symbols = fetch_available_symbols()
    
    # Validate requested symbols based on Bybit's available symbols
    filtered_coins = [coin for coin in datasetG if coin in valid_symbols]

    result_data = []
    now = datetime.now(pytz.timezone('America/New_York'))
    
    for index, coin in enumerate(filtered_coins, 1):
        historical_data = fetch_bybit_data(coin, selected_date)
        analysis = analyze_data(historical_data)
        current_price = fetch_current_price(coin)

        result_data.append({
            "number": index,
            "coin": coin,
            "rb": "🟢" if coin in robinhood_coins else " ",
            "start_price": analysis[0],
            "highest_price": analysis[2],
            "lowest_price": analysis[3],
            "end_price": analysis[1],
            "fluctuation": analysis[4],
            "cp_bb": current_price,
        })

    # Sorting logic
    sort_key = 'coin' if (selected_date == now.strftime('%Y-%m-%d')) else 'fluctuation'
    reverse = False if sort_key == 'coin' else True

    # Custom sorting for 'rb' column
    if sort_key == 'rb':
        result_data.sort(key=lambda x: (x['rb'] == " ", x[sort_key]), reverse=reverse)
    else:
        result_data.sort(key=lambda x: x[sort_key] if x[sort_key] is not None else float('inf'), reverse=reverse)

    return jsonify({
        "date_fetched": now.strftime('%I:%M %p'),
        "data": result_data
    })

@app.route('/api/crypto-dataH', methods=['GET'])
def get_crypto_dataH():
    """Fetch data for dataset H"""
    selected_date = request.args.get('date')
    valid_symbols = fetch_available_symbols()
    
    # Validate requested symbols based on Bybit's available symbols
    filtered_coins = [coin for coin in datasetH if coin in valid_symbols]

    result_data = []
    now = datetime.now(pytz.timezone('America/New_York'))
    
    for index, coin in enumerate(filtered_coins, 1):
        historical_data = fetch_bybit_data(coin, selected_date)
        analysis = analyze_data(historical_data)
        current_price = fetch_current_price(coin)

        result_data.append({
            "number": index,
            "coin": coin,
            "rb": "🟢" if coin in robinhood_coins else " ",
            "start_price": analysis[0],
            "highest_price": analysis[2],
            "lowest_price": analysis[3],
            "end_price": analysis[1],
            "fluctuation": analysis[4],
            "cp_bb": current_price,
        })

    # Sorting logic
    sort_key = 'coin' if (selected_date == now.strftime('%Y-%m-%d')) else 'fluctuation'
    reverse = False if sort_key == 'coin' else True

    # Custom sorting for 'rb' column
    if sort_key == 'rb':
        result_data.sort(key=lambda x: (x['rb'] == " ", x[sort_key]), reverse=reverse)
    else:
        result_data.sort(key=lambda x: x[sort_key] if x[sort_key] is not None else float('inf'), reverse=reverse)

    return jsonify({
        "date_fetched": now.strftime('%I:%M %p'),
        "data": result_data
    })

@app.route('/api/crypto-dataI', methods=['GET'])
def get_crypto_dataI():
    """Fetch data for dataset I"""
    selected_date = request.args.get('date')
    valid_symbols = fetch_available_symbols()
    
    # Validate requested symbols based on Bybit's available symbols
    filtered_coins = [coin for coin in datasetI if coin in valid_symbols]

    result_data = []
    now = datetime.now(pytz.timezone('America/New_York'))
    
    for index, coin in enumerate(filtered_coins, 1):
        historical_data = fetch_bybit_data(coin, selected_date)
        analysis = analyze_data(historical_data)
        current_price = fetch_current_price(coin)

        result_data.append({
            "number": index,
            "coin": coin,
            "rb": "🟢" if coin in robinhood_coins else " ",
            "start_price": analysis[0],
            "highest_price": analysis[2],
            "lowest_price": analysis[3],
            "end_price": analysis[1],
            "fluctuation": analysis[4],
            "cp_bb": current_price,
        })

    # Sorting logic
    sort_key = 'coin' if (selected_date == now.strftime('%Y-%m-%d')) else 'fluctuation'
    reverse = False if sort_key == 'coin' else True

    # Custom sorting for 'rb' column
    if sort_key == 'rb':
        result_data.sort(key=lambda x: (x['rb'] == " ", x[sort_key]), reverse=reverse)
    else:
        result_data.sort(key=lambda x: x[sort_key] if x[sort_key] is not None else float('inf'), reverse=reverse)

    return jsonify({
        "date_fetched": now.strftime('%I:%M %p'),
        "data": result_data
    })

@app.route('/api/crypto-dataJ', methods=['GET'])
def get_crypto_dataJ():
    """Fetch data for dataset J"""
    selected_date = request.args.get('date')
    valid_symbols = fetch_available_symbols()
    
    # Validate requested symbols based on Bybit's available symbols
    filtered_coins = [coin for coin in datasetJ if coin in valid_symbols]

    result_data = []
    now = datetime.now(pytz.timezone('America/New_York'))
    
    for index, coin in enumerate(filtered_coins, 1):
        historical_data = fetch_bybit_data(coin, selected_date)
        analysis = analyze_data(historical_data)
        current_price = fetch_current_price(coin)

        result_data.append({
            "number": index,
            "coin": coin,
            "rb": "🟢" if coin in robinhood_coins else " ",
            "start_price": analysis[0],
            "highest_price": analysis[2],
            "lowest_price": analysis[3],
            "end_price": analysis[1],
            "fluctuation": analysis[4],
            "cp_bb": current_price,
        })

    # Sorting logic
    sort_key = 'coin' if (selected_date == now.strftime('%Y-%m-%d')) else 'fluctuation'
    reverse = False if sort_key == 'coin' else True

    # Custom sorting for 'rb' column
    if sort_key == 'rb':
        result_data.sort(key=lambda x: (x['rb'] == " ", x[sort_key]), reverse=reverse)
    else:
        result_data.sort(key=lambda x: x[sort_key] if x[sort_key] is not None else float('inf'), reverse=reverse)

    return jsonify({
        "date_fetched": now.strftime('%I:%M %p'),
        "data": result_data
    })

@app.route('/api/crypto-dataK', methods=['GET'])
def get_crypto_dataK():
    """Fetch data for dataset K"""
    selected_date = request.args.get('date')
    valid_symbols = fetch_available_symbols()
    
    # Validate requested symbols based on Bybit's available symbols
    filtered_coins = [coin for coin in datasetK if coin in valid_symbols]

    result_data = []
    now = datetime.now(pytz.timezone('America/New_York'))
    
    for index, coin in enumerate(filtered_coins, 1):
        historical_data = fetch_bybit_data(coin, selected_date)
        analysis = analyze_data(historical_data)
        current_price = fetch_current_price(coin)

        result_data.append({
            "number": index,
            "coin": coin,
            "rb": "🟢" if coin in robinhood_coins else " ",
            "start_price": analysis[0],
            "highest_price": analysis[2],
            "lowest_price": analysis[3],
            "end_price": analysis[1],
            "fluctuation": analysis[4],
            "cp_bb": current_price,
        })

    # Sorting logic
    sort_key = 'coin' if (selected_date == now.strftime('%Y-%m-%d')) else 'fluctuation'
    reverse = False if sort_key == 'coin' else True

    # Custom sorting for 'rb' column
    if sort_key == 'rb':
        result_data.sort(key=lambda x: (x['rb'] == " ", x[sort_key]), reverse=reverse)
    else:
        result_data.sort(key=lambda x: x[sort_key] if x[sort_key] is not None else float('inf'), reverse=reverse)

    return jsonify({
        "date_fetched": now.strftime('%I:%M %p'),
        "data": result_data
    })
@app.route('/api/crypto-data-all', methods=['GET'])
def get_crypto_data_all():
    """Fetch data for all datasets A, B, C, D, E, F, G, H, I, J, K"""
    selected_date = request.args.get('date')
    valid_symbols = fetch_available_symbols()

    all_datasets = {
        "datasetA": datasetA,
        "datasetB": datasetB,
        "datasetC": datasetC,
        "datasetD": datasetD,
        "datasetE": datasetE,
        "datasetF": datasetF,
        "datasetG": datasetG,
        "datasetH": datasetH,
        "datasetI": datasetI,
        "datasetJ": datasetJ,
        "datasetK": datasetK,
    }

    result_data = {}
    now = datetime.now(pytz.timezone('America/New_York'))

    for dataset_name, coins in all_datasets.items():
        filtered_coins = [coin for coin in coins if coin in valid_symbols]
        dataset_results = []

        for index, coin in enumerate(filtered_coins, 1):
            historical_data = fetch_bybit_data(coin, selected_date)
            analysis = analyze_data(historical_data)
            current_price = fetch_current_price(coin)

            dataset_results.append({
                "number": index,
                "coin": coin,
                "rb": "🟢" if coin in robinhood_coins else " ",
                "start_price": analysis[0],
                "highest_price": analysis[2],
                "lowest_price": analysis[3],
                "end_price": analysis[1],
                "fluctuation": analysis[4],
                "cp_bb": current_price,
            })

        # Sorting logic
        sort_key = 'coin' if (selected_date == now.strftime('%Y-%m-%d')) else 'fluctuation'
        reverse = False if sort_key == 'coin' else True

        # Custom sorting for 'rb' column
        if sort_key == 'rb':
            dataset_results.sort(key=lambda x: (x['rb'] == " ", x[sort_key]), reverse=reverse)
        else:
            dataset_results.sort(key=lambda x: x[sort_key] if x[sort_key] is not None else float('inf'), reverse=reverse)

        result_data[dataset_name] = dataset_results

    return jsonify({
        "date_fetched": now.strftime('%I:%M %p'),
        "data": result_data
    })


if __name__ == '__main__':
    app.run(debug=True)
