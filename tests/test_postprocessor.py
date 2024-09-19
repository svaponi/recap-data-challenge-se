from app.postprocessor import postprocess


def test_postprocessor():
    data = [
        ((2023, 9), "client_1", 300.0),
        ((2023, 9), "client_2", 250.0),
        ((2023, 9), "client_3", 150.0),
        ((2023, 10), "client_2", 275.0),
    ]
    results = postprocess(data)

    results = sorted(results, key=lambda x: (x[0], x[1]))
    it = iter(results)
    assert next(it, None) == ((2023, 9), "client_1", 300.0, 0)
    assert next(it, None) == ((2023, 9), "client_2", 250.0, 0)
    assert next(it, None) == ((2023, 9), "client_3", 150.0, 0)
    assert next(it, None) == ((2023, 10), "client_1", 0, 300.0)
    assert next(it, None) == ((2023, 10), "client_2", 275.0, 0)
    assert next(it, None) == ((2023, 10), "client_3", 0, 150.0)
    assert next(it, None) is None


def test_postprocessor_case1():
    data = [
        ((2023, 1), "client_1", 190.0),
        ((2023, 9), "client_1", 300.0),
        ((2023, 9), "client_2", 250.0),
        ((2023, 9), "client_3", 150.0),
        ((2023, 10), "client_2", 275.0),
    ]
    results = postprocess(data)

    results = sorted(results, key=lambda x: (x[0], x[1]))
    it = iter(results)
    assert next(it, None) == ((2023, 1), "client_1", 190.0, 0)
    assert next(it, None) == ((2023, 2), "client_1", 0, 190.0)
    assert next(it, None) == ((2023, 9), "client_1", 300.0, 0)
    assert next(it, None) == ((2023, 9), "client_2", 250.0, 0)
    assert next(it, None) == ((2023, 9), "client_3", 150.0, 0)
    assert next(it, None) == ((2023, 10), "client_1", 0, 300.0)
    assert next(it, None) == ((2023, 10), "client_2", 275.0, 0)
    assert next(it, None) == ((2023, 10), "client_3", 0, 150.0)
    assert next(it, None) is None


def test_postprocessor_case2():
    data = [
        ((2023, 1), "client_1", 190.0),
        ((2023, 3), "client_1", -10.0),
        ((2023, 9), "client_1", 300.0),
        ((2023, 9), "client_2", 250.0),
        ((2023, 9), "client_3", 150.0),
        ((2023, 10), "client_2", 275.0),
    ]
    results = postprocess(data)

    results = sorted(results, key=lambda x: (x[0], x[1]))
    it = iter(results)
    assert next(it, None) == ((2023, 1), "client_1", 190.0, 0)
    assert next(it, None) == ((2023, 2), "client_1", 0, 190.0)
    assert next(it, None) == ((2023, 3), "client_1", -10.0, 0)
    assert next(it, None) == ((2023, 9), "client_1", 300.0, 0)
    assert next(it, None) == ((2023, 9), "client_2", 250.0, 0)
    assert next(it, None) == ((2023, 9), "client_3", 150.0, 0)
    assert next(it, None) == ((2023, 10), "client_1", 0, 300.0)
    assert next(it, None) == ((2023, 10), "client_2", 275.0, 0)
    assert next(it, None) == ((2023, 10), "client_3", 0, 150.0)
    assert next(it, None) is None
