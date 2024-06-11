# Created by gaojie at 2024-04-01
Feature: 自定义用户组管理模块
  用户管理 -> 基础数据管理 -> 自定义用户组管理模块 相关功能测试用例

  Background:
    Given 进入地址：/
    When 如果跳转到登录页面：${login_url}, 使用用户名：${login}，密码：${password}重新登录
    When 进入模块：用户管理
    And 进入二级菜单：基础数据管理 下的三级菜单：自定义用户组管理

  Scenario: 新增自定义用户组
    Given 点击按钮：新增用户组
    When 输入用户组名称：自定义用户组，备注：自定义用户组
    And 点击按钮：添加用户
    And 选择用户：gaojie
    And 点击按钮：确定
    Then 弹出提示框，显示提示信息：创建成功

  Scenario: 自定义用户组查询
    When 根据查询条件进行自定义用户组查询：
      """
        {
          "用户组名称": "自定义用户组"
        }
      """

  Scenario Outline: 删除自定义用户组
    When 删除自定义用户组：<用户组名称>
    Examples:
      | 用户组名称  |
      | 自定义用户组 |