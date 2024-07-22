#!/usr/bin/env python3

"""
Python script that contains function named index_range
that takes two integer arguments page and page_size
Function returns a tuple of size two containing a start index
and an end index corresponding to the range of indexes to
return in a list for those particular pagination parameters
"""

from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Returns a tuple containing the start index and end index for pagination
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return (start_index, end_index)
