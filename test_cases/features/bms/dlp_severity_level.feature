# Created by gaojie at 2024-04-29
Feature: 严重性等级
  规则管理 -> 敏感级别 -> 严重性等级 相关功能测试用例

  Background:
    Given 进入地址：/
    When 如果跳转到登录页面：${login_url}, 使用用户名：${login}，密码：${password}重新登录
    When 进入模块：规则管理
    And 进入二级菜单：敏感级别 下的三级菜单：严重性等级

  @smoke
  Scenario: 新增严重性等级
    Given 点击按钮：新增严重性等级
    When 输入新增严重性等级信息：
      """
        {
          "严重性等级名称": "极低",
          "对应严重性等级": "1",
          "严重性等级颜色": "#5ADCA8"
        }
      """
    And 点击【新增严重性等级】页面的【确认】按钮
    Then 弹出提示框，显示提示信息：提交成功