# Created by gaojie at 2024-04-26
Feature: 管理员审计模块
  系统管理 -> 运维管理 -> 管理员审计模块 相关功能测试用例

  Background:
    Given 进入地址：/
    When 如果跳转到登录页面：${login_url}, 使用用户名：${login}，密码：${password}重新登录
    When 进入模块：系统管理
    And 进入二级菜单：运维管理 下的三级菜单：管理员审计

#  Scenario: 查看审计日志
#    Given 点击按钮：搜索
#    When