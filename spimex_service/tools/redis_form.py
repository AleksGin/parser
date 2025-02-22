class RedisKeys:
    TRADING_DATE: str = "latest_trading_count:{}"
    DYNAMICS_KEY: str = "dynamics:{}:{}:{}:{}:{}"
    LAST_TRADE_DATA_KEY: str = "last_trades_result:{}:{}:{}"
