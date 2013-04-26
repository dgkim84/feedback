# -*- coding: utf-8 -*-
from attest import Tests, assert_hook

from feedback.commons.views import mod

from . import make_debug_app

tests = Tests()

app = make_debug_app()
app.register_blueprint(mod)

client = app.test_client()

@tests.test
def test_render_index():
  res = client.get('/')
  assert res.status_code == 200
  assert res.data == 'INDEX'

@tests.test
def test_render_projects():
  res = client.get('/projects')
  assert res.status_code == 200
  assert res.data == 'INDEX'

@tests.test
def test_render_projects():
  res = client.get('/tickets/new')
  assert res.status_code == 200
  assert res.data == 'INDEX'

@tests.test
def test_render_project_show_when_id_is_invalid():
  """project ID를 숫자가 아닌 문자로 했을 경우 404를 뱉어내는지 확인"""
  res = client.get('/projects/afe')
  assert res.status_code == 404

@tests.test
def test_render_project_show():
  res = client.get('/projects/1')
  assert res.status_code == 200
  assert res.data == 'INDEX'

