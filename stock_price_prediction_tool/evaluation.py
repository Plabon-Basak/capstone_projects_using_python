def backtest(prices, predictor_class):
    if len(prices) < 4:
        raise ValueError("At least four prices are required for backtesting")
    errors = []
    for end in range(3, len(prices)):
        prediction = predictor_class().fit(prices[:end]).predict_next()
        errors.append(abs(prices[end] - prediction))
    return {
        "mean_absolute_error": round(sum(errors) / len(errors), 2),
        "test_points": len(errors),
    }
