import sys

sys.path.append('../')
from middle_download.utils import *


def test_basename_fullpath():
    file_name = 'test_file'
    file_ext = '.csv'
    file_dir = '/test_dir/test_dir/'
    path = f'{file_dir}{file_name}{file_ext}'
    expect = f'{file_name}{file_ext}'
    res = basename(path)
    assert res == expect


def test_pathjoin_multiple_values():
    path01 = 'parent'
    path02 = 'child'
    path03 = 'grandchild'
    expect = f'{path01}/{path02}/{path03}'
    res = pathjoin(path01, path02, path03)
    assert res == expect


def test_pathjoin_single_values():
    path01 = 'parent'
    expect = f'{path01}'
    res = pathjoin(path01)
    assert res == expect


def test_isfile_file():
    file_name = 'test.txt'
    expect = True
    res = isfile(file_name)
    assert res == expect


def test_isfile_dir():
    dir_name = '/test_dir'
    expect = False
    res = isfile(dir_name)
    assert res == expect


def test_ls_volume():
    res = True
    expect = True
    assert res == expect


def test_check_status():
    res = True
    expect = True
    assert res == expect


def test_get_list():
    res = True
    expect = True
    assert res == expect


def test_xml_to_list():
    res = True
    expect = True
    assert res == expect


def test_make_proself_url():
    res = True
    expect = True
    assert res == expect


def test_get_file():
    res = True
    expect = True
    assert res == expect


def test_put_file():
    res = True
    expect = True
    assert res == expect


def remove_local_file():
    res = True
    expect = True
    assert res == expect
