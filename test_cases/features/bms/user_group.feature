# Created by gaojie at 2024-03-28
Feature: 用户及机构管理模块
  用户管理 -> 基础数据管理 -> 用户与机构管理模块 相关功能测试用例

  Background:
    Given 进入地址：/
    When 如果跳转到登录页面：${login_url}, 使用用户名：${login}，密码：${password}重新登录
    When 进入模块：用户管理
    And 进入二级菜单：基础数据管理 下的三级菜单：用户与机构管理



  Scenario: 手动新增用户
    Given 点击按钮：新增
    When 输入新增用户信息：
      | 账号   | 认证方式 | 姓名   | 所属机构 | 职位    |
      | 自动化测试用户 | 口令认证 | 测试   | 默认组   | 普通职员 |
    And 点击按钮：确认
    Then 弹出提示框，显示提示信息：新增成功


  Scenario: 手动新增组织机构
    Given 登录-接口
    When 添加用户组-接口






