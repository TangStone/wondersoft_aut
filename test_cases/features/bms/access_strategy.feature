# Created by gaojie at 2024-04-23
Feature: 管理员登录限制模块
  用户管理 -> 权限管理 -> 管理员登录限制模块 相关功能测试用例

  Background:
    Given 进入地址：/
    When 如果跳转到登录页面：${login_url}, 使用用户名：${login}，密码：${password}重新登录
    When 进入模块：用户管理
    And 进入二级菜单：权限管理 下的三级菜单：管理员登录限制

  Scenario: 管理员登录限制-录入限制范围-录入ip
    Given 点击按钮：新增
    When 录入限制信息：
      """
      {
          "类型": "ip",
          "ip": "192.168.154.31"
      }
      """
    And 点击按钮：确定
    Then 弹出提示框，显示提示信息：新增成功
    When 全局控制：开启

  Scenario: 限制策略查询
    When 根据查询条件进行限制策略列表查询：
      """
        {
          "IP地址": "192.168.1.1"
        }
      """

  Scenario Outline: 删除限制
    When 删除限制：<限制范围>
    Examples:
      | 限制范围         |
      | 192.168.154.31 |