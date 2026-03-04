# coding=utf-8
"""
@Time : 2021/4/23 上午9:12
@Author : HeXW
"""
import pytest
from py.xml import html


@pytest.mark.optionalhook
def pytest_html_results_summary(prefix):
    prefix.extend([html.p("所属部门: NSY_测试部")])
    prefix.extend([html.p("开发维护人员: 测试组成员")])


def pytest_configure(config):
    # 添加接口地址与项目名称
    config._metadata["项目名称"] = "商品、供应链、运营"
    config._metadata["测试环境"] = 'http://localdev.xytask.uheixia.com'
    config._metadata['接口地址'] = 'https://98du.yuque.com/98du/puskgo/hn9szg'
    # 删除Java_Home
    config._metadata.pop("JAVA_HOME")
    config._metadata.pop("Packages")
    config._metadata.pop("Plugins")
    config._metadata.pop("Python")


# @pytest.mark.hookwrapperß
# def pytest_runtest_makereport(item):
#     outcome = yield
#     report = outcome.get_result()
#     getattr(report, 'extra', [])
#     report.nodeid = report.nodeid.encode("utf-8").decode("unicode_escape")  # 解决乱码

# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     report = outcome.get_result()
#     report.description = str(item.function.__doc__)
#     report.nodeid = report.nodeid.encode("utf-8").decode("unicode_escape")   #设置编码显示中文

@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.pop(-1)  # 删除link列


@pytest.mark.optionalhook
def pytest_html_results_table_row(cells):
    cells.pop(-1)  # 删除link列


def pytest_sessionstart(session):
    session.results = dict()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    if result.when == call:
        item.session.results[item] = result


def pytest_terminal_summary(terminalreporter):
    if 'passed' in terminalreporter.stats:
        print('passed amount:', len(terminalreporter.stats['passed']))
    if 'failed' in terminalreporter.stats:
        print('failed amount:', len(terminalreporter.stats['failed']))
    if 'xfailed' in terminalreporter.stats:
        print('xfailed amount:', len(terminalreporter.stats['xfailed']))
    if 'skipped' in terminalreporter.stats:
        print('skipped amount:', len(terminalreporter.stats['skipped']))


def pytest_addoption(parser):
    parser.addoption(
        "--eve",
        action="store",
        default="test",
        choices=["test", "uat"],
        help="test：表示测试环境, \
             uat：表示预发布环境, \
             默认test环境"
    )


@pytest.fixture(scope='session')
def get_cmdopts(request):
    if request.config.getoption("--eve"):
        return request.config.getoption("--eve")
