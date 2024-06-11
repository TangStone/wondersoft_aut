# Created by gaojie at 2024-04-03
Feature: 用户同步模块
  用户管理 -> 用户同步管理 -> 用户同步模块 相关功能测试用例

  Background:
    Given 进入地址：/
    When 如果跳转到登录页面：${login_url}, 使用用户名：${login}，密码：${password}重新登录
    When 进入模块：用户管理
    And 进入二级菜单：用户同步管理 下的三级菜单：用户同步

  Scenario: 配置数据源
    Given 切换到标签页：数据源配置
    When 点击按钮：新增
    And 选择数据源类型：LDAP域
    And AD域参数配置: ${domain}
    And 点击按钮：测试
    Then 弹出提示框，显示提示信息：参数配置正确
    When 点击按钮：下一步
    And AD域数据关联
    And 点击按钮：提交
    Then 弹出提示框，显示提示信息：数据源添加成功

  Scenario: 新增同步配置
    Given 切换到标签页：同步配置
    When 点击按钮：新增
    And 设置同步配置参数：
        | 名称     | 数据源  | 同步模式 | 任务时间 | 错误阈值 | 日志保留周期 |
        | AD域同步 | 70.235 | 周期同步 | 周 星期一 00:00 | 10 | 30 |
    And 点击按钮：确认
    Then 弹出提示框，显示提示信息：同步配置成功！

  Scenario: 立即同步
    Given 点击按钮：立即同步
    When 选择同步配置名称：AD域同步
    And 点击按钮：确认

  Scenario: 用户同步-数据源配置-新增-LDAP域-账户统一后缀、组织统一后缀
    Given 切换到标签页：数据源配置
    When 点击按钮：新增
    And 选择数据源类型：LDAP域
    And AD域参数配置(基础配置+其它配置): ${domain}
      """
        {
          "数据源名称": "70.235-unified-suffix",
          "账号统一后缀": "account>ceshi*&测试",
          "组织统一后缀": "group>ceshi*&测试"
        }
      """
    And 点击按钮：测试
    Then 弹出提示框，显示提示信息：参数配置正确
    When 点击按钮：下一步
    And AD域数据关联(基础配置+其它配置):
      """
        {
          "上级领导人": ["输入数据源", "boss"],
          "上级领导人同步关联": "sid"
        }
      """
    And 点击按钮：提交
    Then 弹出提示框，显示提示信息：数据源添加成功
    Given 切换到标签页：同步配置
    When 点击按钮：新增
    And 设置同步配置参数：
        | 名称                    | 数据源                 | 同步模式 | 任务时间        | 错误阈值 | 日志保留周期 |
        | AD域同步-unified-suffix | 70.235-unified-suffix | 周期同步 | 周 星期一 00:00 | 10      | 30         |
    And 点击按钮：确认
    Then 弹出提示框，显示提示信息：同步配置成功！
    Given 点击按钮：立即同步
    When 选择同步配置名称：AD域同步-unified-suffix
    And 点击按钮：确认

  Scenario: 数据源配置查询
    Given 切换到标签页：数据源配置
    When 根据查询条件进行查询：
      """
        {
          "名称": "70.235-unified-suffix"
        }
      """
  Scenario Outline: 删除同步配置及数据源配置
    Given 切换到标签页：同步配置
    When 删除同步配置：<同步配置>
    Given 切换到标签页：数据源配置
    When 删除数据源配置：<数据源配置>
    Examples:
      | 同步配置                |   数据源配置             |
      | AD域同步                |  70.235                |
      | AD域同步-unified-suffix |  70.235-unified-suffix |
