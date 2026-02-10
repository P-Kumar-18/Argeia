from app.pattern_detection import detect_pattern, Pattern_polarity_type, Pattern_strength_type

def test_single_delay_creates_unconfirmed_negative_pattern():
    signals = [
        {
            "delay_time": 5,
            "planned_duration": 120
        }
    ]

    pattern = detect_pattern(signals)

    assert pattern["polarity"] == Pattern_polarity_type.NEGATIVE
    assert pattern["confirmed"] is False


def test_mixed_signals_do_not_confirm_pattern():
    signals = [
        {"delay_time": 30, "planned_duration": 120},
        {"delay_time": 0, "planned_duration": 120}
    ]

    pattern = detect_pattern(signals)

    assert pattern["polarity"] == Pattern_polarity_type.NEGATIVE
    assert pattern["confirmed"] is False


def test_repeated_delays_confirm_negative_pattern():
    signals = [
        {"delay_time": 20, "planned_duration": 120},
        {"delay_time": 25, "planned_duration": 120},
        {"delay_time": 15, "planned_duration": 120},
        {"delay_time": 0, "planned_duration": 120}
    ]

    pattern = detect_pattern(signals)

    assert pattern["polarity"] == Pattern_polarity_type.NEGATIVE
    assert pattern["confirmed"] is True


# Strength thresholds are intentionally coarse and count-based.
def test_few_weak_signals_produce_low_strength_pattern():
    signals = [
        {"delay_time": 5, "planned_duration": 120},
        {"delay_time": 6, "planned_duration": 120},
        {"delay_time": 7, "planned_duration": 120},
        {"delay_time": 8, "planned_duration": 120},
        {"delay_time": 5, "planned_duration": 120},
        {"delay_time": 6, "planned_duration": 120},
        {"delay_time": 7, "planned_duration": 120},
        {"delay_time": 8, "planned_duration": 120}
    ]

    pattern = detect_pattern(signals)

    assert pattern["confirmed"] is True
    assert pattern["strength"] == Pattern_strength_type.LOW


def test_many_weak_signals_produce_high_strength_pattern():
    signals = [
        {"delay_time": 5, "planned_duration": 120},
        {"delay_time": 6, "planned_duration": 120},
        {"delay_time": 7, "planned_duration": 120},
        {"delay_time": 8, "planned_duration": 120},
        {"delay_time": 5, "planned_duration": 120},
        {"delay_time": 6, "planned_duration": 120},
        {"delay_time": 7, "planned_duration": 120},
        {"delay_time": 8, "planned_duration": 120},
        {"delay_time": 5, "planned_duration": 120},
        {"delay_time": 6, "planned_duration": 120},
        {"delay_time": 7, "planned_duration": 120},
        {"delay_time": 8, "planned_duration": 120}
    ]

    pattern = detect_pattern(signals)

    assert pattern["polarity"] == Pattern_polarity_type.NEGATIVE
    assert pattern["strength"] == Pattern_strength_type.HIGH
    assert pattern["confirmed"] is True 

def test_few_strong_signals_produce_high_strength_pattern():
    signals = [
        {"timeout_time": 120, "planned_duration": 120},
        {"delay_time": 70, "planned_duration": 120}
    ]

    pattern = detect_pattern(signals)

    assert pattern["confirmed"] is True
    assert pattern["strength"] == Pattern_strength_type.HIGH


def test_few_moderate_signals_produce_high_strength_pattern():
    signals = [
        {"delay_time": 20, "planned_duration": 120},
        {"delay_time": 15, "planned_duration": 120},
        {"delay_time": 23, "planned_duration": 120},
        {"delay_time": 20, "planned_duration": 120}
    ]

    pattern = detect_pattern(signals)

    assert pattern["confirmed"] is True
    assert pattern["strength"] == Pattern_strength_type.HIGH


# Single positive signals should not trigger recovery
def test_single_positive_signal_is_unconfirmed():
    signals = [
        {"delay_time": 0, "planned_duration": 120},
        {"underwork_time": 0, "planned_duration": 120}
    ]

    pattern = detect_pattern(signals)

    assert pattern["polarity"] == Pattern_polarity_type.POSITIVE
    assert pattern["confirmed"] is False