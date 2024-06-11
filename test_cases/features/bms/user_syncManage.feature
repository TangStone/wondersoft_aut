# Created by gaojie at 2024-04-15
Feature: 用户推送模块
  用户管理 -> 用户同步管理 -> 用户推送 相关功能测试用例

  Background:
    Given 进入地址：/
    When 如果跳转到登录页面：${login_url}, 使用用户名：${login}，密码：${password}重新登录
    When 进入模块：用户管理
    And 进入二级菜单：用户同步管理 下的三级菜单：用户推送

  Scenario: 用户推送
    Given 选择系统名称：自定义审批系统，点击操作：推送
    Then 弹出提示框，显示提示信息：推送成功
#    When 推送状态：推送成功，推送时间
