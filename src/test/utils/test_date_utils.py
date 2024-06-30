import pytest
from dateutil import parser
from datetime import datetime
import pytz

from utils.date_utils import parse_date_with_timezone


def test_parse_date_with_timezone():
    date_string_cst = "Fri, 21 Jul 2023 09:04 CST"
    parsed_date_cst = parse_date_with_timezone(date_string_cst)
    expected_date_cst = datetime(2023, 7, 21, 9, 4, tzinfo=pytz.timezone('America/Chicago'))
    assert parsed_date_cst == expected_date_cst

    date_string_edt = "Fri, 21 Jul 2023 09:04 EDT"
    parsed_date_edt = parse_date_with_timezone(date_string_edt)
    expected_date_edt = datetime(2023, 7, 21, 9, 4, tzinfo=pytz.timezone('America/New_York'))
    assert parsed_date_edt == expected_date_edt

    date_string_invalid = "test"
    with pytest.raises(parser.ParserError):
        parse_date_with_timezone(date_string_invalid)
