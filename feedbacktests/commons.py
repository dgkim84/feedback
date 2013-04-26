from attest import assert_hook
from attest import Tests

from feedback.commons.utils import peek, decrease

import feedback

tests = Tests()

@tests.test
def test_peek():
  container = [1,2,3]
  assert peek(container) == 3

@tests.test
def test_peek_empty_container():
  container = []
  assert peek(container) == None
  assert peek(None) == None

@tests.test
def test_decrease():
  assert decrease(10, 1) == 9
  assert decrease(10) == 9
  assert decrease(10, 0.1) == 9.9
